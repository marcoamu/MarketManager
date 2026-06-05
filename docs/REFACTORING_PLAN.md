# Plan: Separar MarketManager.py (7,392 líneas) en módulos

## Estructura propuesta

```
core/
  __init__.py                    # Exports principales
  market_manager.py              # Class MarketManager (~500 líneas)
                                # Solo init, config, orchestación

  evaluation/
    __init__.py
    indicators.py               # _eval_* métodos (~400 líneas)
    actions.py                  # evaluateActions, evaluateNewAction, applyNewAction (~400 líneas)
    flow.py                      # determinar_flujo, getProbFlow, calculateHourlyFlow (~400 líneas)

  data/
    __init__.py
    prices.py                    # search_prices*, inserDataPrices (~200 líneas)
    relative.py                  # calculateRelativeValues*, getPrevRelativeValues (~300 líneas)

  simulation/
    __init__.py
    simulate.py                  # simulateFlow, RealMode, simulate* (~400 líneas)
    analysis.py                  # generateAnalisysData*, evaluateMarketMovements (~300 líneas)

  models/
    __init__.py
    results.py                   # Result dataclass
    config.py                    # Config generation helpers
```

## Estrategia

**REGLA #1: No romper nada**
- Cada módulo nuevo mantiene la misma interfaz pública
- Los imports existentes siguen funcionando
- Test smoke después de cada cambio

**REGLA #2: Un cambio a la vez**
- Empezar por lo más sencillo (funciones independientes)
- No tocar lógica, solo reorganizar
- Commits pequeños después de cada paso

**REGLA #3: Tests antes de push**
- `test_smoke.py` pasa → push
- Falla → revertir y corregir

---

## Pasos

### Paso 1: Functions sueltas → simulation/analysis.py
Mover las funciones de módulo (no métodos de clase):
- `generateAnalisysData` → `simulation.analysis`
- `generateAnalisysDataColoredOK` → `simulation.analysis`
- `generateAnalisysDataColored` → `simulation.analysis`
- `evaluateMarketMovements` → `simulation.analysis`
- `simulateFlowConfig` → `simulation.simulate`
- `simulateFlow` → `simulation.simulate`
- `RealModeConfig` → `simulation.simulate`
- `RealMode` → `simulation.simulate`
- `RealModeLocal` → `simulation.simulate`
- `drawActive` → `simulation.simulate`
- `drawActiveDates` → `simulation.simulate`
- `drawActiveDatesSelected` → `simulation.simulate`
- `simulateFlowActive` → `simulation.simulate`
- `drawRelativeTendence` → `simulation.simulate`
- `simulateWeekDirection` → `simulation.simulate`
- `simulateIndicatorDates` → `simulation.simulate`
- `simulateEvaluatorsForActiveDates` → `simulation.simulate`
- `simulate_Star_Close_ForActiveDates` → `simulation.simulate`
- `simulate_EMA_parameters_ForActiveDates` → `simulation.simulate`
- `simulate_Control_ForActiveDates` → `simulation.simulate`

### Paso 2: Métodos de datos → data/prices.py + data/relative.py
- `search_pricesYahoo` → `data.prices`
- `search_pricesDB` → `data.prices`
- `search_prices_list` → `data.prices`
- `inserDataPrices` → `data.prices`
- `calculateRelativeValuesFIXED2` → `data.relative`
- `get3daysValue` → `data.relative`
- `calculateRelativeValuesWith3days` → `data.relative`

### Paso 3: Métodos de evaluación → evaluation/
- `evaluateActions` → `evaluation.actions`
- `evaluateNewAction` → `evaluation.actions`
- `applyNewAction` → `evaluation.actions`
- `_eval_*` → `evaluation.indicators`
- `calculateSpecialIndicators` → `evaluation.indicators`
- `calculatePredictionIndicator` → `evaluation.indicators`

### Paso 4: Flujo → evaluation/flow.py
- `determinar_flujo` → `evaluation.flow`
- `determinar_flujo_WEEK` → `evaluation.flow`
- `calculateHourlyFlow` → `evaluation.flow`
- `getProbFlow` → `evaluation.flow`

### Paso 5: Solo MarketManager orchestrating
- init, createConfig, process, evaluate — delegando a los módulos

---

## Lo QUE NO tocamos todavía
- ActiveHelper.py (4,189 líneas) — después de MarketManager
- AlpacaServiceBot.py (1,185 líneas) — después de ActiveHelper
- MarketSQLManager.py (2,181 líneas) — después de todo

---

## Timeline sugerido
1. ✅ Crear estructura de carpetas
2. ⬜ Paso 1 (funciones) — 1 sesión
3. ⬜ Paso 2 (datos) — 1 sesión
4. ⬜ Paso 3 (evaluación) — 1 sesión
5. ⬜ Paso 4 (flujo) — 1 sesión
6. ⬜ Smoke test final + cleanup

Total: ~4-5 sesiones

---

## Scripts necesarios
```bash
# Crear estructura
mkdir -p core/evaluation core/data core/simulation core/models

# Test después de cada paso
./venv/bin/python3 test_smoke.py

# Commit después de cada paso
git add -A && git commit -m "refactor: move simulation functions to core/simulation/"
```