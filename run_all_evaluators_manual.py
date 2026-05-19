#!/usr/bin/env python3
"""
Evaluator Runner — Parametri nel codice, descomenta quello che vuoi eseguire.
======================================================================
Más fácil: descomentás la opción, corrés, listo.
"""

import sys, os, importlib.util
from datetime import datetime, timedelta
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# PARAMETERS — descomenta lo que necesites
# ============================================================

# --- ASSET y DURACIÓN ---
ASSET = "AAPL"
DAYS = 15

# --- EVALUATOR específico (opcional) ---
# Si está vacío usa TODOS los evaluadores de prepareActivesEvaluators
EVALUATOR = ""  # ej: "EvaluatorDistMarketTenOptimiz01"

# --- PARALLEL ---
PARALLEL = False
WORKERS = 8

# --- RANGO DE FECHAS ---
# Si start_str/end_str están vacíos usa los últimos DAYS
START_STR = ""
END_STR = ""

# --- OUTPUT ---
SAVE_JSON = True
JSON_PATH = f"/tmp/evaluator_ranking_{ASSET}_{DAYS}d.json"

# ============================================================
# WORKER FUNCTION (module level for pickling)
# ============================================================

def _run_single_evaluator(args):
    """Corre un active individual y devuelve resultado."""
    active_item, start_str, end_str, mm_path = args

    try:
        spec = importlib.util.spec_from_file_location("MarketManager", mm_path)
        mm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mm)

        ms = mm.MarketManager(
            simulation=True,
            isDBData=True,
            useConfig=True,
            showLog=False,
            disableInitPROB=True,
            disableCloseEndRevenue=True,
        )

        totalBuy, totalSell = ms.simulateFlowConfigReview(
            active_item, start_str, end_str, draw=False, isDBData=True, prepareExcel=False
        )
        total = float(totalBuy + totalSell)

        return {
            'evaluator': active_item.evaluator.name,
            'buy': float(totalBuy),
            'sell': float(totalSell),
            'total': total,
        }
    except Exception as e:
        return {
            'evaluator': active_item.evaluator.name,
            'buy': 0.0, 'sell': 0.0, 'total': 0.0,
            'error': str(e)[:100]
        }


def main():
    # Calcular fechas
    if not START_STR or not END_STR:
        end = datetime.now()
        start = end - timedelta(days=DAYS)
        start_str = start.strftime('%Y-%m-%d')
        end_str = end.strftime('%Y-%m-%d')
    else:
        start_str = START_STR
        end_str = END_STR

    print(f"=== Evaluator Runner ===")
    print(f"Asset: {ASSET}")
    print(f"Dias: {DAYS}")
    print(f"Fechas: {start_str} → {end_str}")
    print(f"Parallel: {PARALLEL} x {WORKERS}" if PARALLEL else "")
    print(f"Evaluador: {EVALUATOR or 'TODOS'}")
    print()

    # Importar MarketManager
    mm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MarketManager.py")
    spec = importlib.util.spec_from_file_location("MarketManager", mm_path)
    mm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mm)

    activeHelper = mm.ActiveHelper(simulation=True, isDBData=True)

    # Preparar el asset base
    prepare_map = {
        'AAPL': 'prepareAAPL', 'TSLA': 'prepareTSLA', 'INTC': 'prepareINTC',
        'BTC': 'prepareBTC', 'ETH': 'prepareETH', 'SPY': 'prepareSPY',
        'QQQ': 'prepareQQQ', 'META': 'prepareMETA', 'NVDA': 'prepareNVDA',
        'AMD': 'prepareAMD', 'AMZN': 'prepareAMZN', 'GOOGL': 'prepareGOOGL',
        'MSFT': 'prepareMSFT', 'NFLX': 'prepareNFLX', 'DIS': 'prepareDIS',
        'PYPL': 'preparePYPL', 'ADBE': 'prepareADBE', 'CMCSA': 'prepareCMCSA',
    }

    if ASSET not in prepare_map:
        print(f"ERROR: asset {ASSET} no reconocido")
        return

    prepare_fn = getattr(activeHelper, prepare_map[ASSET])
    base_active = prepare_fn()

    # Obtener lista de activos con prepareActivesEvaluators (52 evals)
    # NOTA: prepareActivesEvaluators4 está roto (falta import de EvaluatorBase)
    activesList = activeHelper.prepareActivesEvaluators(base_active)
    print(f"Total evaluadores disponibles: {len(activesList)}")

    # Filtrar por evaluador específico si aplica
    if EVALUATOR:
        activesList = [a for a in activesList if a.evaluator.name == EVALUATOR]
        print(f"Filtrado a: {len(activesList)} evaluadores")

    for a in activesList[:5]:
        print(f"  - {a.evaluator.name}")
    if len(activesList) > 5:
        print(f"  ... y {len(activesList)-5} más")
    print()

    # Construir tareas
    tasks = [(a, start_str, end_str, mm_path) for a in activesList]

    if PARALLEL:
        print(f"Corriendo en paralelo ({WORKERS} workers)...")
        with Pool(WORKERS) as pool:
            results = pool.map(_run_single_evaluator, tasks)
    else:
        print("Corriendo secuencial...")
        results = []
        for i, task in enumerate(tasks):
            r = _run_single_evaluator(task)
            results.append(r)
            print(f"  [{i+1}/{len(tasks)}] {r['evaluator']}: total={r['total']:.2f}")

    # Ordenar por total descendente
    results.sort(key=lambda x: x['total'], reverse=True)

    print()
    print("=== TOP 20 RESULTADOS ===")
    for i, r in enumerate(results[:20], 1):
        print(f"  {i:2}. {r['evaluator']:<40} total={r['total']:>10.2f}  buy={r['buy']:>8.2f}  sell={r['sell']:>8.2f}")

    if len(results) > 20:
        print(f"  ... y {len(results)-20} más")

    # Guardar JSON
    if SAVE_JSON and results:
        import json
        with open(JSON_PATH, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nJSON guardado: {JSON_PATH}")

    # Resumen
    totals = [r['total'] for r in results]
    winners = [r for r in results if r['total'] > 0]
    losers = [r for r in results if r['total'] < 0]

    print()
    print(f"Total evaluadores: {len(results)}")
    print(f"Ganadores (>0): {len(winners)}")
    print(f"Perdedores (<0): {len(losers)}")
    if totals:
        print(f"Promedio: {sum(totals)/len(totals):.2f}")
        print(f"Mejor: {max(totals):.2f} ({results[0]['evaluator']})")
        print(f"Peor: {min(totals):.2f} ({results[-1]['evaluator']})")


if __name__ == "__main__":
    main()