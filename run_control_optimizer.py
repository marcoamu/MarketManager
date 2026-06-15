#!/usr/bin/env python3
"""
Control Optimizer v2 - Usa atributos configurables del evaluador
================================================================
Usage:
    python3 run_control_optimizer.py EvaluatorEMA_LONG_03
    python3 run_control_optimizer.py EvaluatorEMA_LONG_03 --days 30 --asset AAPL
    python3 run_control_optimizer.py EvaluatorEMA_LONG_03 --buy-controls control_BUY_EMA_02 control_BUY_EMA_03
    python3 run_control_optimizer.py EvaluatorEMA_LONG_03 --sell-controls control_SELL_EMA_01 control_SELL_BLG_01
"""

import sys
import os
import importlib.util
import json
import argparse
from datetime import datetime, timedelta
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# CONFIGURACIÓN
# ============================================================
START_STR = "2026-06-08"
END_STR = "2026-06-15"

ASSET = "INTC"
DAYS = 15
SAVE_JSON = True
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
JSON_PATH = f"f:/WORK/2026/MarketManager/OUT/evaluator_ranking_{ASSET}_{DAYS}d_{timestamp}.json"
PARALLEL = True
WORKERS = 8

# ============================================================
# CONTROLES DISPONIBLES (recolectados de CierreBase.py)
# ============================================================

CONTROL_BUY_CONTROLS = [
    "control_BUY_BLG_01",
    "control_BUY_BLG_02", 
    "control_BUY_BLG_03",
    "control_BUY_EMA_01",
    "control_BUY_EMA_02",
    "control_BUY_EMA_03",
    "control_BUY_EMA_04",
    "control_BUY_EMA_OUP_01",
    "control_BUY_EMA_OUP_02",
    "control_BUY_EMA_OUP_03",
    "control_BUY_EMA_OUP_04",
    "control_BUY_WEEK_01",
    "control_BUY_WEEK_02",
    "control_BUY_WEEK_03",
    "control_BUY_WEEK_04",
    "control_BUY_WEEK_NEW_DIFF_01",
    "control_BUY_WEEK_NEW_DIFF_02",
    "control_BUY_WEEK_NEW_DIFF_03",
    "control_BUY_RSI_01",
    "control_BUY_START_CLOSE_01",
    "control_BUY_START_CLOSE_03",
    "control_BUY_START_CLOSE_04",
    "control_BUY_START_CLOSE_05",
    "control_BUY_BLG_MID_01",
    "control_BUY_BLG_MID_02",
    "control_BUY_BLG_MID_03",
    "control_BUY_BLG_MID_04",
    "control_BUY_BLG_LONG_01",
    "control_BUY_BLG_LONG_02",
    "control_BUY_IMA1_01",
    "control_BUY_IMA_02",
    "control_BUY_LONG_ONLYUP_01",
    "control_BUY_LONG_ONLYUP_02",
    "control_BUY_LONG_ONLYUP_05",
]

CONTROL_SELL_CONTROLS = [
    "control_SELL_BLG_01",
    "control_SELL_BLG_02",
    "control_SELL_BLG_03",
    "control_SELL_EMA_01",
    "control_SELL_EMA_02",
    "control_SELL_EMA_WEEK_01",
    "control_SELL_EMA_WEEK_02",
    "control_SELL_EMA_WEEK_03",
    "control_SELL_EMA_WEEK_04",
    "control_SELL_EMA_WEEK_05",
    "control_SELL_EMA_WEEK_NEW_FLOW_01",
    "control_SELL_EMA_WEEK_NEW_FLOW_02",
    "control_SELL_EMA_WEEK_NEW_FLOW_03",
    "control_SELL_EMA_WEEK_NEW_FLOW_04",
    "control_SELL_RSI_01",
    "control_SELL_START_CLOSE_01",
    "control_SELL_START_CLOSE_02",
    "control_SELL_BLG_MID_01",
    "control_SELL_BLG_MID_02",
    "control_SELL_BLG_LONG_01",
    "control_SELL_BLG_LONG_02",
    "control_SELL_BLG_LONG_03",
    "control_SELL_BLG_LONG_04",
    "control_SELL_IMA1_01",
    "control_SELL_IMA1_02",
]


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
                'error': 'Evaluador no tiene controles configurables (control_buy/control_sell)'
            }
        
        # Verificar que los controles existan en CierreBase
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
        
        # Crear MarketManager y ejecutar
        ms = mm.MarketManager(
            simulation=True,
            isDBData=True,
            useConfig=True,
            showLog=False,
            disableInitPROB=True,
            disableCloseEndRevenue=True,
        )
        
        # Obtener el activo base (parameters)
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
        
        # Crear el Active con nuestros parámetros y evaluador configurado
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
        import traceback
        return {
            'control_buy': control_buy_name,
            'control_sell': control_sell_name,
            'buy': 0.0,
            'sell': 0.0,
            'total': 0.0,
            'error': str(e)[:200]
        }


def main():
    parser = argparse.ArgumentParser(description='Control Optimizer para MarketManager (v2)')
    parser.add_argument('evaluator', help='Nombre del evaluador (ej: EvaluatorEMA_LONG_03)')
    parser.add_argument('--days', type=int, default=DAYS, help=f'Días de simulación (default: {DAYS})')
    parser.add_argument('--asset', default=ASSET, help=f'Asset a simular (default: {ASSET})')
    parser.add_argument('--buy-controls', nargs='+', help='Lista de controles BUY a probar')
    parser.add_argument('--sell-controls', nargs='+', help='Lista de controles SELL a probar')
    parser.add_argument('--top', type=int, default=20, help='Top N resultados a mostrar')
    parser.add_argument('--parallel', action='store_true', help='Ejecutar en paralelo')
    parser.add_argument('--workers', type=int, default=WORKERS, help=f'Workers para paralelo (default: {WORKERS})')
    parser.add_argument('--output', default=JSON_PATH, help=f'Archivo de salida JSON (default: {JSON_PATH})')


    if not START_STR or not END_STR:
        end = datetime.now()
        start = end - timedelta(days=DAYS)
        start_str = start.strftime('%Y-%m-%d')
        end_str = end.strftime('%Y-%m-%d')
    else:
        start_str = START_STR
        end_str = END_STR
        
    args = parser.parse_args()
    
    # Calcular fechas
    end = datetime.now()
    start = end - timedelta(days=args.days)
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')
    
    # Cargar el evaluador dinámicamente
    evaluators_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evaluators")
    sys.path.insert(0, evaluators_dir)
    
    try:
        evaluator_module = importlib.import_module(args.evaluator)
        evaluator_class = getattr(evaluator_module, args.evaluator)
    except (ImportError, AttributeError) as e:
        print(f"ERROR: No se pudo cargar el evaluador {args.evaluator}: {e}")
        return
    
    # Determinar controles a probar
    buy_controls = args.buy_controls if args.buy_controls else CONTROL_BUY_CONTROLS
    sell_controls = args.sell_controls if args.sell_controls else CONTROL_SELL_CONTROLS
    
    print(f"=== Control Optimizer v2 ===")
    print(f"Evaluador: {args.evaluator}")
    print(f"Asset: {args.asset}")
    print(f"Días: {args.days} ({start_str} → {end_str})")
    print(f"Controles BUY: {len(buy_controls)}")
    print(f"Controles SELL: {len(sell_controls)}")
    print(f"Combinaciones totales: {len(buy_controls) * len(sell_controls)}")
    print(f"Paralelo: {args.parallel} ({args.workers} workers)" if args.parallel else "")
    print()
    
    # Generar todas las combinaciones
    combinations = [(b, s) for b in buy_controls for s in sell_controls]
    print(f"Generando {len(combinations)} combinaciones...")
    
    mm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MarketManager.py")
    
    # Preparar tareas
    tasks = [
        (evaluator_class, b, s, start_str, end_str, mm_path, args.asset)
        for b, s in combinations
    ]
    
    results = []
    
    if args.parallel:
        print(f"Ejecutando en paralelo ({args.workers} workers)...")
        with Pool(args.workers) as pool:
            results = pool.map(run_evaluator_with_controls, tasks)
    else:
        print("Ejecutando secuencial...")
        for i, task in enumerate(tasks):
            r = run_evaluator_with_controls(task)
            results.append(r)
            status = "✅" if 'error' not in r else "❌"
            print(f"  [{i+1}/{len(tasks)}] {status} {task[1]} + {task[2]}: total={r.get('total', 0):.2f}")
    
    # Ordenar por total descendente
    results.sort(key=lambda x: x.get('total', 0), reverse=True)
    
    # Filtrar errores
    errors = [r for r in results if 'error' in r]
    valid_results = [r for r in results if 'error' not in r]
    
    print()
    print("=" * 100)
    print(f"=== TOP {args.top} COMBINACIONES ===")
    print("=" * 100)
    print(f"{'Rank':<5} {'Control BUY':<28} {'Control SELL':<28} {'Total':>10} {'Buy':>10} {'Sell':>10}")
    print("-" * 100)
    
    for i, r in enumerate(valid_results[:args.top], 1):
        print(f"{i:<5} {r['control_buy']:<28} {r['control_sell']:<28} {r['total']:>10.2f} {r['buy']:>10.2f} {r['sell']:>10.2f}")
    
    if len(valid_results) > args.top:
        print(f"  ... y {len(valid_results) - args.top} más")
    
    if errors:
        print()
        print(f"=== ERRORES ({len(errors)}) ===")
        for e in errors[:10]:
            print(f"  {e['control_buy']} + {e['control_sell']}: {e.get('error', 'Unknown')}")
    
    # Guardar JSON
    if SAVE_JSON:
        output_data = {
            'evaluator': args.evaluator,
            'asset': args.asset,
            'days': args.days,
            'start_date': start_str,
            'end_date': end_str,
            'total_combinations': len(combinations),
            'buy_controls_tested': buy_controls,
            'sell_controls_tested': sell_controls,
            'results': valid_results,
            'errors': errors,
            'timestamp': datetime.now().isoformat()
        }
        with open(args.output, 'w') as f:
            json.dump(output_data, f, indent=2)
        print()
        print(f"✅ JSON guardado: {args.output}")
    
    # Resumen
    print()
    print("=== RESUMEN ===")
    print(f"Total combinaciones probadas: {len(valid_results)}")
    if valid_results:
        totals = [r['total'] for r in valid_results]
        winners = [r for r in valid_results if r['total'] > 0]
        losers = [r for r in valid_results if r['total'] < 0]
        print(f"Ganadores (>0): {len(winners)}")
        print(f"Perdedores (<0): {len(losers)}")
        print(f"Promedio: {sum(totals)/len(totals):.2f}")
        best = valid_results[0]
        worst = valid_results[-1]
        print(f"Mejor: {best['total']:.2f} ({best['control_buy']} + {best['control_sell']})")
        print(f"Peor: {worst['total']:.2f} ({worst['control_buy']} + {worst['control_sell']})")


if __name__ == "__main__":
    main()