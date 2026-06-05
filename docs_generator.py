"""
MarketManager Documentation Generator
"""
import sqlite3
from datetime import date

def _db():
    return sqlite3.connect('/home/MarketManager/market.db')


def get_evaluator_docs():
    """Documentación completa de cada evaluador"""
    close_actions = "'CLOSE','CLOSE-BUY','CLOSE-SELL'"

    conn = _db()
    cur = conn.cursor()

    # Main stats per evaluator
    cur.execute(f"""
        SELECT
            EVAL_NAME,
            COUNT(*) as total_ops,
            COUNT(DISTINCT NAME) as assets_count,
            SUM(REVENUE) as total_pnl,
            AVG(REVENUE) as avg_pnl,
            MIN(DATEVALUE) as first_seen,
            MAX(DATEVALUE) as last_seen,
            MIN(REVENUE) as worst_trade,
            MAX(REVENUE) as best_trade
        FROM MARKET
        WHERE EVAL_NAME IS NOT NULL AND ACTION IN ({close_actions})
        GROUP BY EVAL_NAME
        ORDER BY total_pnl DESC
    """)
    rows = cur.fetchall()
    conn.close()

    # Per-asset breakdown (single query, more efficient)
    conn2 = _db()
    cur2 = conn2.cursor()
    cur2.execute(f"""
        SELECT
            EVAL_NAME, NAME, SUM(REVENUE) as pnl, COUNT(*) as ops
        FROM MARKET
        WHERE EVAL_NAME IS NOT NULL AND ACTION IN ({close_actions})
        GROUP BY EVAL_NAME, NAME
        ORDER BY EVAL_NAME, pnl DESC
    """)
    asset_map = {}
    for ar in cur2.fetchall():
        ev = ar[0]
        if ev not in asset_map:
            asset_map[ev] = []
        asset_map[ev].append({'symbol': ar[1], 'pnl': round(ar[2], 2), 'ops': ar[3]})
    conn2.close()

    result = []
    cumulative = 0.0
    for r in rows:
        ev_name = r[0]
        pnl = r[3]
        cumulative += pnl
        result.append({
            'name': ev_name,
            'total_ops': r[1],
            'assets_count': r[2],
            'total_pnl': round(pnl, 2),
            'avg_pnl': round(r[4], 4),
            'first_seen': r[5],
            'last_seen': r[6],
            'worst_trade': round(r[7], 4),
            'best_trade': round(r[8], 4),
            'cumulative_pnl': round(cumulative, 2),
            'performance_grade': calc_grade(pnl, r[1], r[2]),
            'assets_detail': asset_map.get(ev_name, []),
        })

    return result


def calc_grade(pnl, ops, assets):
    if pnl < 0:
        if pnl < -1000: return 'F'
        elif pnl < -100: return 'D'
        elif pnl < -10: return 'C'
        return 'B'
    else:
        if pnl > 1000: return 'S'
        elif pnl > 100: return 'A'
        elif pnl > 10: return 'B'
        return 'C'


# ─── Indicators ───────────────────────────────────────────────────────────────

INDICATOR_DEFINITIONS = {
    'INDICATOR': {
        'description': 'Indicador principal de acción. Señales base del sistema.',
        'values': {
            'I_BUY':   {'label': 'I_BUY',   'action': 'BUY',  'color': '#22c55e', 'meaning': 'Señal de compra fuerte'},
            'I_BUYX':  {'label': 'I_BUYX',  'action': 'BUY',  'color': '#22c55e', 'meaning': 'Señal de compra confirmada'},
            'I_SELL':  {'label': 'I_SELL',  'action': 'SELL', 'color': '#ef4444', 'meaning': 'Señal de venta fuerte'},
            'I_SELLX': {'label': 'I_SELLX', 'action': 'SELL', 'color': '#ef4444', 'meaning': 'Señal de venta confirmada'},
            'WAIT':    {'label': 'WAIT',    'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Sin señal, espera'},
            'EMPTY':   {'label': 'EMPTY',   'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Sin datos'},
        }
    },
    'IMA_NEW': {
        'description': 'Media móvil adaptativa — señal principal de dirección.',
        'values': {
            'IMA_NEW_BUY':  {'label': 'BUY',  'action': 'BUY',  'color': '#22c55e', 'meaning': 'IMA indica compra'},
            'IMA_NEW_SELL': {'label': 'SELL', 'action': 'SELL', 'color': '#ef4444', 'meaning': 'IMA indica venta'},
            'IMA_NEW_WAIT': {'label': 'WAIT', 'action': 'WAIT', 'color': '#6b7280', 'meaning': 'IMA indica espera'},
        }
    },
    'DIRECTION': {
        'description': 'Dirección del precio en tiempo real.',
        'values': {
            'DIR_UP':       {'label': '↑ DIR UP',       'action': 'BUY',  'color': '#22c55e', 'meaning': 'Tendencia alcista confirmada'},
            'DIR_DOWN':     {'label': '↓ DIR DOWN',      'action': 'SELL', 'color': '#ef4444', 'meaning': 'Tendencia bajista confirmada'},
            'DIR_CHANGE':   {'label': '↔ DIR CHANGE',    'action': 'WAIT', 'color': '#f59e0b', 'meaning': 'Cambio de tendencia en progreso'},
            'DIR_PRE_UP':   {'label': '↗ PRE UP',        'action': 'BUY',  'color': '#22c55e', 'meaning': 'Pre-señal alcista'},
            'DIR_PRE_DOWN': {'label': '↘ PRE DOWN',      'action': 'SELL', 'color': '#ef4444', 'meaning': 'Pre-señal bajista'},
        }
    },
    'TENDENCE': {
        'description': 'Tendencia general del activo (largo plazo).',
        'values': {
            'SUBE':     {'label': '↑ SUBE',     'action': 'BUY',  'color': '#22c55e', 'meaning': 'Tendencia alcista general'},
            'BAJA':     {'label': '↓ BAJA',     'action': 'SELL', 'color': '#ef4444', 'meaning': 'Tendencia bajista general'},
            'MANTIENE': {'label': '→ MANTIENE', 'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Tendencia lateral / sin dirección'},
        }
    },
    'MARKET_TENDENCE': {
        'description': 'Tendencia del mercado global (índice general).',
        'values': {
            'MARKET_TENDENCE_UP':   {'label': 'Mercado ↑',   'action': 'BUY',  'color': '#22c55e', 'meaning': 'Mercado general alcista'},
            'MARKET_TENDENCE_DOWN': {'label': 'Mercado ↓',  'action': 'SELL', 'color': '#ef4444', 'meaning': 'Mercado general bajista'},
            'MARKET_TENDENCE_UNDEF':{'label': 'Mercado ?',  'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Mercado sin tendencia clara'},
        }
    },
    'WEEK_FLOW': {
        'description': 'Flujo semanal — dirección predominante de la semana.',
        'values': {
            'WEEK_FLOW_UP':   {'label': 'Semana ↑',  'action': 'BUY',  'color': '#22c55e', 'meaning': 'Flujo semanal positivo'},
            'WEEK_FLOW_DOWN': {'label': 'Semana ↓',  'action': 'SELL', 'color': '#ef4444', 'meaning': 'Flujo semanal negativo'},
            'WEEK_FLOW_WAIT': {'label': 'Semana →',  'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Flujo semanal neutral'},
        }
    },
    'WEEK_DIR': {
        'description': 'Dirección semanal de corto plazo.',
        'values': {
            'DIR_UP':   {'label': '↗ Semana UP',   'action': 'BUY',  'color': '#22c55e', 'meaning': 'Dirección semanal alcista'},
            'DIR_DOWN': {'label': '↘ Semana DOWN', 'action': 'SELL', 'color': '#ef4444', 'meaning': 'Dirección semanal bajista'},
        }
    },
    'REL_FCST': {
        'description': 'Forecast relativo — predicción de dirección basada en modelo.',
        'values': {
            'IND_REL_FCST_UP':      {'label': 'FCST ↑ UP',      'action': 'BUY',  'color': '#22c55e', 'meaning': 'Forecast predice subida'},
            'IND_REL_FCST_DOWN':    {'label': 'FCST ↓ DOWN',    'action': 'SELL', 'color': '#ef4444', 'meaning': 'Forecast predice bajada'},
            'IND_REL_FCST_PRE_UP':  {'label': 'FCST pre-↑',     'action': 'BUY',  'color': '#22c55e', 'meaning': 'Pre-forecast de subida'},
            'IND_REL_FCST_PRE_DOWN':{'label': 'FCST pre-↓',    'action': 'SELL', 'color': '#ef4444', 'meaning': 'Pre-forecast de bajada'},
            'IND_REL_FCST_STD':     {'label': 'FCST STD',       'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Forecast dentro de desviación estándar'},
            'IND_REL_FCST_MED':     {'label': 'FCST MED',       'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Forecast en la mediana'},
            'IND_REL_FCST_WAIT':    {'label': 'FCST WAIT',      'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Datos insuficientes para forecast'},
        }
    },
    'INDICATOR_EMA': {
        'description': 'EMA (Exponential Moving Average) — señal de cruce de EMAs.',
        'values': {
            'INDICATOR_EMA_BUY':  {'label': 'EMA BUY',  'action': 'BUY',  'color': '#22c55e', 'meaning': 'EMA rápido cruzó por encima del lento — compra'},
            'INDICATOR_EMA_SELL': {'label': 'EMA SELL', 'action': 'SELL', 'color': '#ef4444', 'meaning': 'EMA rápido cruzó por debajo del lento — venta'},
            'INDICATOR_EMA_WAIT': {'label': 'EMA WAIT', 'action': 'WAIT', 'color': '#6b7280', 'meaning': 'EMAs sin cruz — sin señal'},
        }
    },
    'INDICATOR_MED': {
        'description': 'Tendencia de momento — dirección del momento corto plazo.',
        'values': {
            'INDICATOR_TM_UP':   {'label': 'TM ↑ UP',   'action': 'BUY',  'color': '#22c55e', 'meaning': 'Momento alcista — fuerza compradora'},
            'INDICATOR_TM_DOWN': {'label': 'TM ↓ DOWN', 'action': 'SELL', 'color': '#ef4444', 'meaning': 'Momento bajista — fuerza vendedora'},
            'INDICATOR_TM_WAIT': {'label': 'TM → WAIT', 'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Momento neutral'},
            'INDICATOR_TM_UNDEF':{'label': 'TM ? UNDEF', 'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Momento no definido'},
        }
    },
    'MOTION': {
        'description': 'Movimiento del precio —加速度 del precio.',
        'values': {
            'UP':    {'label': '↑ UP',    'action': 'BUY',  'color': '#22c55e', 'meaning': 'Precio acelerando al alza'},
            'DOWN':  {'label': '↓ DOWN',  'action': 'SELL', 'color': '#ef4444', 'meaning': 'Precio acelerando a la baja'},
            'FLAT':  {'label': '→ FLAT',  'action': 'WAIT', 'color': '#6b7280', 'meaning': 'Precio sin movimiento'},
        }
    },
}


def get_indicator_stats():
    """Usage stats for each indicator value in the DB"""
    conn = _db()
    cur = conn.cursor()
    result = {}
    for field in ['INDICATOR', 'IMA_NEW', 'DIRECTION', 'TENDENCE', 'MARKET_TENDENCE', 'WEEK_FLOW', 'REL_FCST', 'INDICATOR_EMA', 'MOTION']:
        cur.execute(f"""
            SELECT {field}, COUNT(*) as cnt
            FROM MARKET
            WHERE {field} IS NOT NULL
            GROUP BY {field}
            ORDER BY cnt DESC
        """)
        result[field] = [{'value': r[0], 'count': r[1]} for r in cur.fetchall()]
    conn.close()
    return result


def get_assets_docs():
    """Documentación de todos los activos"""
    close_actions = "'CLOSE','CLOSE-BUY','CLOSE-SELL'"
    today = date.today()
    month_start = date(today.year, today.month, 1)

    conn = _db()
    cur = conn.cursor()

    cur.execute(f"""
        SELECT
            NAME as symbol,
            MIN(DATEVALUE) as first_seen,
            MAX(DATEVALUE) as last_seen,
            COUNT(*) as total_rows,
            COUNT(DISTINCT EVAL_NAME) as evaluators_used,
            SUM(CASE WHEN ACTION IN ({close_actions}) THEN 1 ELSE 0 END) as close_ops,
            SUM(CASE WHEN ACTION IN ({close_actions}) AND DATE(DATEVALUE) >= '{month_start}' THEN 1 ELSE 0 END) as month_ops,
            SUM(CASE WHEN ACTION IN ({close_actions}) THEN REVENUE ELSE 0 END) as total_pnl,
            SUM(CASE WHEN ACTION IN ({close_actions}) AND DATE(DATEVALUE) >= '{month_start}' THEN REVENUE ELSE 0 END) as month_pnl,
            MIN(VALUE) as min_price,
            MAX(VALUE) as max_price,
            (SELECT EVAL_NAME FROM MARKET M2
             WHERE M2.NAME = MARKET.NAME AND ACTION IN ({close_actions})
             GROUP BY EVAL_NAME ORDER BY SUM(REVENUE) DESC LIMIT 1) as best_evaluator
        FROM MARKET
        GROUP BY NAME
        ORDER BY NAME
    """)
    rows = cur.fetchall()
    conn.close()

    crypto = ['BTCUSD', 'ETHUSD']
    tech   = ['AAPL', 'AMD', 'AMZN', 'GOOG', 'META', 'MSFT', 'NVDA', 'TSLA', 'INTC', 'NFLX']

    docs = []
    for r in rows:
        sym = r[0]
        if sym in crypto:
            atype = 'crypto'
        elif sym in tech:
            atype = 'tech'
        elif sym in ['GLD', 'VTI']:
            atype = 'etf'
        elif sym in ['KO', 'MCD', 'SBUX', 'HD', 'DIS']:
            atype = 'consumer'
        else:
            atype = 'other'
        docs.append({
            'symbol': sym,
            'asset_type': atype,
            'first_seen': r[1],
            'last_seen': r[2],
            'total_rows': r[3],
            'evaluators_used': r[4],
            'close_ops': r[5],
            'month_ops': r[6],
            'total_pnl': round(r[7], 2),
            'month_pnl': round(r[8], 2),
            'min_price': round(r[9], 4) if r[9] else None,
            'max_price': round(r[10], 4) if r[10] else None,
            'best_evaluator': r[11],
        })
    return docs


def get_system_docs():
    """Documentación general del sistema"""
    conn = _db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM CONTROL")
    control = cur.fetchall()
    cur.execute("SELECT * FROM CONTROLMINMAX")
    minmax = cur.fetchall()
    conn.close()
    return {'control': control, 'minmax': minmax}