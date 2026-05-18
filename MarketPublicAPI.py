"""
MarketPublicAPI
===============
Servicio REST independiente basado en FastAPI que expone información clave
de cada activo almacenado en la BD de MarketManager.

Permite a otros servicios externos consultar:
  - Lista de activos disponibles
  - Resumen actual con señales de decisión (BUY/SELL/WAIT, tendencia, ángulos, etc.)
  - Histórico reciente de N días

Arrancar con:
    python MarketPublicAPI.py
    uvicorn MarketPublicAPI:app --host 0.0.0.0 --port 8765 --reload

Swagger UI disponible en: http://localhost:8765/docs
"""

import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any

from service.MarketSQLManager import MarketSQLManager
from service.AlpacaServiceBot import AlpacaServiceBot
from service.AlpacaServiceBot import AlpacaServiceBot as AlpacaBot

# ─────────────────────────────────────────────
# Inicialización de la app y del acceso a datos
# ─────────────────────────────────────────────

app = FastAPI(
    title="MarketManager Public API",
    description=(
        "API REST pública que expone el estado actual y el histórico de activos "
        "gestionados por MarketManager. Diseñada para ser consumida por bots, "
        "dashboards u otros servicios externos."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Permitir acceso desde cualquier origen (ajustar en producción si es necesario)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancia global del gestor de BD (sin simulación)
_db = MarketSQLManager(simulation=False)
_alpaca = AlpacaServiceBot()


# ─────────────────────────────────────────────
# Modelos de respuesta (tipado como dict para
# compatibilidad con diferentes versiones de pydantic)
# ─────────────────────────────────────────────

def _format_asset_summary(raw: dict) -> dict:
    """
    Normaliza y enriquece el diccionario crudo devuelto por MarketSQLManager
    con campos de utilidad para la toma de decisiones.
    """
    if not raw:
        return {}

    # Calcular señal de dirección simplificada
    action = raw.get("action") or "WAIT"
    week_flow = raw.get("week_flow") or ""
    direction = raw.get("direction") or ""
    angle = raw.get("angle")
    rel_fcst = raw.get("rel_fcst") or ""

    bias = "NEUTRAL"
    if action in ("BUY",):
        bias = "BULLISH"
    elif action in ("SELL",):
        bias = "BEARISH"
    elif "UP" in week_flow:
        bias = "BULLISH_WEAK"
    elif "DOWN" in week_flow:
        bias = "BEARISH_WEAK"

    # Rango esperado de precio
    close_up = raw.get("close_nxt_up")
    close_down = raw.get("close_nxt_down")
    close_mid = raw.get("close_nxt_middle")
    price = raw.get("price")
    expected_range_pct = None
    if price and close_up and close_down and float(price) > 0:
        span = abs(float(close_up) - float(close_down))
        expected_range_pct = round(span / float(price) * 100, 4)

    return {
        # ---- Identificación ----
        "name":               raw.get("name"),
        "timestamp":          raw.get("timestamp"),
        "retrieved_at":       datetime.datetime.utcnow().isoformat() + "Z",

        # ---- Precio actual ----
        "price":              raw.get("price"),
        "open_value":         raw.get("open_value"),
        "last_dif":           raw.get("last_dif"),
        "acumulate":          raw.get("acumulate"),

        # ---- Señales de acción ----
        "action":             action,
        "action_count":       raw.get("action_count"),
        "action_acum":        raw.get("action_acum"),
        "bias":               bias,

        # ---- Tendencia y flujo ----
        "tendence":           raw.get("tendence"),
        "direction":          direction,
        "week_flow":          week_flow,
        "week_dir":           raw.get("week_dir"),

        # ---- Previsiones de cierre ----
        "close_nxt_up":       close_up,
        "close_nxt_down":     close_down,
        "close_nxt_middle":   close_mid,
        "expected_range_pct": expected_range_pct,

        # ---- Indicadores de volatilidad/flujo semanal ----
        "rel_fcst":           rel_fcst,
        "rel_fcst_percent":   raw.get("rel_fcst_percent"),
        "rel_fcst_std":       raw.get("rel_fcst_std"),
        "rel_fcst_med":       raw.get("rel_fcst_med"),
        "week_flow_med":      raw.get("week_flow_med"),
        "week_flow_std":      raw.get("week_flow_std"),

        # ---- Ángulos (momentum angular) ----
        "angle":              angle,
        "angle_ima":          raw.get("angle_ima"),
        "angle_counter":      raw.get("angle_counter"),

        # ---- Rangos de precio ----
        "global_min":         raw.get("global_min"),
        "global_max":         raw.get("global_max"),
        "motion_min":         raw.get("motion_min"),
        "motion_max":         raw.get("motion_max"),
        "week_dir_bot_dst":   raw.get("week_dir_bot_dst"),
        "month_dir_bot_dst":  raw.get("month_dir_bot_dst"),

        # ---- P&L / Riesgo ----
        "profit":             raw.get("profit"),
        "protect":            raw.get("protect"),
    }


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@app.get(
    "/health",
    summary="Health check",
    description="Verifica que el servicio está activo y la BD es accesible.",
    tags=["Sistema"],
)
def health_check():
    """Comprueba que la API y la BD están operativas."""
    try:
        assets = _db.get_active_assets()
        return {
            "status": "ok",
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "db": "connected",
            "assets_count": len(assets),
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "detail": str(e)},
        )


@app.get(
    "/assets",
    summary="Lista de activos",
    description="Devuelve todos los nombres de activos presentes en la BD.",
    tags=["Activos"],
    response_model=List[str],
)
def list_assets():
    """Lista todos los activos disponibles en la base de datos."""
    try:
        return _db.get_active_assets()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/asset/{name}",
    summary="Estado actual de un activo",
    description=(
        "Devuelve el estado más reciente de un activo con todos los indicadores "
        "relevantes para la toma de decisiones: acción, tendencia, flujo semanal, "
        "ángulos, previsiones de cierre, rangos de precio y P&L."
    ),
    tags=["Activos"],
    response_model=Dict[str, Any],
)
def get_asset(name: str):
    """
    Retorna un resumen completo del activo `name` con las señales actuales.

    Campos clave:
    - **action**: BUY / SELL / WAIT / CLOSE
    - **bias**: BULLISH / BEARISH / BULLISH_WEAK / BEARISH_WEAK / NEUTRAL
    - **week_flow**: flujo semanal dominante
    - **close_nxt_up / close_nxt_down**: nivel esperado de precio la próxima sesión
    - **rel_fcst / rel_fcst_percent**: forecast relativo y porcentaje
    - **angle / angle_ima**: momento angular del precio
    - **profit / protect**: beneficio acumulado y nivel de protección
    """
    raw = _db.get_asset_summary(name.upper())
    if not raw:
        raise HTTPException(
            status_code=404,
            detail=f"Activo '{name}' no encontrado en la base de datos.",
        )
    return _format_asset_summary(raw)


@app.get(
    "/asset/{name}/history",
    summary="Histórico reciente de un activo",
    description=(
        "Devuelve los registros diarios de los últimos N días para el activo indicado. "
        "Incluye precio, acción, tendencia, flujo, ángulo y P&L."
    ),
    tags=["Activos"],
    response_model=List[Dict[str, Any]],
)
def get_asset_history(
    name: str,
    days: int = Query(default=5, ge=1, le=90, description="Número de días hacia atrás"),
):
    """
    Devuelve el histórico reciente del activo `name` para los últimos `days` días.
    Útil para analizar la evolución de señales, tendencia y acumulados.
    """
    try:
        history = _db.get_asset_history(name.upper(), days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not history:
        raise HTTPException(
            status_code=404,
            detail=f"No se encontraron datos para '{name}' en los últimos {days} días.",
        )
    return history


@app.get(
    "/assets/summary",
    summary="Resumen de todos los activos",
    description=(
        "Devuelve el estado actual de TODOS los activos disponibles en un solo request. "
        "Ideal para dashboards o servicios que necesitan un snapshot global del mercado."
    ),
    tags=["Activos"],
    response_model=List[Dict[str, Any]],
)
def get_all_assets_summary():
    """
    Snapshot completo del mercado: devuelve el estado actual de cada activo.
    La lista está ordenada por nombre de activo.
    """
    try:
        asset_names = _db.get_active_assets()
        summaries = []
        for asset_name in asset_names:
            raw = _db.get_asset_summary(asset_name)
            if raw:
                summaries.append(_format_asset_summary(raw))
        return summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# Endpoints de Operación (Trading)
# ─────────────────────────────────────────────

@app.post(
    "/asset/{name}/buy",
    summary="Comprar activo",
    description="Ejecuta una orden de compra (LONG) por el monto en USD especificado utilizando Alpaca.",
    tags=["Operaciones"],
)
def buy_asset(name: str, amount_usd: float = Query(..., description="Monto en USD a invertir")):
    try:
        result = _alpaca.execute_target_position(name.upper(), "LONG", amount_usd)
        return {"status": "success", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/asset/{name}/sell",
    summary="Vender activo",
    description="Ejecuta una orden de venta en corto (SHORT) por el monto en USD especificado utilizando Alpaca.",
    tags=["Operaciones"],
)
def sell_asset(name: str, amount_usd: float = Query(..., description="Monto en USD a invertir")):
    try:
        result = _alpaca.execute_target_position(name.upper(), "SHORT", amount_usd)
        return {"status": "success", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/asset/{name}/close",
    summary="Cerrar posición",
    description="Cierra cualquier posición abierta (LONG o SHORT) y cancela órdenes pendientes para el activo.",
    tags=["Operaciones"],
)
def close_asset(name: str):
    try:
        result = _alpaca.close_all_positions_and_orders(name.upper())
        return {"status": "success", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/asset/{name}/stop-loss",
    summary="Configurar Stop Loss Inteligente",
    description="Configura un stop loss basado en la pérdida máxima permitida o en proteger las ganancias, dependiendo del estado actual de la posición.",
    tags=["Operaciones"],
)
def set_smart_stop_loss(
    name: str, 
    max_loss_usd: float = Query(..., description="Pérdida máxima permitida en USD (ej. 5.0)"),
    protect_profit_usd: float = Query(..., description="Ganancia a proteger en USD (ej. 2.0)")
):
    try:
        symbol = name.upper()
        # Determinar si es crypto (convención: termina en USD y longitud > 5, ej. BTCUSD)
        is_crypto = symbol.endswith("USD") and len(symbol) > 5
        
        if is_crypto:
            symbol_slash = symbol[:-3] + "/" + symbol[-3:]
            result = _alpaca.add_smart_stop_usd_crypto(
                symbol, 
                symbol_slash, 
                max_loss_usd, 
                protect_profit_usd
            )
        else:
            result = _alpaca.add_smart_stop_usd_stock(
                symbol, 
                max_loss_usd, 
                protect_profit_usd
            )
            
        return {"status": "success", "detail": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/trading/positions",
    summary="Posiciones abiertas en Alpaca",
    description="Devuelve todas las posiciones abiertas actuales con P&L no realizado.",
    tags=["Trading"],
)
def get_alpaca_positions():
    try:
        positions = _alpaca.listPositions()
        result = []
        for p in positions:
            result.append({
                "symbol": p.symbol,
                "qty": float(p.qty),
                "side": p.side,
                "avg_entry_price": float(p.avg_entry_price),
                "current_price": float(p.current_price),
                "unrealized_pl": float(p.unrealized_pl),
                "unrealized_plpc": float(p.unrealized_plpc),
                "market_value": float(p.market_value),
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/trading/orders",
    summary="Órdenes abiertas en Alpaca",
    description="Devuelve todas las órdenes abiertas (pending, partially_filled, etc).",
    tags=["Trading"],
)
def get_alpaca_orders(
    symbol: Optional[str] = Query(default=None, description="Filtrar por símbolo (opcional)"),
):
    try:
        from alpaca.trading.requests import GetOrdersRequest
        from alpaca.trading.enums import QueryOrderStatus
        
        req = GetOrdersRequest(
            status=QueryOrderStatus.OPEN,
            symbols=[symbol.upper()] if symbol else None,
        )
        orders = _alpaca.api.get_orders(req)
        
        result = []
        for o in orders:
            result.append({
                "id": str(o.id),
                "symbol": o.symbol,
                "side": o.side.value,
                "type": o.type.value,
                "qty": float(o.qty),
                "filled_qty": float(o.filled_qty),
                "status": o.status.value,
                "limit_price": float(o.limit_price) if o.limit_price else None,
                "stop_price": float(o.stop_price) if o.stop_price else None,
                "created_at": str(o.created_at),
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete(
    "/trading/orders/{order_id}",
    summary="Cancelar una orden",
    description="Cancela una orden abierta por su ID. Devuelve error si ya estaba cancelada o completada.",
    tags=["Trading"],
)
def cancel_order(order_id: str):
    try:
        _alpaca.api.cancel_order_by_id(order_id)
        return {"status": "success", "detail": f"Orden {order_id} cancelada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/trading/close-all",
    summary="Cerrar todas las posiciones",
    description="Cierra todas las posiciones abiertas y cancela todas las órdenes.",
    tags=["Trading"],
)
def close_all_positions():
    try:
        # Cancelar todas las órdenes primero
        _alpaca.api.cancel_orders()
        
        # Cerrar todas las posiciones
        _alpaca.api.close_all_positions()
        
        return {"status": "success", "detail": "Todas las posiciones y órdenes cerradas"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post(
    "/trading/daily-loss-limit",
    summary="Límite de pérdida diaria",
    description="Cierra todas las posiciones si el P&L del día supera la pérdida máxima permitida. Protege el capital.",
    tags=["Trading"],
)
def set_daily_loss_limit(
    max_loss_usd: float = Query(..., description="Pérdida máxima diaria en USD (ej. 50.0)"),
):
    try:
        # Obtener P&L del día
        pnl_data = _alpaca.get_daily_pnl_by_asset()
        
        if pnl_data.empty:
            return {"status": "success", "detail": "No hay posiciones abiertas", "daily_pnl": 0}
        
        total_pnl = pnl_data['pnl'].sum()
        
        if total_pnl < 0 and abs(total_pnl) >= max_loss_usd:
            # Pérdida supera el límite → cerrar todo
            _alpaca.api.cancel_orders()
            _alpaca.api.close_all_positions()
            return {
                "status": "limit_reached",
                "detail": f"Límite de pérdida alcanzado: ${total_pnl:.2f} >= ${max_loss_usd:.2f}. Todo cerrado.",
                "daily_pnl": total_pnl,
                "closed": True,
            }
        else:
            return {
                "status": "ok",
                "detail": f"P&L del día: ${total_pnl:.2f} (límite: ${max_loss_usd:.2f})",
                "daily_pnl": total_pnl,
                "closed": False,
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# Entrada principal
# ─────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run(
        "MarketPublicAPI:app",
        host="0.0.0.0",
        port=8765,
        reload=False,
        log_level="info",
    )
