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
import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any

from service.MarketSQLManager import MarketSQLManager
from service.AlpacaServiceBot import AlpacaServiceBot
from alpaca.trading.requests import GetOrdersRequest
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




# ══════════════════════════════════════════════════════════════
# ACTIVITY / AUDIT ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.get(
    "/activity/today",
    summary="Actividad de hoy — todos los activos",
    description="Devuelve actividad de trading del día para todos los activos con operaciones.",
    tags=["Activity"],
)
def get_activity_today():
    """Resumen de actividad del día para todos los activos."""
    try:
        date = datetime.date.today().strftime('%Y-%m-%d')
        # Get all unique symbols from orders today
        request = GetOrdersRequest(status="all", limit=1000)
        orders = _alpaca.api.get_orders(request)
        
        today_start = datetime.datetime.combine(datetime.date.today(), datetime.datetime.min.time()).replace(tzinfo=datetime.timezone.utc)
        today_orders = [o for o in orders if o.created_at and (o.created_at.replace(tzinfo=datetime.timezone.utc) if o.created_at.tzinfo is None else o.created_at) >= today_start]
        
        symbols = set()
        for o in today_orders:
            if o.filled_at and float(o.filled_qty) > 0:
                symbols.add(o.symbol)
        
        if not symbols:
            # Still include symbols with open positions even if no new trades today
            try:
                positions = _alpaca.api.get_all_positions()
                for p in positions:
                    qty = abs(float(p.qty))
                    if qty > 0:
                        symbols.add(p.symbol)
            except:
                pass
            if not symbols:
                return {"date": date, "assets": [], "total_pnl": 0, "count": 0}
        
        results = []
        total_pnl = 0
        for symbol in sorted(symbols):
            activity = _alpaca.get_asset_activity(symbol, date)
            results.append({
                "symbol": symbol,
                "long_opens": activity["long_opens"],
                "long_closes": activity["long_closes"],
                "short_opens": activity["short_opens"],
                "short_closes": activity["short_closes"],
                "total_opens": activity["total_opens"],
                "total_closes": activity["total_closes"],
                "pnl": round(activity["total_pnl"], 2),
                "trades": len(activity["trades"]),
                "open_positions": activity["open_positions"],
            })
            total_pnl += activity["total_pnl"]
        
        # Add unrealized PnL from currently open positions (floating P&L)
        try:
            positions = _alpaca.api.get_all_positions()
            unrealized_total = 0
            for p in positions:
                qty = abs(float(p.qty))
                if qty > 0:
                    entry = float(p.avg_entry_price)
                    current = float(p.current_price)
                    unrealized = (current - entry) * qty if float(p.qty) > 0 else (entry - current) * qty
                    unrealized_total += unrealized
                    for r in results:
                        if r["symbol"] == p.symbol:
                            r["pnl"] = round((r["pnl"] or 0) + unrealized, 2)
                            break
            total_pnl += unrealized_total
        except:
            pass
        
        results.sort(key=lambda x: x["pnl"], reverse=True)
        
        return {
            "date": date,
            "assets": results,
            "total_pnl": round(total_pnl, 2),
            "count": len(results),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/activity/by-asset/{symbol}",
    summary="Actividad por activo y fecha",
    description="Detalle completo de actividad de trading para un activo específico.",
    tags=["Activity"],
)
def get_activity_by_asset(
    symbol: str,
    date: Optional[str] = Query(None, description="Fecha YYYY-MM-DD (default: hoy)"),
):
    """Detalle de actividad por activo."""
    try:
        if date is None:
            date = datetime.date.today().strftime('%Y-%m-%d')
        activity = _alpaca.get_asset_activity(symbol.upper(), date)
        return activity
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/activity/range",
    summary="Actividad en rango de fechas",
    description="PnL por activo para un rango de días.",
    tags=["Activity"],
)
def get_activity_range(
    date_from: str = Query(..., description="Fecha inicio YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="Fecha fin YYYY-MM-DD (default: hoy)"),
):
    """Resumen de PnL por activo para un rango de fechas."""
    try:
        if date_to is None:
            date_to = datetime.date.today().strftime('%Y-%m-%d')
        
        start = datetime.datetime.fromisoformat(date_from)
        end = datetime.datetime.fromisoformat(date_to)
        end = datetime.datetime.combine(end.date(), datetime.datetime.max.time())
        
        # Limit range to 30 days to avoid saturating Alpaca API
        days_diff = (end.date() - start.date()).days
        if days_diff > 30:
            return {
                "error": f"Rango máximo de 30 días permitido. Rango solicitado: {days_diff} días.",
                "date_from": date_from,
                "date_to": date_to,
                "assets": [],
            }
        
        request = GetOrdersRequest(status="all", after=start.isoformat(), until=end.isoformat(), limit=1000)
        orders = _alpaca.api.get_orders(request)
        
        # Group orders by symbol (single API call, no per-symbol calls)
        from collections import defaultdict
        symbol_orders = defaultdict(list)
        for o in orders:
            if o.filled_at and float(o.filled_qty) > 0:
                symbol_orders[o.symbol].append(o)
        
        results = []
        for symbol in sorted(symbol_orders.keys()):
            orders_list = symbol_orders[symbol]
            
            long_stack = []
            short_stack = []
            daily_pnl = defaultdict(float)
            total_opens = 0
            total_closes = 0
            
            def get_filled_at(o):
                return o.filled_at if o.filled_at else datetime.datetime.min.time()
            
            orders_list.sort(key=get_filled_at)
            
            for o in orders_list:
                qty = abs(float(o.filled_qty))
                price = float(o.filled_avg_price)
                side = o.side.value
                filled_at = o.filled_at.isoformat() if o.filled_at else ""
                day = filled_at[:10]
                
                trade_pnl = 0.0
                
                if side == "buy":
                    temp_qty = qty
                    while temp_qty > 0 and short_stack:
                        entry_price, entry_qty = short_stack[0]
                        if entry_qty <= temp_qty:
                            cover_qty = entry_qty
                            pnl = (entry_price - price) * cover_qty
                            trade_pnl += pnl
                            daily_pnl[day] += pnl
                            total_closes += 1
                            temp_qty -= entry_qty
                            short_stack.pop(0)
                        else:
                            cover_qty = temp_qty
                            pnl = (entry_price - price) * cover_qty
                            trade_pnl += pnl
                            daily_pnl[day] += pnl
                            total_closes += 1
                            short_stack[0] = (entry_price, entry_qty - temp_qty)
                            temp_qty = 0
                    if temp_qty > 0:
                        long_stack.append((price, temp_qty))
                        total_opens += 1
                        
                elif side == "sell":
                    temp_qty = qty
                    while temp_qty > 0 and long_stack:
                        entry_price, entry_qty = long_stack[0]
                        if entry_qty <= temp_qty:
                            cover_qty = entry_qty
                            pnl = (price - entry_price) * cover_qty
                            trade_pnl += pnl
                            daily_pnl[day] += pnl
                            total_closes += 1
                            temp_qty -= entry_qty
                            long_stack.pop(0)
                        else:
                            cover_qty = temp_qty
                            pnl = (price - entry_price) * cover_qty
                            trade_pnl += pnl
                            daily_pnl[day] += pnl
                            total_closes += 1
                            long_stack[0] = (entry_price, entry_qty - temp_qty)
                            temp_qty = 0
                    if temp_qty > 0:
                        short_stack.append((price, temp_qty))
                        total_opens += 1
            
            total_pnl = sum(daily_pnl.values())
            
            results.append({
                "symbol": symbol,
                "total_pnl": round(total_pnl, 2),
                "total_opens": total_opens,
                "total_closes": total_closes,
                "daily_pnl": dict(daily_pnl),
            })
        
        results.sort(key=lambda x: x["total_pnl"], reverse=True)
        
        total_pnl = sum(r["total_pnl"] or 0 for r in results)
        
        return {
            "date_from": date_from,
            "date_to": date_to,
            "assets": results,
            "total_pnl": round(total_pnl, 2),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/activity/positions",
    summary="Posiciones abiertas ahora",
    description="Todas las posiciones abiertas en este momento con entry price y PnL flotante.",
    tags=["Activity"],
)
def get_open_positions():
    """Posiciones abiertas con PnL no realizado."""
    try:
        positions = _alpaca.api.get_all_positions()
        
        result = []
        for p in positions:
            qty = float(p.qty)
            entry = float(p.avg_entry_price)
            current = float(p.current_price)
            pnl = (current - entry) * qty if qty > 0 else (entry - current) * abs(qty)
            result.append({
                "symbol": p.symbol,
                "qty": qty,
                "entry_price": entry,
                "current_price": current,
                "market_value": float(p.market_value),
                "unrealized_pnl": round(pnl, 2),
                "side": "long" if qty > 0 else "short",
                "change_today": round(float(p.change_today or 0), 2),
            })
        
        total_pnl = sum(r["unrealized_pnl"] for r in result)
        result.sort(key=lambda x: x["unrealized_pnl"], reverse=True)
        
        return {
            "positions": result,
            "total_unrealized_pnl": round(total_pnl, 2),
            "count": len(result),
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


# ═══════════════════════════════════════════════════════════════
# PERFORMANCE DB — Métricas desde la BD local (sin Alpaca)
# ═══════════════════════════════════════════════════════════════

@app.get(
    "/db/performance/summary",
    summary="Resumen P&L global por período",
    description="PnL total realizado, operaciones y mejores/peores activos para hoy, 7, 14, 30 días y mes actual.",
    tags=["Performance DB"],
)
def get_db_performance_summary():
    """Resumen global de rendimiento calculado desde la BD local."""
    try:
        db_path = "/home/MarketManager/market.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        today = datetime.date.today()
        periods = {
            "today":    (today, today),
            "1d":      (today - datetime.timedelta(days=1), today),
            "2d":      (today - datetime.timedelta(days=2), today),
            "3d":      (today - datetime.timedelta(days=3), today),
            "7d":      (today - datetime.timedelta(days=7), today),
            "14d":     (today - datetime.timedelta(days=14), today),
            "30d":     (today - datetime.timedelta(days=30), today),
        }

        month_start = datetime.date(today.year, today.month, 1)
        periods["month"] = (month_start, today)

        close_actions = ("'CLOSE'", "'CLOSE-BUY'", "'CLOSE-SELL'")

        results = {}
        for label, (date_from, date_to) in periods.items():
            cur.execute(f"""
                SELECT
                    COALESCE(SUM(REVENUE), 0) as total_pnl,
                    COUNT(*) as total_ops,
                    COUNT(DISTINCT NAME) as total_assets
                FROM MARKET
                WHERE ACTION IN ({','.join(close_actions)})
                AND DATE(DATEVALUE) >= '{date_from}'
                AND DATE(DATEVALUE) <= '{date_to}'
            """)
            row = cur.fetchone()
            results[label] = {
                "total_pnl": round(row[0] or 0, 2),
                "total_ops": row[1] or 0,
                "total_assets": row[2] or 0,
            }

        conn.close()
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/performance/assets",
    summary="PnL por activo y período",
    description="PnL por cada activo para períodos selectedos: 1d, 7d, 30d, mes actual.",
    tags=["Performance DB"],
)
def get_db_performance_assets(period: str = Query("30d", description="1d|7d|14d|30d|month")):
    """PnL por activo para un período específico."""
    try:
        db_path = "/home/MarketManager/market.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        today = datetime.date.today()
        if period == "today":
            date_from = today
        elif period == "1d":
            date_from = today - datetime.timedelta(days=1)
        elif period == "2d":
            date_from = today - datetime.timedelta(days=2)
        elif period == "3d":
            date_from = today - datetime.timedelta(days=3)
        elif period == "7d":
            date_from = today - datetime.timedelta(days=7)
        elif period == "14d":
            date_from = today - datetime.timedelta(days=14)
        elif period == "month":
            date_from = datetime.date(today.year, today.month, 1)
        else:
            date_from = today - datetime.timedelta(days=30)

        close_actions = ("'CLOSE'", "'CLOSE-BUY'", "'CLOSE-SELL'")

        cur.execute(f"""
            SELECT
                NAME as symbol,
                COALESCE(SUM(REVENUE), 0) as total_pnl,
                COUNT(*) as total_ops,
                MIN(DATEVALUE) as first_seen,
                MAX(DATEVALUE) as last_seen
            FROM MARKET
            WHERE ACTION IN ({','.join(close_actions)})
            AND DATE(DATEVALUE) >= '{date_from}'
            AND DATE(DATEVALUE) <= '{today}'
            GROUP BY NAME
            ORDER BY total_pnl DESC
        """)
        rows = cur.fetchall()
        conn.close()

        assets = [{
            "symbol": r[0],
            "total_pnl": round(r[1] or 0, 2),
            "total_ops": r[2] or 0,
        } for r in rows]

        return {
            "period": period,
            "date_from": str(date_from),
            "date_to": str(today),
            "total_pnl": round(sum(a["total_pnl"] for a in assets), 2),
            "assets": assets,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/performance/calendar/{symbol}",
    summary="Calendario PnL por activo (heatmap)",
    description="PnL diario de un activo para un mes concreto. Sirve para el heatmap del calendario.",
    tags=["Performance DB"],
)
def get_db_performance_calendar(
    symbol: str,
    year: int = Query(None, description="Año YYYY (default: año actual)"),
    month: int = Query(None, description="Mes 1-12 (default: mes actual)"),
):
    """Calendario de PnL diario para un activo y mes dados."""
    try:
        db_path = "/home/MarketManager/market.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        today = datetime.date.today()
        if year is None:
            year = today.year
        if month is None:
            month = today.month

        date_from = datetime.date(year, month, 1)
        if month == 12:
            date_to = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            date_to = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        close_actions = ("'CLOSE'", "'CLOSE-BUY'", "'CLOSE-SELL'")

        cur.execute(f"""
            SELECT
                DATE(DATEVALUE) as day,
                COALESCE(SUM(REVENUE), 0) as pnl,
                COUNT(*) as ops
            FROM MARKET
            WHERE NAME = ?
            AND ACTION IN ({','.join(close_actions)})
            AND DATE(DATEVALUE) >= '{date_from}'
            AND DATE(DATEVALUE) <= '{date_to}'
            GROUP BY DATE(DATEVALUE)
            ORDER BY day
        """, (symbol.upper(),))
        rows = cur.fetchall()
        conn.close()

        days = []
        for r in rows:
            days.append({
                "date": r[0],
                "pnl": round(r[1], 2),
                "ops": r[2],
                "status": "positive" if r[1] > 0 else ("negative" if r[1] < 0 else "neutral"),
            })

        return {
            "symbol": symbol.upper(),
            "year": year,
            "month": month,
            "days": days,
            "month_pnl": round(sum(d["pnl"] for d in days), 2),
            "positive_days": sum(1 for d in days if d["pnl"] > 0),
            "negative_days": sum(1 for d in days if d["pnl"] < 0),
            "neutral_days": sum(1 for d in days if d["pnl"] == 0),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/performance/intraday/{symbol}",
    summary="PnL intradiario por activo para hoy",
    description="PnL por cada operación de hoy para un activo, mostrando precio, hora y PnL individual.",
    tags=["Performance DB"],
)
def get_db_performance_intraday(symbol: str):
    """Detalle intradiario de operaciones para hoy."""
    try:
        db_path = "/home/MarketManager/market.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        today = datetime.date.today()

        close_actions = ("'CLOSE'", "'CLOSE-BUY'", "'CLOSE-SELL'")

        cur.execute(f"""
            SELECT
                DATEVALUE,
                VALUE,
                REVENUE,
                PROFIT,
                ACTION,
                QTY,
                DIRECTION
            FROM MARKET
            WHERE NAME = ?
            AND DATE(DATEVALUE) = '{today}'
            ORDER BY DATEVALUE
        """, (symbol.upper(),))
        rows = cur.fetchall()
        conn.close()

        trades = [{
            "datetime": r[0],
            "price": round(r[1], 4),
            "revenue": round(r[2], 4),
            "profit": round(r[3], 4),
            "action": r[4],
            "qty": r[5],
            "direction": r[6],
        } for r in rows]

        return {
            "symbol": symbol.upper(),
            "date": str(today),
            "trades": trades,
            "total_pnl": round(sum(t["revenue"] for t in trades if t["action"] in ("CLOSE", "CLOSE-BUY", "CLOSE-SELL")), 2),
            "total_ops": len(trades),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/performance/monthly",
    summary="PnL mensual histórico",
    description="PnL total por cada mes para todos los activos combinados.",
    tags=["Performance DB"],
)
def get_db_performance_monthly():
    """PnL mensual acumulado de todos los activos."""
    try:
        db_path = "/home/MarketManager/market.db"
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        close_actions = ("'CLOSE'", "'CLOSE-BUY'", "'CLOSE-SELL'")

        cur.execute(f"""
            SELECT
                strftime('%Y', DATEVALUE) as year,
                strftime('%m', DATEVALUE) as month,
                COALESCE(SUM(REVENUE), 0) as total_pnl,
                COUNT(*) as total_ops,
                COUNT(DISTINCT NAME) as total_assets
            FROM MARKET
            WHERE ACTION IN ({','.join(close_actions)})
            GROUP BY year, month
            ORDER BY year DESC, month DESC
        """)
        rows = cur.fetchall()
        conn.close()

        months = []
        for r in rows:
            months.append({
                "year": int(r[0]),
                "month": int(r[1]),
                "month_name": datetime.date(int(r[0]), int(r[1]), 1).strftime("%B"),
                "total_pnl": round(r[2], 2),
                "total_ops": r[3] or 0,
                "total_assets": r[4] or 0,
            })

        # Compute cumulative
        cumulative = 0.0
        for m in months:
            cumulative += m["total_pnl"]
            m["cumulative_pnl"] = round(cumulative, 2)

        months.reverse()

        return {"months": months}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════
# ANALYTICS — Detailed asset analysis, evaluator insights, signals
# ═══════════════════════════════════════════════════════════════

@app.get(
    "/db/analytics/asset/{symbol}",
    summary="Análisis completo de activo",
    description="Todos los detalles de un activo: evaluadores usados, señales, histórico diario.",
    tags=["Analytics"],
)
def get_analytics_asset(symbol: str):
    """Análisis completo de un activo."""
    try:
        import sys
        sys.path.insert(0, '/home/MarketManager')
        from analize_db import (
            get_asset_evaluator_detail, get_asset_signal_history,
            get_asset_daily_detail, get_asset_current_signals
        )
        symbol = symbol.upper()
        return {
            "symbol": symbol,
            "current_signals": get_asset_current_signals(symbol),
            "evaluators": get_asset_evaluator_detail(symbol),
            "daily_detail": get_asset_daily_detail(symbol),
            "recent_signals": get_asset_signal_history(symbol),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/analytics/evaluators",
    summary="Ranking de evaluadores",
    description="Ranking global de todos los evaluadores por PnL total, ops, assets y PnL promedio.",
    tags=["Analytics"],
)
def get_analytics_evaluators():
    """Ranking de evaluadores ordenado por performance."""
    try:
        import sys
        sys.path.insert(0, '/home/MarketManager')
        from analize_db import get_global_evaluator_ranking
        return {"evaluators": get_global_evaluator_ranking()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/analytics/worst",
    summary="Activos en pérdida",
    description="Todos los activos que están en rojo, agrupados por evaluador causante.",
    tags=["Analytics"],
)
def get_analytics_worst():
    """Assets en pérdida con detalle del evaluador asociado."""
    try:
        import sys
        sys.path.insert(0, '/home/MarketManager')
        from analize_db import get_worst_assets_by_evaluator
        return {"loss_assets": get_worst_assets_by_evaluator()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/analytics/portfolio",
    summary="Resumen de todos los activos",
    description="PnL mensual y total de todos los activos, mejor evaluador, número de evaluadores usados.",
    tags=["Analytics"],
)
def get_analytics_portfolio():
    """Portfolio completo con métricas clave por activo."""
    try:
        import sys
        sys.path.insert(0, '/home/MarketManager')
        from analize_db import get_assets_with_pnl_summary
        assets = get_assets_with_pnl_summary()
        total_month = sum(a['month_pnl'] for a in assets)
        total_all = sum(a['total_pnl'] for a in assets)
        return {
            "assets": assets,
            "total_month_pnl": round(total_month, 2),
            "total_all_pnl": round(total_all, 2),
            "positive_month": sum(1 for a in assets if a['month_pnl'] > 0),
            "negative_month": sum(1 for a in assets if a['month_pnl'] < 0),
            "positive_all": sum(1 for a in assets if a['total_pnl'] > 0),
            "negative_all": sum(1 for a in assets if a['total_pnl'] < 0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/analytics/asset/{symbol}/signals",
    summary="Señales actuales de activo",
    description="Último estado de todas las señales (tendencia, ángulo, momentum, forecast) de un activo.",
    tags=["Analytics"],
)
def get_analytics_asset_signals(symbol: str):
    """Señales actuales de un activo para diagnosis."""
    try:
        import sys
        sys.path.insert(0, '/home/MarketManager')
        from analize_db import get_asset_current_signals
        sigs = get_asset_current_signals(symbol.upper())
        return {"symbol": symbol.upper(), "signals": sigs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════
# DOCUMENTATION — Evaluators, Indicators, Assets, System Docs
# ═══════════════════════════════════════════════════════════════

@app.get(
    "/db/docs/evaluators",
    summary="Documentación de evaluadores",
    description="Documentación completa de todos los evaluadores con stats, grades y detalle por activo.",
    tags=["Documentation"],
)
def get_docs_evaluators():
    """Documentación de todos los evaluadores usados en la BD."""
    try:
        import sys
        sys.path.insert(0, '/home/MarketManager')
        from docs_generator import get_evaluator_docs
        return {"evaluators": get_evaluator_docs()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/docs/indicators",
    summary="Documentación de indicadores",
    description="Definiciones, valores posibles y significado de cada indicador del sistema.",
    tags=["Documentation"],
)
def get_docs_indicators():
    """Documentación completa de indicadores."""
    try:
        import sys
        sys.path.insert(0, '/home/MarketManager')
        from docs_generator import get_indicator_stats, INDICATOR_DEFINITIONS
        stats = get_indicator_stats()
        return {
            "definitions": INDICATOR_DEFINITIONS,
            "usage_stats": stats,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/docs/assets",
    summary="Documentación de activos",
    description="Todos los activos con stats, rango de precios y mejor evaluador.",
    tags=["Documentation"],
)
def get_docs_assets():
    """Documentación de todos los activos."""
    try:
        import sys
        sys.path.insert(0, '/home/MarketManager')
        from docs_generator import get_assets_docs
        return {"assets": get_assets_docs()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    "/db/docs/system",
    summary="Documentación del sistema",
    description="Arquitectura, tablas, endpoints y configuración del sistema MarketManager.",
    tags=["Documentation"],
)
def get_docs_system():
    """Documentación general del sistema."""
    try:
        import sys
        sys.path.insert(0, '/home/MarketManager')
        from docs_generator import get_active_params_docs
        params = get_active_params_docs()
        return {
            "project": "MarketManager",
            "version": "1.0.0",
            "database": "/home/MarketManager/market.db",
            "total_tables": 7,
            "tables": {
                "MARKET": "Datos de mercado — 97k+ filas con señales, acciones, evaluadores, PnL",
                "MARKET_DATA": "Datos OHLCV diarios por activo (vacío en prod)",
                "CONTROL": "Valores de control por activo — umbrales SUBE/BAJA",
                "CONTROLTIME": "Control de timing — intervalos y predictores",
                "CONTROLMINMAX": "Precios históricos min/max por activo",
                "indicator_snapshots": "Snapshots de indicadores (vacío en prod)",
                "sqlite_sequence": "Metadatos internos de SQLite",
            },
            "active_params": params,
            "endpoints": {
                "performance": {
                    "/db/performance/summary": "PnL por período: hoy, 1d, 2d, 3d, 7d, 14d, 30d, mes",
                    "/db/performance/assets": "PnL por activo y período seleccionado",
                    "/db/performance/calendar/{symbol}": "Calendario PnL diario por activo y mes",
                    "/db/performance/intraday/{symbol}": "Detalle de operaciones intradiarias",
                    "/db/performance/monthly": "PnL mensual histórico acumulado",
                },
                "analytics": {
                    "/db/analytics/asset/{symbol}": "Análisis completo: evaluadores, señales, diario",
                    "/db/analytics/evaluators": "Ranking de evaluadores con stats",
                    "/db/analytics/worst": "Activos en pérdida por evaluador",
                    "/db/analytics/portfolio": "Resumen portfolio: PnL mes/total por activo",
                    "/db/analytics/asset/{symbol}/signals": "Señales actuales de un activo",
                },
                "docs": {
                    "/db/docs/evaluators": "Documentación completa de evaluadores",
                    "/db/docs/indicators": "Definiciones de indicadores",
                    "/db/docs/assets": "Documentación de activos",
                    "/db/docs/system": "Arquitectura y schema del sistema",
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
