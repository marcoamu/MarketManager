#!/usr/bin/env python3
"""
Evaluator Ranker v2 — Backtest paralelo para PC potente
======================================================
Uso:
  python3 rank_evaluators.py --all --days 30 --parallel
  python3 rank_evaluators.py --asset AAPL --days 7
  python3 rank_evaluators.py --asset BTC --days 30 --parallel --workers 8
"""

import sys, os, argparse, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import importlib.util
from datetime import datetime, timedelta
from multiprocessing import Pool, cpu_count


def run_single_evaluator(args):
    """Una tarea: un evaluador sobre un asset. Unit of parallel work."""
    asset_name, evaluator_name, preparer_method, start, end, mm_path, sim_flags = args

    try:
        spec = importlib.util.spec_from_file_location("MarketManager", mm_path)
        mm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mm)

        activeHelper = mm.ActiveHelper(simulation=True, isDBData=True)
        prepare_map = {
            'AAPL': 'prepareAAPL', 'TSLA': 'prepareTSLA', 'INTC': 'prepareINTC',
            'AMZN': 'prepareAMZN', 'MSFT': 'prepareMSFT', 'NVDA': 'prepareNVDA',
            'NFLX': 'prepareNFLX', 'GOOG': 'prepareGOOG', 'BTC': 'prepareBTC',
            'ETH': 'prepareETH', 'AMD': 'prepareAMD', 'MCD': 'prepareMCD',
            'KO': 'prepareKO', 'DIS': 'prepareDIS', 'BABA': 'prepareBABA',
            'VTI': 'prepareVTI', 'HD': 'prepareHD', 'SBUX': 'prepareSBUX',
            'META': 'prepareMETA', 'SONY': 'prepareSONY', 'GLD': 'prepareGLD',
        }

        norm = asset_name.upper()
        if norm == 'BTCUSD': norm = 'BTC'
        if norm == 'ETHUSD': norm = 'ETH'
        if norm not in prepare_map:
            return None

        prepare_fn = getattr(activeHelper, prepare_map[norm])
        active = prepare_fn()
        preparer = getattr(activeHelper, preparer_method)
        activesList = preparer(active)

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
            disableInitPROB=sim_flags.get('disableInitPROB', False),
            disableCloseEndRevenue=sim_flags.get('disableCloseEndRevenue', False),
        )

        totalBuy, totalSell = marketService.simulateFlowConfigReview(
            target, start, end, draw=False
        )
        total = float(totalBuy + totalSell)

        return {
            'evaluator': evaluator_name,
            'asset': asset_name.upper(),
            'total_buy': totalBuy,
            'total_sell': totalSell,
            'total': total,
        }

    except Exception as e:
        return {
            'evaluator': evaluator_name,
            'asset': asset_name.upper(),
            'total_buy': 0, 'total_sell': 0, 'total': 0,
            'error': str(e)[:100],
        }


def main():
    parser = argparse.ArgumentParser(description='Evaluator Ranker v2')
    parser.add_argument('--asset', type=str, help='Asset específico')
    parser.add_argument('--all', action='store_true', help='Todos los assets')
    parser.add_argument('--days', type=int, default=7, help='Días hacia atrás')
    parser.add_argument('--parallel', action='store_true', help='Multiprocessing')
    parser.add_argument('--workers', type=int, default=None, help='Num workers')
    parser.add_argument('--output', type=str, default='/tmp/evaluator_ranking.json')
    parser.add_argument('--limit', type=int, help='Limitar N tareas (debug)')
    parser.add_argument('--disable-init-prob', action='store_true')
    parser.add_argument('--no-disable-close', action='store_true')
    args = parser.parse_args()

    all_assets = ['AAPL','TSLA','INTC','AMZN','MSFT','NVDA','NFLX','GOOG',
                  'AMD','MCD','KO','DIS','BABA','SBUX','META','SONY','HD','VTI','GLD']
    crypto_assets = ['BTC','ETH']

    if args.asset:
        assets_to_test = [args.asset.upper()]
    elif args.all:
        assets_to_test = all_assets + crypto_assets
    else:
        assets_to_test = ['INTC']

    preparer_map = {a: 'prepareActivesEvaluators4' for a in all_assets}
    for c in crypto_assets:
        preparer_map[c.upper()] = 'prepareActivesEvaluatorsONLYUPNEW'

    print("📊 Evaluator Ranker v2")
    print(f"   Días: {args.days} | Assets: {len(assets_to_test)}")
    print(f"   Paralelo: {'Sí' if args.parallel else 'No'}")

    start = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    mm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MarketManager.py')
    sim_flags = {
        'disableInitPROB': args.disable_init_prob,
        'disableCloseEndRevenue': not args.no_disable_close,
    }

    # Build flat task list: one entry per (asset, evaluator)
    spec = importlib.util.spec_from_file_location("MarketManager", mm_path)
    mm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mm)
    activeHelper = mm.ActiveHelper(simulation=True, isDBData=True)
    prepare_map = {
        'AAPL': 'prepareAAPL', 'TSLA': 'prepareTSLA', 'INTC': 'prepareINTC',
        'AMZN': 'prepareAMZN', 'MSFT': 'prepareMSFT', 'NVDA': 'prepareNVDA',
        'NFLX': 'prepareNFLX', 'GOOG': 'prepareGOOG', 'BTC': 'prepareBTC',
        'ETH': 'prepareETH', 'AMD': 'prepareAMD', 'MCD': 'prepareMCD',
        'KO': 'prepareKO', 'DIS': 'prepareDIS', 'BABA': 'prepareBABA',
        'VTI': 'prepareVTI', 'HD': 'prepareHD', 'SBUX': 'prepareSBUX',
        'META': 'prepareMETA', 'SONY': 'prepareSONY', 'GLD': 'prepareGLD',
    }

    tasks = []
    for asset in assets_to_test:
        norm = asset.upper()
        if norm == 'BTCUSD': norm = 'BTC'
        if norm == 'ETHUSD': norm = 'ETH'
        if norm not in prepare_map:
            continue

        preparer_method = preparer_map[asset.upper()]
        active_fn = getattr(activeHelper, prepare_map[norm])
        active = active_fn()
        preparer = getattr(activeHelper, preparer_method)
        activesList = preparer(active)

        for a in activesList:
            tasks.append((asset, a.evaluator.name, preparer_method, start, end, mm_path, sim_flags))

    if args.limit:
        tasks = tasks[:args.limit]

    print(f"   Total simulaciones: {len(tasks)}")
    start_time = time.time()

    if args.parallel:
        num_workers = args.workers or cpu_count()
        print(f"⚡ Paralelo ({num_workers} workers)...")
        ctx = __import__('multiprocessing').get_context('spawn')
        with ctx.Pool(num_workers) as pool:
            all_results = pool.map(run_single_evaluator, tasks)
    else:
        print("🔁 Secuencial...")
        all_results = []
        for i, task in enumerate(tasks, 1):
            r = run_single_evaluator(task)
            all_results.append(r)
            if i % 10 == 0:
                print(f"  {i}/{len(tasks)}")

    elapsed = time.time() - start_time
    all_results = [r for r in all_results if r is not None]

    # ── Ranking global ──
    by_eval = {}
    for r in all_results:
        if 'error' in r:
            continue
        name = r['evaluator']
        if name not in by_eval:
            by_eval[name] = {'total': 0, 'count': 0, 'wins': 0, 'losses': 0, 'assets': set()}
        by_eval[name]['total'] += r['total']
        by_eval[name]['count'] += 1
        by_eval[name]['assets'].add(r['asset'])
        if r['total'] > 0:
            by_eval[name]['wins'] += 1
        elif r['total'] < 0:
            by_eval[name]['losses'] += 1

    ranking = sorted(
        [{'evaluator': k, **v} for k, v in by_eval.items()],
        key=lambda x: x['total'], reverse=True
    )

    print(f"\n⏱️  {elapsed:.1f}s")
    print(f"\n{'='*70}")
    print(f"📈 RANKING GLOBAL ({len(tasks)} simulaciones)")
    print(f"{'='*70}")
    print(f"\n{'Rank':<4} {'Evaluator':<50} {'Total':>10} {'W':>4} {'L':>4} {'Assets'}")
    print(f"{'-'*4} {'-'*50} {'-'*10} {'-'*4} {'-'*4} {'-'*10}")
    for i, r in enumerate(ranking, 1):
        wr = r['wins'] / (r['wins'] + r['losses']) * 100 if (r['wins'] + r['losses']) > 0 else 0
        print(f"{i:<4} {r['evaluator']:<50} {r['total']:>+10.2f} {r['wins']:>4} {r['losses']:>4} {r['count']} ({', '.join(sorted(r['assets']))})")

    # Crypto ranking
    crypto_by_eval = {}
    for r in all_results:
        if 'error' in r or r['asset'].upper() not in {'BTC','ETH','BTCUSD','ETHUSD'}:
            continue
        name = r['evaluator']
        if name not in crypto_by_eval:
            crypto_by_eval[name] = {'total': 0, 'count': 0, 'wins': 0, 'losses': 0, 'assets': set()}
        crypto_by_eval[name]['total'] += r['total']
        crypto_by_eval[name]['count'] += 1
        crypto_by_eval[name]['assets'].add(r['asset'])
        if r['total'] > 0:
            crypto_by_eval[name]['wins'] += 1
        elif r['total'] < 0:
            crypto_by_eval[name]['losses'] += 1

    crypto_ranking = sorted(
        [{'evaluator': k, **v} for k, v in crypto_by_eval.items()],
        key=lambda x: x['total'], reverse=True
    )

    if crypto_ranking:
        print(f"\n{'='*70}")
        print(f"📈 RANKING CRYPTO (LONG only — BTC/ETH)")
        print(f"{'-'*4} {'-'*50} {'-'*10} {'-'*4} {'-'*4}")
        for i, r in enumerate(crypto_ranking, 1):
            print(f"{i:<4} {r['evaluator']:<50} {r['total']:>+10.2f} {r['wins']:>4} {r['losses']:>4}")

    # Save
    output_data = {
        'ranking': ranking,
        'crypto_ranking': crypto_ranking,
        'all_results': all_results,
        'params': {
            'days': args.days, 'start': start, 'end': end,
            'assets': assets_to_test, 'parallel': args.parallel,
            'elapsed_seconds': round(elapsed, 1),
        },
        'generated_at': datetime.now().isoformat(),
    }
    with open(args.output, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)
    print(f"\n💾 {args.output}")
    return ranking, all_results


if __name__ == '__main__':
    main()