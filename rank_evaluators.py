#!/usr/bin/env python3
"""
Evaluator Ranker v2 — Backtest paralelo para PC potente
======================================================
Ejecuta cada evaluador en modo simulación sobre datos históricos
y devuelve P&L por evaluador.

Uso:
  # Paralelo (usa todos los cores)
  python3 rank_evaluators.py --all --days 30 --parallel

  # BTC/ETH solo (LONG only)
  python3 rank_evaluators.py --asset BTCUSD --days 30

  # Stock específico (LONG + SHORT)
  python3 rank_evaluators.py --asset AAPL --days 30

  # Un activo específico, todos los días
  python3 rank_evaluators.py --all --days 30 --assets BTC,ETH,AAPL,TSLA

Flags:
  --all              todos los assets
  --days N           días hacia atrás (default 7)
  --parallel         usa multiprocessing (PC potente)
  --workers N         workers paralelos (default num_cores)
  --output FILE       guardar JSON (default /tmp/evaluator_ranking.json)
  --limit N           limitar a N evaluadores (para debug rápido)
"""

import sys, os, argparse, json, time
sys.path.insert(0, '/home/MarketManager')
os.environ['DISPLAY'] = ':99'

import importlib.util
from datetime import datetime, timedelta
from service.ActiveHelper import ActiveHelper
from multiprocessing import Pool, cpu_count
from functools import partial

# ── Asset → preparer mapping ─────────────────────────────────────────────────

CRYPTO_ASSETS = {'BTC', 'ETH', 'BTCUSD', 'ETHUSD'}

def get_preparer_methods(activeHelper, asset_name):
    """Devuelve el método de preparación según tipo de asset."""
    asset_key = asset_name.upper()
    if asset_key in CRYPTO_ASSETS:
        return 'prepareActivesEvaluatorsONLYUPNEW', 11
    else:
        return 'prepareActivesEvaluators4', 24


def load_market_manager():
    spec = importlib.util.spec_from_file_location(
        "MarketManager", "/home/MarketManager/MarketManager.py"
    )
    mm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mm)
    return mm


def run_single_evaluator(args):
    """Ejecuta un único evaluador sobre un asset. Diseñado para multiprocessing."""
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

        prepare_method = getattr(activeHelper, prepare_map[norm])
        active = prepare_method()
        preparer = getattr(activeHelper, preparer_method)
        activesList = preparer(active)

        # Encontrar el evaluador específico
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


def run_asset(args):
    """Ejecuta todos los evaluadores para un asset. Unidad de paralelismo."""
    asset_name, preparer_method, num_evals, start, end, mm_path, sim_flags, parallel = args

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
        return []

    prepare_method_fn = getattr(activeHelper, prepare_map[norm])
    active = prepare_method_fn()
    preparer = getattr(activeHelper, preparer_method)
    activesList = preparer(active)

    if parallel:
        # Crear tareas para cada evaluador
        tasks = [
            (asset_name, a.evaluator.name, preparer_method, start, end, mm_path, sim_flags)
            for a in activesList
        ]
        with Pool() as pool:
            results = pool.map(run_single_evaluator, tasks)
        return [r for r in results if r is not None]
    else:
        # Secuencial
        marketService = mm.MarketManager(
            simulation=True, isDBData=True, useConfig=True,
            start=start, end=end, showLog=False,
            disableInitPROB=sim_flags.get('disableInitPROB', False),
            disableCloseEndRevenue=sim_flags.get('disableCloseEndRevenue', False),
        )
        results = []
        for a in activesList:
            try:
                totalBuy, totalSell = marketService.simulateFlowConfigReview(
                    a, start, end, draw=False
                )
                results.append({
                    'evaluator': a.evaluator.name,
                    'asset': asset_name.upper(),
                    'total_buy': totalBuy,
                    'total_sell': totalSell,
                    'total': float(totalBuy + totalSell),
                })
            except Exception as e:
                results.append({
                    'evaluator': a.evaluator.name,
                    'asset': asset_name.upper(),
                    'total_buy': 0, 'total_sell': 0, 'total': 0,
                    'error': str(e)[:100],
                })
        return results


def main():
    parser = argparse.ArgumentParser(description='Evaluator Ranker v2')
    parser.add_argument('--asset', type=str, help='Asset específico (ej: AAPL, BTCUSD...)')
    parser.add_argument('--all', action='store_true', help='Todos los assets')
    parser.add_argument('--days', type=int, default=7, help='Días hacia atrás')
    parser.add_argument('--parallel', action='store_true', help='Usar multiprocessing')
    parser.add_argument('--workers', type=int, default=None, help='Num workers (default: num_cores)')
    parser.add_argument('--output', type=str, default='/tmp/evaluator_ranking.json', help='Fichero salida JSON')
    parser.add_argument('--limit', type=int, help='Limitar a N evaluadores por asset')
    parser.add_argument('--disable-init-prob', action='store_true', help='Deshabilitar init PROB')
    parser.add_argument('--no-disable-close', action='store_true', help='No deshabilitar close end revenue')
    args = parser.parse_args()

    # Assets
    all_assets = ['AAPL', 'TSLA', 'INTC', 'AMZN', 'MSFT', 'NVDA', 'NFLX', 'GOOG',
                  'AMD', 'MCD', 'KO', 'DIS', 'BABA', 'SBUX', 'META', 'SONY', 'HD', 'VTI', 'GLD']
    crypto_assets = ['BTC', 'ETH']

    if args.asset:
        assets_to_test = [args.asset.upper()]
    elif args.all:
        assets_to_test = all_assets + crypto_assets
    else:
        assets_to_test = ['INTC']

    # Load MM lazily
    print("📊 Evaluator Ranker v2 — Backtest")
    print(f"   Días: {args.days} | Assets: {len(assets_to_test)}")
    print(f"   Paralelo: {'Sí' if args.parallel else 'No'}")
    print(f"   Output: {args.output}")

    start = (datetime.now() - timedelta(days=args.days)).strftime('%Y-%m-%d')
    end = datetime.now().strftime('%Y-%m-%d')
    mm_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MarketManager.py')

    sim_flags = {
        'disableInitPROB': args.disable_init_prob,
        'disableCloseEndRevenue': not args.no_disable_close,
    }

    # ── Build task list ──
    tasks = []
    for asset in assets_to_test:
        preparer_method, num_evals = get_preparer_methods(None, asset)
        tasks.append((asset, preparer_method, num_evals, start, end, mm_path, sim_flags, args.parallel))

    total_evals = sum(t[2] for t in tasks)
    print(f"   Total simulaciones: {total_evals}")
    print()

    start_time = time.time()

    if args.parallel:
        num_workers = args.workers or cpu_count()
        print(f"⚡ Ejecutando en paralelo ({num_workers} workers)...")
        with Pool(num_workers) as pool:
            results_per_asset = pool.map(run_asset, tasks)
    else:
        print("🔁 Ejecutando secuencialmente...")
        results_per_asset = []
        for task in tasks:
            asset = task[0]
            res = run_asset(task)
            results_per_asset.append(res)

    all_results = []
    for res_list in results_per_asset:
        all_results.extend(res_list)

    elapsed = time.time() - start_time

    # ── Ranking global ──
    print(f"\n⏱️  Tiempo total: {elapsed:.1f}s")
    print(f"\n{'='*70}")
    print(f"📈 RANKING GLOBAL")
    print(f"{'='*70}")

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
        key=lambda x: x['total'],
        reverse=True
    )

    print(f"\n{'Rank':<4} {'Evaluator':<50} {'Total':>10} {'W':>4} {'L':>4} {'Assets'}")
    print(f"{'-'*4} {'-'*50} {'-'*10} {'-'*4} {'-'*4} {'-'*10}")
    for i, r in enumerate(ranking, 1):
        wr = r['wins'] / (r['wins'] + r['losses']) * 100 if (r['wins'] + r['losses']) > 0 else 0
        print(f"{i:<4} {r['evaluator']:<50} {r['total']:>+10.2f} {r['wins']:>4} {r['losses']:>4} {r['count']} ({', '.join(sorted(r['assets']))})")

    # ── Separate crypto ranking ──
    print(f"\n{'='*70}")
    print(f"📈 RANKING CRYPTO (LONG only — BTC/ETH)")
    print(f"{'='*70}")

    crypto_by_eval = {}
    for r in all_results:
        if 'error' in r or r['asset'].upper() not in {'BTC', 'ETH', 'BTCUSD', 'ETHUSD'}:
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
        key=lambda x: x['total'],
        reverse=True
    )

    print(f"\n{'Rank':<4} {'Evaluator':<50} {'Total':>10} {'W':>4} {'L':>4}")
    print(f"{'-'*4} {'-'*50} {'-'*10} {'-'*4} {'-'*4}")
    for i, r in enumerate(crypto_ranking, 1):
        wr = r['wins'] / (r['wins'] + r['losses']) * 100 if (r['wins'] + r['losses']) > 0 else 0
        print(f"{i:<4} {r['evaluator']:<50} {r['total']:>+10.2f} {r['wins']:>4} {r['losses']:>4}")

    # ── Save JSON ──
    output_data = {
        'ranking': ranking,
        'crypto_ranking': crypto_ranking,
        'all_results': all_results,
        'params': {
            'days': args.days,
            'start': start,
            'end': end,
            'assets': assets_to_test,
            'parallel': args.parallel,
            'elapsed_seconds': round(elapsed, 1),
        },
        'generated_at': datetime.now().isoformat(),
    }

    with open(args.output, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)

    print(f"\n💾 Guardado en {args.output}")
    return ranking, all_results


if __name__ == '__main__':
    main()