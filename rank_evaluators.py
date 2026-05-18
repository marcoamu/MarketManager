#!/usr/bin/env python3
"""
Evaluator Ranker — Backtest de evaluadores sobre datos históricos
================================================================
Ejecuta cada evaluador de prepareActivesEvaluatorsONLYUPNEW sobre un rango
de fechas histórico y devuelve P&L por evaluador.

Uso:
  cd /home/MarketManager
  ./venv/bin/python3 rank_evaluators.py --asset INTC --days 7
  ./venv/bin/python3 rank_evaluators.py --all --days 7
"""

import sys, os, argparse
sys.path.insert(0, '/home/MarketManager')
os.environ['DISPLAY'] = ':99'

import importlib.util
from datetime import datetime, timedelta
from service.ActiveHelper import ActiveHelper

# ── helpers ─────────────────────────────────────────────────────────────────

def load_mm():
    spec = importlib.util.spec_from_file_location(
        "MarketManager", "/home/MarketManager/MarketManager.py"
    )
    mm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mm)
    return mm

def run_backtest_for_evaluators(mm_module, activeHelper, asset_name, start, end, limit=None):
    """Ejecuta todos los evaluadores de ONLYUPNEW para un asset en modo simulación."""
    
    # preparar el activo
    prepare_map = {
        'AAPL':  'prepareAAPL',
        'TSLA':  'prepareTSLA',
        'INTC':  'prepareINTC',
        'AMZN':  'prepareAMZN',
        'MSFT':  'prepareMSFT',
        'NVDA':  'prepareNVDA',
        'NFLX':  'prepareNFLX',
        'GOOG':  'prepareGOOG',
        'BTC':   'prepareBTC',
        'ETH':   'prepareETH',
        'AMD':   'prepareAMD',
        'MCD':   'prepareMCD',
        'KO':    'prepareKO',
        'DIS':   'prepareDIS',
        'BABA':  'prepareBABA',
        'VTI':   'prepareVTI',
        'HD':    'prepareHD',
        'SBUX':  'prepareSBUX',
        'META':  'prepareMETA',
        'SONY':  'prepareSONY',
        'GLD':   'prepareGLD',
    }
    
    # Normalize name
    asset_key = asset_name.upper()
    if asset_key == 'BTCUSD': asset_key = 'BTC'
    if asset_key == 'ETHUSD': asset_key = 'ETH'
    
    if asset_key not in prepare_map:
        return [], f"Unknown asset: {asset_name} (try: {', '.join(prepare_map.keys())})"
    
    prepare_method = getattr(activeHelper, prepare_map[asset_key])
    active = prepare_method()
    
    # Solo los de ONLYUPNEW
    activesList = activeHelper.prepareActivesEvaluatorsONLYUPNEW(active)
    
    if limit:
        activesList = activesList[:limit]
    
    MarketManager = mm_module.MarketManager
    
    marketService = MarketManager(
        simulation=True,
        isDBData=True,
        useConfig=True,
        start=start,
        end=end,
        showLog=False,
        disableInitPROB=False,
        disableCloseEndRevenue=False,
    )
    
    results = []
    for x in activesList:
        try:
            totalBuy, totalSell = marketService.simulateFlowConfigReview(
                x, start, end, draw=False
            )
            total = float(totalBuy + totalSell)
            results.append({
                'evaluator': x.evaluator.name,
                'total_buy': totalBuy,
                'total_sell': totalSell,
                'total': total,
                'asset': asset_name.upper(),
            })
        except Exception as e:
            results.append({
                'evaluator': x.evaluator.name,
                'total_buy': 0,
                'total_sell': 0,
                'total': 0,
                'asset': asset_name.upper(),
                'error': str(e),
            })
    
    return results, None


def main():
    parser = argparse.ArgumentParser(description='Rank evaluators via backtest')
    parser.add_argument('--asset', type=str, default='INTC', help='Asset a testear (ej: INTC, TSLA, AAPL...)')
    parser.add_argument('--days', type=int, default=7, help='Días hacia atrás para backtest')
    parser.add_argument('--limit', type=int, default=None, help='Limitar a N evaluadores (para pruebas rápidas)')
    parser.add_argument('--all', action='store_true', help='Correr para todos los assets principales')
    parser.add_argument('--output', type=str, default=None, help='Guardar JSON en fichero')
    args = parser.parse_args()
    
    print(f"📊 Evaluator Ranker — Backtest")
    print(f"   Días: {args.days}")
    print(f"   Asset: {args.asset if not args.all else 'TODOS'}")
    print()
    
    # Load MarketManager lazily
    print("Cargando MarketManager...")
    mm = load_mm()
    activeHelper = mm.ActiveHelper(simulation=True, isDBData=True)
    
    end = datetime.now().strftime('%Y-%m-%d')
    start_dt = datetime.now() - timedelta(days=args.days)
    start = start_dt.strftime('%Y-%m-%d')
    
    all_results = []
    assets_to_test = []
    
    if args.all:
        assets_to_test = ['AAPL', 'TSLA', 'INTC', 'AMZN', 'MSFT', 'NVDA', 'NFLX', 'GOOG', 'AMD', 'MCD', 'KO', 'DIS', 'BABA', 'SBUX', 'META', 'SONY', 'HD', 'VTI', 'GLD']
    else:
        assets_to_test = [args.asset]
    
    for asset in assets_to_test:
        print(f"\n⏳ Evaluando {asset} ({start} → {end})...")
        results, err = run_backtest_for_evaluators(mm, activeHelper, asset, start, end, args.limit)
        if err:
            print(f"  ❌ {err}")
            continue
        print(f"  ✅ {len(results)} evaluadores evaluados")
        for r in results[:3]:
            print(f"     {r['evaluator'][:45]:45} TOTAL={r['total']:+.2f}")
        all_results.extend(results)
    
    # ── Ranking global ──
    print(f"\n{'='*70}")
    print(f"📈 RANKING GLOBAL (todos los assets)")
    print(f"{'='*70}")
    
    # Agrupar por evaluador
    from collections import defaultdict
    by_eval = defaultdict(lambda: {'total': 0, 'count': 0, 'wins': 0, 'losses': 0, 'assets': []})
    
    for r in all_results:
        if 'error' in r:
            continue
        name = r['evaluator']
        by_eval[name]['total'] += r['total']
        by_eval[name]['count'] += 1
        by_eval[name]['assets'].append(r['asset'])
        if r['total'] > 0:
            by_eval[name]['wins'] += 1
        elif r['total'] < 0:
            by_eval[name]['losses'] += 1
    
    ranking = sorted(
        [{'evaluator': k, **v} for k, v in by_eval.items()],
        key=lambda x: x['total'],
        reverse=True
    )
    
    print(f"\n{'Rank':<4} {'Evaluator':<50} {'Total':>10} {'W':>4} {'L':>4} {'Assets'}")
    print(f"{'-'*4} {'-'*50} {'-'*10} {'-'*4} {'-'*4} {'-'*10}")
    for i, r in enumerate(ranking, 1):
        wr = r['wins'] / (r['wins'] + r['losses']) * 100 if (r['wins'] + r['losses']) > 0 else 0
        print(f"{i:<4} {r['evaluator']:<50} {r['total']:>+10.2f} {r['wins']:>4} {r['losses']:>4} {r['count']} ({', '.join(set(r['assets']))})")
    
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump({'ranking': ranking, 'all_results': all_results, 'params': {
                'days': args.days, 'start': start, 'end': end, 'assets': assets_to_test
            }}, f, indent=2)
        print(f"\n💾 Guardado en {args.output}")
    
    return ranking, all_results


if __name__ == '__main__':
    main()