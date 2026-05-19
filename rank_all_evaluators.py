#!/usr/bin/env python3
"""
Evaluator Ranker v3 — ALL evaluators via prepareActivesEvaluators4
===================================================================
Evalua los 206 evaluadores (sin ONLY_UP, BTC, ETH) usando prepareActivesEvaluators4.
Útil para encontrar los mejores evaluadores para cada asset.

Uso:
  python3 rank_all_evaluators.py --asset AAPL --days 15
  python3 rank_all_evaluators.py --asset AAPL --days 15 --parallel --workers 8
  python3 rank_all_evaluators.py --all --days 15 --parallel --workers 8
"""

import sys, os, argparse, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util
from datetime import datetime, timedelta
from multiprocessing import Pool, cpu_count


def run_single_evaluator(args):
    """Una tarea: un evaluador sobre un asset."""
    asset_name, evaluator_name, preparer_method, start, end, mm_path, sim_flags = args

    try:
        spec = importlib.util.spec_from_file_location("MarketManager", mm_path)
        mm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mm)

        activeHelper = mm.ActiveHelper(simulation=True, isDBData=True)

        prepare_map = {
            'AAPL': 'prepareAAPL7', 'TSLA': 'prepareTSLA02', 'INTC': 'prepareINTC',
            'AMZN': 'prepareAMZN4', 'MSFT': 'prepareMSFT04', 'NVDA': 'prepareNVDA06',
            'NFLX': 'prepareNFLX5', 'GOOG': 'prepareGOOG5', 'BTC': 'prepareBTC3',
            'ETH': 'prepareETH2', 'AMD': 'prepareAMD06', 'MCD': 'prepareMCD02',
            'KO': 'prepareKO3', 'DIS': 'prepareDIS08', 'BABA': 'prepareBABA02',
            'VTI': 'prepareVTI02', 'HD': 'prepareHD01', 'SBUX': 'prepareSBUX',
            'META': 'prepareMETA02', 'SONY': 'prepareSONY03', 'GLD': 'prepareGLD',
        }

        norm = asset_name.upper()
        if norm == 'BTCUSD': norm = 'BTC'
        if norm == 'ETHUSD': norm = 'ETH'
        if norm not in prepare_map:
            return None

        prepare_fn = getattr(activeHelper, prepare_map[norm])
        active = prepare_fn()

        # Use prepareActivesEvaluators4 — the big one with 206 evaluators
        preparer = getattr(activeHelper, preparer_method)
        activesList = preparer(active)

        # Find target evaluator
        target = None
        for a in activesList:
            if a.evaluator.name == evaluator_name:
                target = a
                break
        if target is None:
            return None

        marketService = mm.MarketManager(
            simulation=True, isDBData=True, useConfig=True,
            start=start, end=end, showLog=False,
            evaluate=target, showAnalyze=False
        )

        marketService.process()

        result = marketService.getResult()
        if result:
            return {
                'evaluator': evaluator_name,
                'asset': asset_name,
                'pnl': result.get('pnl', 0),
                'operations': result.get('operations', 0),
                'wins': result.get('wins', 0),
                'losses': result.get('losses', 0),
                'profit_factor': result.get('profitFactor', 0),
                'sharpe': result.get('sharpe', 0),
            }
    except Exception as e:
        return {
            'evaluator': evaluator_name,
            'asset': asset_name,
            'error': str(e)[:100]
        }
    return None


def get_evaluators_list(preparer_method, mm_path):
    """Extrae la lista de evaluadores desde prepareActivesEvaluators4."""
    spec = importlib.util.spec_from_file_location("MarketManager", mm_path)
    mm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mm)

    activeHelper = mm.ActiveHelper(simulation=True, isDBData=True)

    # Use a dummy active to call the preparer
    prepare_map = {'AAPL': 'prepareAAPL'}
    prepare_fn = getattr(activeHelper, prepare_map['AAPL'])
    active = prepare_fn()
    preparer = getattr(activeHelper, preparer_method)
    activesList = preparer(active)

    return [(a.evaluator.name for a in activesList)]


def main():
    parser = argparse.ArgumentParser(description='Rank all evaluators')
    parser.add_argument('--asset', default='AAPL', help='Asset to test')
    parser.add_argument('--days', type=int, default=15, help='Days of backtest')
    parser.add_argument('--parallel', action='store_true', help='Use parallel')
    parser.add_argument('--workers', type=int, default=cpu_count(), help='Workers')
    parser.add_argument('--preparer', default='prepareActivesEvaluators4',
                        help='Method name in ActiveHelper')
    parser.add_argument('--output', help='Output JSON file')
    args = parser.parse_args()

    mm_path = os.path.join(os.path.dirname(__file__), "MarketManager.py")

    # Get evaluator list
    spec = importlib.util.spec_from_file_location("MarketManager", mm_path)
    mm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mm)

    activeHelper = mm.ActiveHelper(simulation=True, isDBData=True)
    prepare_map = {'AAPL': 'prepareAAPL'}
    prepare_fn = getattr(activeHelper, prepare_map['AAPL'])
    active = prepare_fn()
    preparer = getattr(activeHelper, args.preparer)
    activesList = preparer(active)

    evaluator_names = [a.evaluator.name for a in activesList]
    print(f"Preparer: {args.preparer} → {len(evaluator_names)} evaluadores")

    # Date range
    end = datetime.now()
    start = end - timedelta(days=args.days)
    start_str = start.strftime('%Y-%m-%d')
    end_str = end.strftime('%Y-%m-%d')

    # Build tasks
    if args.asset.upper() == 'ALL':
        assets = ['AAPL', 'TSLA', 'INTC', 'AMZN', 'MSFT', 'NVDA', 'NFLX', 'GOOG',
                  'MCD', 'KO', 'DIS', 'SBUX', 'GLD']
    else:
        assets = [args.asset]

    tasks = []
    for ev in evaluator_names:
        for asset in assets:
            tasks.append((asset, ev, args.preparer, start_str, end_str, mm_path, None))

    print(f"Testing {len(tasks)} tasks across {len(assets)} assets...")
    print(f"Date range: {start_str} → {end_str}")

    results = []
    if args.parallel:
        with Pool(args.workers) as pool:
            for r in pool.imap_unordered(run_single_evaluator, tasks):
                if r:
                    results.append(r)
                    sys.stdout.write(f"\rDone: {len(results)}/{len(tasks)}")
                    sys.stdout.flush()
    else:
        for task in tasks:
            r = run_single_evaluator(task)
            if r:
                results.append(r)
                sys.stdout.write(f"\rDone: {len(results)}/{len(tasks)}")
                sys.stdout.flush()

    print(f"\n\nTotal results: {len(results)}")

    if not results:
        print("No results!")
        return

    # Group by evaluator (average across assets)
    from collections import defaultdict
    by_eval = defaultdict(list)
    for r in results:
        by_eval[r['evaluator']].append(r)

    summary = []
    for ev_name, res_list in by_eval.items():
        pnls = [r['pnl'] for r in res_list if 'pnl' in r]
        ops = sum(r.get('operations', 0) for r in res_list)
        wins = sum(r.get('wins', 0) for r in res_list)
        losses = sum(r.get('losses', 0) for r in res_list)
        total_pnl = sum(pnls)
        summary.append({
            'evaluator': ev_name,
            'total_pnl': total_pnl,
            'operations': ops,
            'wins': wins,
            'losses': losses,
            'win_rate': round(wins/(wins+losses)*100, 1) if (wins+losses) > 0 else 0,
            'assets_tested': len(res_list),
        })

    summary.sort(key=lambda x: x['total_pnl'], reverse=True)

    print(f"\n{'='*80}")
    print(f"RANKING — {args.preparer} ({args.days} days, {len(assets)} assets)")
    print(f"{'='*80}")
    print(f"{'#':<4} {'Evaluator':<50} {'P&L':>12} {'Ops':>6} {'W':>4} {'L':>4} {'WR%':>5}")
    print(f"{'-'*80}")
    for i, s in enumerate(summary, 1):
        print(f"{i:<4} {s['evaluator']:<50} {s['total_pnl']:>12.2f} {s['operations']:>6} "
              f"{s['wins']:>4} {s['losses']:>4} {s['win_rate']:>5}")

    output_path = args.output
    if not output_path:
        import tempfile
        output_path = os.path.join(tempfile.gettempdir(), f"ranking_{args.days}d.json")

    with open(output_path, 'w') as f:
        json.dump({
            'meta': {
                'preparer': args.preparer,
                'days': args.days,
                'assets': assets,
                'timestamp': datetime.now().isoformat()
            },
            'results': results,
            'summary': summary
        }, f, indent=2)

    print(f"\nSaved: {output_path}")


if __name__ == '__main__':
    main()