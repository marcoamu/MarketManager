import sqlite3
from datetime import datetime, timedelta, date

def _get_db():
    return sqlite3.connect('/home/MarketManager/market.db')

# ─── Per-asset evaluator breakdown ───────────────────────────────────────────

def get_asset_evaluator_detail(symbol):
    """All evaluators used for this asset, with P&L stats"""
    conn = _get_db()
    cur = conn.cursor()
    close_actions = "'CLOSE','CLOSE-BUY','CLOSE-SELL'"

    cur.execute(f"""
        SELECT
            EVAL_NAME,
            COUNT(*) as ops,
            COUNT(DISTINCT DATE(DATEVALUE)) as trading_days,
            SUM(REVENUE) as total_pnl,
            AVG(REVENUE) as avg_pnl,
            MIN(DATEVALUE) as first_seen,
            MAX(DATEVALUE) as last_seen
        FROM MARKET
        WHERE NAME = ?
        AND EVAL_NAME IS NOT NULL
        AND ACTION IN ({close_actions})
        GROUP BY EVAL_NAME
        ORDER BY total_pnl DESC
    """, (symbol.upper(),))
    rows = cur.fetchall()
    conn.close()
    return [{
        'evaluator': r[0],
        'ops': r[1],
        'trading_days': r[2],
        'total_pnl': round(r[3], 2),
        'avg_pnl': round(r[4], 4),
        'first_seen': r[5],
        'last_seen': r[6],
    } for r in rows]

def get_asset_signal_history(symbol):
    """Latest signal/indicator values for an asset"""
    conn = _get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT DATEVALUE, ACTION, DIRECTION, TENDENCE, MARKET_TENDENCE,
               IMA_NEW, INDICATOR, REVENUE, PROFIT, ANGLE, REL_FCST,
               WEEK_FLOW, WEEK_DIR, CLOSE_NXT_UP, CLOSE_NXT_DOWN,
               ANGLE_IMA, MOTION, QTY
        FROM MARKET
        WHERE NAME = ?
        ORDER BY DATEVALUE DESC
        LIMIT 20
    """, (symbol.upper(),))
    rows = cur.fetchall()
    conn.close()
    return [{
        'datetime': r[0],
        'action': r[1],
        'direction': r[2],
        'tendencie': r[3],
        'market_tendencie': r[4],
        'ima_new': r[5],
        'indicator': r[6],
        'revenue': round(r[7], 4) if r[7] is not None else None,
        'profit': round(r[8], 4) if r[8] is not None else None,
        'angle': r[9],
        'rel_fcst': r[10],
        'week_flow': r[11],
        'week_dir': r[12],
        'close_nxt_up': r[13],
        'close_nxt_down': r[14],
        'angle_ima': r[15],
        'motion': r[16],
        'qty': r[17],
    } for r in rows]

def get_asset_daily_detail(symbol):
    """Daily aggregated P&L for an asset, with evaluator breakdown"""
    conn = _get_db()
    cur = conn.cursor()
    close_actions = "'CLOSE','CLOSE-BUY','CLOSE-SELL'"

    cur.execute(f"""
        SELECT
            DATE(DATEVALUE) as day,
            EVAL_NAME,
            COUNT(*) as ops,
            SUM(REVENUE) as pnl,
            AVG(REVENUE) as avg_pnl,
            MIN(VALUE) as min_price,
            MAX(VALUE) as max_price
        FROM MARKET
        WHERE NAME = ?
        AND ACTION IN ({close_actions})
        GROUP BY DATE(DATEVALUE), EVAL_NAME
        ORDER BY day DESC, pnl DESC
    """, (symbol.upper(),))
    rows = cur.fetchall()
    conn.close()

    days = {}
    for r in rows:
        day = r[0]
        if day not in days:
            days[day] = {'day': day, 'total_pnl': 0, 'ops': 0, 'evaluators': []}
        days[day]['total_pnl'] += r[4]
        days[day]['ops'] += r[2]
        days[day]['evaluators'].append({
            'evaluator': r[1],
            'ops': r[2],
            'pnl': round(r[4], 2),
            'avg_pnl': round(r[5], 4),
        })
    for d in days.values():
        d['total_pnl'] = round(d['total_pnl'], 2)
    return sorted(days.values(), key=lambda x: x['day'], reverse=True)

def get_global_evaluator_ranking():
    """Ranking of all evaluators by total P&L"""
    conn = _get_db()
    cur = conn.cursor()
    close_actions = "'CLOSE','CLOSE-BUY','CLOSE-SELL'"

    cur.execute(f"""
        SELECT
            EVAL_NAME,
            COUNT(*) as total_ops,
            COUNT(DISTINCT NAME) as assets,
            SUM(REVENUE) as total_pnl,
            AVG(REVENUE) as avg_pnl,
            MIN(DATEVALUE) as first_seen,
            MAX(DATEVALUE) as last_seen
        FROM MARKET
        WHERE EVAL_NAME IS NOT NULL AND ACTION IN ({close_actions})
        GROUP BY EVAL_NAME
        ORDER BY total_pnl DESC
    """)
    rows = cur.fetchall()
    conn.close()

    result = []
    cumulative = 0
    for r in rows:
        cumulative += r[3]
        result.append({
            'evaluator': r[0],
            'total_ops': r[1],
            'assets': r[2],
            'total_pnl': round(r[3], 2),
            'avg_pnl': round(r[4], 4),
            'cumulative_pnl': round(cumulative, 2),
            'first_seen': r[5],
            'last_seen': r[6],
        })
    return result

def get_worst_assets_by_evaluator():
    """Assets that are in loss — grouped by evaluator"""
    conn = _get_db()
    cur = conn.cursor()
    close_actions = "'CLOSE','CLOSE-BUY','CLOSE-SELL'"

    cur.execute(f"""
        SELECT
            NAME as symbol,
            EVAL_NAME,
            COUNT(*) as ops,
            SUM(REVENUE) as total_pnl,
            AVG(REVENUE) as avg_pnl,
            MIN(VALUE) as entry_min,
            MAX(VALUE) as entry_max
        FROM MARKET
        WHERE EVAL_NAME IS NOT NULL
        AND ACTION IN ({close_actions})
        GROUP BY NAME, EVAL_NAME
        HAVING SUM(REVENUE) < 0 AND COUNT(*) >= 3
        ORDER BY total_pnl ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return [{
        'symbol': r[0],
        'evaluator': r[1],
        'ops': r[2],
        'total_pnl': round(r[3], 2),
        'avg_pnl': round(r[4], 4),
        'entry_min': round(r[5], 4),
        'entry_max': round(r[6], 4),
    } for r in rows]

def get_asset_current_signals(symbol):
    """Most recent signal state for an asset"""
    conn = _get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT TENDENCE, MARKET_TENDENCE, DIRECTION, IMA_NEW, INDICATOR,
               ANGLE, ANGLE_IMA, REL_FCST, WEEK_FLOW, WEEK_DIR,
               CLOSE_NXT_UP, CLOSE_NXT_DOWN, MOTION,
               ACTION_COUNT, ACTION_ACUM, CHANGE_ACTION
        FROM MARKET
        WHERE NAME = ?
        ORDER BY DATEVALUE DESC
        LIMIT 1
    """, (symbol.upper(),))
    row = cur.fetchone()
    conn.close()
    if not row:
        return {}
    keys = ['tendencie','market_tendencie','direction','ima_new','indicator',
            'angle','angle_ima','rel_fcst','week_flow','week_dir',
            'close_nxt_up','close_nxt_down','motion','action_count','action_acum','change_action']
    return dict(zip(keys, row))

def get_assets_with_pnl_summary():
    """All assets with their P&L for current month"""
    conn = _get_db()
    cur = conn.cursor()
    close_actions = "'CLOSE','CLOSE-BUY','CLOSE-SELL'"
    today = date.today()
    month_start = date(today.year, today.month, 1)

    cur.execute(f"""
        SELECT
            NAME as symbol,
            SUM(CASE WHEN DATE(DATEVALUE) >= '{month_start}' THEN REVENUE ELSE 0 END) as month_pnl,
            SUM(REVENUE) as total_pnl,
            COUNT(CASE WHEN DATE(DATEVALUE) >= '{month_start}' THEN 1 END) as month_ops,
            COUNT(*) as total_ops,
            COUNT(DISTINCT EVAL_NAME) as evaluators_used,
            (SELECT EVAL_NAME FROM MARKET M2
             WHERE M2.NAME = MARKET.NAME AND ACTION IN ({close_actions})
             GROUP BY EVAL_NAME ORDER BY SUM(REVENUE) DESC LIMIT 1) as best_evaluator
        FROM MARKET
        WHERE ACTION IN ({close_actions})
        GROUP BY NAME
        ORDER BY month_pnl ASC
    """)
    rows = cur.fetchall()
    conn.close()
    return [{
        'symbol': r[0],
        'month_pnl': round(r[1], 2),
        'total_pnl': round(r[2], 2),
        'month_ops': r[3],
        'total_ops': r[4],
        'evaluators_used': r[5],
        'best_evaluator': r[6],
    } for r in rows]