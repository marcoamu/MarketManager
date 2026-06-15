#!/usr/bin/env python3
"""
Control Optimizer - Encuentra la mejor combinación de controles BUY/SELL
========================================================================
TODO: hacer que sea más general, no solo para un evaluador específico
"""

import sys
import os
import importlib.util
import json
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# CONFIGURACIÓN - Modifica estos valores en código
# ============================================================

ASSET = "AAPL"
DAYS = 60
START_STR = ""  # Si está vacío usa los últimos DAYS
END_STR = ""

# Evaluador a probar (debe tener control_buy y control_sell configurables)
EVALUATOR_NAME = "EvaluatorEMA_LONG_03"

# Lista de controles BUY a probar (reducida para no hacer 1000+ combinaciones)
BUY_CONTROLS = [
    "control_BUY_EMA_01",
    "control_BUY_EMA_02",
    "control_BUY_EMA_03",
    "control_BUY_BLG_01",
    "control_BUY_BLG_02",
    "control_BUY_EMA_OUP_01",
    "control_BUY_EMA_OUP_02",
    "control_BUY_WEEK_01",
]

# Lista de controles SELL a probar
SELL_CONTROLS = [
    "control_SELL_EMA_01",
    "control_SELL_EMA_02",
    "control_SELL_BLG_01",
    "control_SELL_BLG_02",
    "control_SELL_BLG_03",
    "control_SELL_EMA_WEEK_01",
    "control_SELL_EMA_WEEK_02",
    "control_SELL_EMA_WEEK_03",
]

PARALLEL = False
WORKERS = 8
SAVE_JSON = True
JSON_PATH = "/tmp/control_optimizer_results.json"


def run_evaluator_with_controls(args):
    """Ejecuta un evaluador con controles específicos y retorna el resultado."""
    evaluator_class, control_buy_name, control_sell_name, start_str, end_str, mm_path, asset = args

    try:
        spec = importlib.util.spec_from_file_location("MarketManager", mm_path)
        mm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mm)

        # Crear instancia del evaluador
        evaluator = evaluator_class()
        
        # Verificar que el evaluador tenga atributos configurables
        if not hasattr(evaluator, 'control_buy') or not hasattr(evaluator, 'control_sell'):
            return {
                'control_buy': control_buy_name,
                'control_sell': control_sell_name,
                'error': 'Evaluador no tiene controles configurables'
            }
        
        # Verificar que los controles existan
        if not hasattr(evaluator, control_buy_name):
            return {
                'control_buy': control_buy_name,
                'control_sell': control_sell_name,
                'error': f'Control BUY {control_buy_name} no encontrado'
            }
        if not hasattr(evaluator, control_sell_name):
            return {
                'control_buy': control_buy_name,
                'control_sell': control_sell_name,
                'error': f'Control SELL {control_sell_name} no encontrado'
            }
        
        # Asignar los controles configurables
        evaluator.control_buy = control_buy_name
        evaluator.control_sell = control_sell_name
        
        # Crear MarketManager
        ms = mm.MarketManager(
            simulation=True,
            isDBData=True,
            useConfig=True,
            showLog=False,
            disableInitPROB=True,
            disableCloseEndRevenue=True,
        )
        
        # Obtener el activo
        activeHelper = mm.ActiveHelper(simulation=True, isDBData=True)
        prepare_map = {
            'AAPL': 'prepareAAPL', 'TSLA': 'prepareTSLA', 'INTC': 'prepareINTC',
            'BTC': 'prepareBTC', 'ETH': 'prepareETH', 'SPY': 'prepareSPY',
            'QQQ': 'prepareQQQ', 'META': 'prepareMETA', 'NVDA': 'prepareNVDA',
            'AMD': 'prepareAMD', 'AMZN': 'prepareAMZN', 'GOOGL': 'prepareGOOGL',
            'MSFT': 'prepareMSFT', 'NFLX': 'prepareNFLX', 'DIS': 'prepareDIS',
            'PYPL': 'preparePYPL', 'ADBE': 'prepareADBE', 'CMCSA': 'prepareCMCSA',
        }
        
        if asset not in prepare_map:
            return {
                'control_buy': control_buy_name,
                'control_sell': control_sell_name,
                'error': f'Asset {asset} no reconocido'
            }
        
        prepare_fn = getattr(activeHelper, prepare_map[asset])
        parameters = prepare_fn()
        
        # Crear el Active con el evaluador configurado
        active_item = mm.Active(parameters, evaluator)
        
        # Ejecutar simulación
        totalBuy, totalSell = ms.simulateFlowConfigReview(
            active_item, start_str, end_str, draw=False, isDBData=True, prepareExcel=False
        )
        total = float(totalBuy + totalSell)
        
        return {
            'control_buy': control_buy_name,
            'control_sell': control_sell_name,
            'buy': float(totalBuy),
            'sell': float(totalSell),
            'total': total,
            'trades': 0,
        }
        
    except Exception as e:
        return {
            'control_buy': control_buy_name,
            'control_sell': control_sell_name,
            'buy': 0.0,
            'sell': 0.0,
            'total': 0.0,
            'error': str(e)[:200]
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
    
    print("=" * 90)
    print(" CONTROL OPTIMIZER - Encuentra la mejor combinación BUY/SELL")
    print("=" * 90)
    print(f"  Evaluador: {EVALUATOR_NAME}")
    print(f"  Asset: {ASSET}")
    print(f"  Período: {start_str} → {end_str} ({DAYS} días)")
    print(f"  Controles BUY: {len(BUY_CONTROLS)} → {BUY_CONTROLS}")
    print(f"  Controles SELL: {len(SELL_CONTROLS)} → {SELL_CONTROLS}")
    print(f"  Combinaciones: {len(BUY_CONTROLS) * len(SELL_CONTROLS)}")
    print("=" * 90)
    print()
    
    # Cargar el evaluador
    evaluators_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evaluators")
    sys.path.insert(0, evaluators_dir)
    
    try:
        evaluator_module = importlib.import_module(EVALUATOR_NAME)
        evaluator_class = getattr(evaluator_module, EVALUATOR_NAME)
    except (ImportError, AttributeError) as e:
        print(f"ERROR: No se pudo cargar el evaluador {EVALUATOR_NAME}: {e}")
        return
    
    # Generar todas las combinaciones
    combinations = [(b, s) for b in BUY_CONTROLS for s in SELL_CONTROLS]
    print(f"Probando {len(combinations)} combinaciones...")
    print()
    
    mm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MarketManager.py")
    
    # Preparar tareas
    tasks = [
        (evaluator_class, b, s, start_str, end_str, mm_path, ASSET)
        for b, s in combinations
    ]
    
    results = []
    
    if PARALLEL:
        from multiprocessing import Pool
        print(f"Ejecutando en paralelo ({WORKERS} workers)...")
        with Pool(WORKERS) as pool:
            results = pool.map(run_evaluator_with_controls, tasks)
    else:
        print("Ejecutando secuencial...")
        for i, task in enumerate(tasks):
            r = run_evaluator_with_controls(task)
            results.append(r)
            status = "✅" if 'error' not in r else "❌"
            pct = (i+1) * 100 // len(tasks)
            print(f"  [{i+1:2d}/{len(tasks)}] {status} {pct:3d}% | {task[1]} + {task[2]}: total={r.get('total', 0):.2f}")
    
    # Ordenar por total descendente
    results.sort(key=lambda x: x.get('total', 0), reverse=True)
    
    # Filtrar
    errors = [r for r in results if 'error' in r]
    valid_results = [r for r in results if 'error' not in r]
    
    # ============================================================
    # RESULTADOS
    # ============================================================
    print()
    print("=" * 90)
    print(" 🥇 TOP 10 MEJORES COMBINACIONES")
    print("=" * 90)
    print(f" {'Rank':<5} {'BUY Control':<25} {'SELL Control':<25} {'Total':>10} {'Buy':>10} {'Sell':>10}")
    print("-" * 90)
    
    for i, r in enumerate(valid_results[:10], 1):
        print(f" {i:<5} {r['control_buy']:<25} {r['control_sell']:<25} {r['total']:>10.2f} {r['buy']:>10.2f} {r['sell']:>10.2f}")
    
    print()
    print("=" * 90)
    print(" 🏁 TOP 10 PEORES COMBINACIONES")
    print("=" * 90)
    print(f" {'Rank':<5} {'BUY Control':<25} {'SELL Control':<25} {'Total':>10} {'Buy':>10} {'Sell':>10}")
    print("-" * 90)
    
    for i, r in enumerate(valid_results[-10:][::-1], 1):
        print(f" {i:<5} {r['control_buy']:<25} {r['control_sell']:<25} {r['total']:>10.2f} {r['buy']:>10.2f} {r['sell']:>10.2f}")
    
    if errors:
        print()
        print(f"⚠️  Errores: {len(errors)}")
        for e in errors[:5]:
            print(f"    {e['control_buy']} + {e['control_sell']}: {e.get('error', 'Unknown')}")
    
    # ============================================================
    # RESUMEN
    # ============================================================
    print()
    print("=" * 90)
    print(" 📊 RESUMEN")
    print("=" * 90)
    
    if valid_results:
        totals = [r['total'] for r in valid_results]
        winners = [r for r in valid_results if r['total'] > 0]
        losers = [r for r in valid_results if r['total'] < 0]
        
        print(f"  Combinaciones probadas: {len(valid_results)}")
        print(f"  Ganadores (>0): {len(winners)} ({len(winners)*100//len(valid_results)}%)")
        print(f"  Perdedores (<0): {len(losers)} ({len(losers)*100//len(valid_results)}%)")
        print(f"  Media: {sum(totals)/len(totals):.2f}")
        print()
        
        best = valid_results[0]
        worst = valid_results[-1]
        
        print(f"  🏆 MEJOR: {best['total']:.2f}")
        print(f"     BUY:  {best['control_buy']}")
        print(f"     SELL: {best['control_sell']}")
        print()
        print(f"  💩 PEOR: {worst['total']:.2f}")
        print(f"     BUY:  {worst['control_buy']}")
        print(f"     SELL: {worst['control_sell']}")
    
    # Guardar JSON
    if SAVE_JSON:
        output_data = {
            'evaluator': EVALUATOR_NAME,
            'asset': ASSET,
            'days': DAYS,
            'start_date': start_str,
            'end_date': end_str,
            'buy_controls_tested': BUY_CONTROLS,
            'sell_controls_tested': SELL_CONTROLS,
            'results': valid_results,
            'errors': errors,
            'timestamp': datetime.now().isoformat(),
            'best_combination': {
                'control_buy': valid_results[0]['control_buy'],
                'control_sell': valid_results[0]['control_sell'],
                'total': valid_results[0]['total'],
                'buy': valid_results[0]['buy'],
                'sell': valid_results[0]['sell'],
            } if valid_results else None
        }
        with open(JSON_PATH, 'w') as f:
            json.dump(output_data, f, indent=2)
        print()
        print(f"  💾 JSON guardado: {JSON_PATH}")
    
    print("=" * 90)


if __name__ == "__main__":
    main()