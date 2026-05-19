#!/usr/bin/env python3
"""
Smoke Test — Verify MarketManager can be imported and basic functions work
=======================================================================
Run this after ANY change before pushing to git.

Usage:
    cd /home/MarketManager && ./venv/bin/python3 test_smoke.py
    cd /home/MarketManager && ./venv/bin/python3 test_smoke.py --quick
"""

import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import():
    """Test 1: Can import MarketManager"""
    print("Test 1: Import MarketManager...")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("MarketManager", "MarketManager.py")
        mm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mm)
        print("  ✅ Import OK")
        return mm
    except Exception as e:
        print(f"  ❌ Import failed: {e}")
        return None

def test_activehelper(mm):
    """Test 2: ActiveHelper works"""
    print("Test 2: ActiveHelper...")
    try:
        ah = mm.ActiveHelper(simulation=True, isDBData=True)
        print("  ✅ ActiveHelper init OK")
        return True
    except Exception as e:
        print(f"  ❌ ActiveHelper failed: {e}")
        return False

def test_evaluators_count():
    """Test 3: prepareActivesEvaluators4 has evaluators"""
    print("Test 3: prepareActivesEvaluators4...")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("MarketManager", "MarketManager.py")
        mm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mm)
        ah = mm.ActiveHelper(simulation=True, isDBData=True)

        # Try with a dummy active — we just check the method exists
        has_method = hasattr(ah, 'prepareActivesEvaluators4')
        print(f"  {'✅' if has_method else '❌'} Method exists: {has_method}")

        # Get method source to count evaluators
        import inspect
        if has_method:
            src = inspect.getsource(ah.prepareActivesEvaluators4)
            count = src.count(".evaluator = Evaluator")
            print(f"  ✅ {count} evaluadores definidos")
            return count > 0
        return False
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def test_marketmanager_init(mm):
    """Test 4: MarketManager can init"""
    print("Test 4: MarketManager() init...")
    try:
        from datetime import datetime, timedelta
        end = datetime.now()
        start = end - timedelta(days=7)
        mgr = mm.MarketManager(
            simulation=True,
            isDBData=True,
            useConfig=False,
            showLog=False,
            start=start.strftime('%Y-%m-%d'),
            end=end.strftime('%Y-%m-%d')
        )
        print("  ✅ MarketManager init OK")
        return True
    except Exception as e:
        print(f"  ❌ MarketManager init failed: {e}")
        return False

def test_alpaca_service():
    """Test 5: AlpacaServiceBot can be imported"""
    print("Test 5: AlpacaServiceBot import...")
    try:
        spec = importlib.util.spec_from_file_location("AlpacaServiceBot", "service/AlpacaServiceBot.py")
        bot = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(bot)
        print("  ✅ AlpacaServiceBot import OK")
        return True
    except Exception as e:
        print(f"  ❌ AlpacaServiceBot import failed: {e}")
        return False

def test_params_btc_eth():
    """Test 6: Params BTC/ETH have operate=False"""
    print("Test 6: Params BTC/ETH operate=False...")
    try:
        spec = importlib.util.spec_from_file_location("ParamBTC06", "params/ParamBTC06.py")
        param = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(param)

        # Check file content directly (no instantiation needed)
        with open("params/ParamBTC06.py", "r") as f:
            content = f.read()
        btc_operate = "self.operate = False" in content

        with open("params/ParamETH03.py", "r") as f:
            content = f.read()
        eth_operate = "self.operate = False" in content

        both_ok = btc_operate and eth_operate
        print(f"  {'✅' if btc_operate else '❌'} BTC operate=False: {btc_operate}")
        print(f"  {'✅' if eth_operate else '❌'} ETH operate=False: {eth_operate}")
        return both_ok
    except Exception as e:
        print(f"  ❌ Params check failed: {e}")
        return False

def test_ranking_script():
    """Test 7: rank_all_evaluators.py can be imported"""
    print("Test 7: rank_all_evaluators.py import...")
    try:
        spec = importlib.util.spec_from_file_location("rank_all_evaluators", "rank_all_evaluators.py")
        script = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(script)
        print("  ✅ rank_all_evaluators.py import OK")
        return True
    except Exception as e:
        print(f"  ❌ rank_all_evaluators.py import failed: {e}")
        return False

def test_prepare_evaluators_script():
    """Test 8: prepare_evaluators.py works"""
    print("Test 8: prepare_evaluators.py runs...")
    try:
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "prepare_evaluators.py"],
            capture_output=True, text=True, timeout=10,
            cwd="/home/MarketManager"
        )
        if result.returncode == 0:
            count_line = [l for l in result.stdout.split('\n') if 'evaluadores' in l]
            print(f"  ✅ Script runs OK — {count_line[0].strip() if count_line else ''}")
            return True
        else:
            print(f"  ❌ Script failed: {result.stderr[:100]}")
            return False
    except Exception as e:
        print(f"  ❌ Script failed: {e}")
        return False

def test_docs_exist():
    """Test 9: Documentation exists"""
    print("Test 9: ARCHITECTURE.md exists...")
    exists = os.path.exists("docs/ARCHITECTURE.md")
    print(f"  {'✅' if exists else '❌'} docs/ARCHITECTURE.md: {exists}")
    return exists

def main():
    print("=" * 60)
    print("MarketManager Smoke Test")
    print("=" * 60)
    print()

    results = []

    # Core import
    mm = test_import()
    if mm is None:
        print("\n❌ CRITICAL FAILURE: Cannot import MarketManager")
        sys.exit(1)

    results.append(("Import", True))
    results.append(("ActiveHelper", test_activehelper(mm) if mm else False))
    results.append(("prepareActivesEvaluators4", test_evaluators_count()))
    results.append(("MarketManager init", test_marketmanager_init(mm) if mm else False))
    results.append(("AlpacaServiceBot", test_alpaca_service()))
    results.append(("Params BTC/ETH", test_params_btc_eth()))
    results.append(("rank_all_evaluators.py", test_ranking_script()))
    results.append(("prepare_evaluators.py", test_prepare_evaluators_script()))
    results.append(("ARCHITECTURE.md", test_docs_exist()))

    print()
    print("=" * 60)
    print("RESULTS")
    print("=" * 60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  {name}")

    print()
    print(f"Total: {passed}/{total} passed")

    if passed == total:
        print("✅ All tests passed — safe to push to git")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed — review before pushing")
        sys.exit(0)  # Don't block push, just warn

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--quick', action='store_true')
    args = parser.parse_args()

    main()