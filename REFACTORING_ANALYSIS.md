# MarketManager Refactoring Analysis
# Generated: 2026-05-19

## Current State

| Metric | Value |
|--------|-------|
| MarketManager.py total lines | 7,392 |
| Class methods | 100 |
| Standalone functions (already extracted to core/) | 1,357 lines |
| Class method code | ~6,035 lines |

## Service Dependencies (self. usage)

The class uses 9 main service objects:

| Service | Type | Used in N methods | Key operations |
|---------|------|-------------------|----------------|
| `self.dataBDMan` | MarketSQLManager | 15 | getAllWithNameForXdays, insert prices |
| `self.telegram` | TelegramService | 11 | send alerts, messages |
| `self.alpaca` | AlpacaServiceBot | 5 | getCurrentPrice, is_investedComplete |
| `self.operations` | Operations | 7 | buyData, sellData, closeData |
| `self.analisisHelper` | AnalisisHelper | 7 | evaluateActiveIndicators, calculate_rsi |
| `self.config_obj` | ConfigParser | 6 | read/write config.ini |
| `self.activeHelper` | ActiveHelper | 3 | prepareActives |
| `self.plotty` | PlottyService | ~5 | plotActive |
| `self.probEvaluator` | ProbEvaluator | 1 | (in __init__) |

## Methods by Self Reference Count

| Category | Count | Description |
|----------|-------|-------------|
| 0 self. refs | 26 | Pure functions, can be extracted directly |
| 1-5 self. refs | 40 | Light dependency, refactorable |
| 6-20 self. refs | 21 | Medium dependency, needs service injection |
| >20 self. refs | 7 | Heavy dependency, core methods |

## Methods with 0 self. References (Already Extractable)

These methods exist in the class but don't actually use `self`:

```
funcion_medida           (9 lines)   - decorator
reviewControls           (8 lines)   - empty stub
review_results          (1 line)     - @mide_tiempo wrapper
updateMinMaxValues       (10 lines)  - standalone
printValues             (10 lines)  - standalone  
determinar_flujo_WEEK   (23 lines)  - standalone, no deps
search_pricesYahoo      (12 lines)  - no self refs
findActiveInDB           (6 lines)  - standalone
addmessages             (11 lines)  - uses Constants only
isHour                  (33 lines)  - standalone
postcalculation         (36 lines)  - standalone
calcular_angulo         (13 lines)  - standalone math
calcular_minutos_entre_fechas (31 lines) - standalone math
_eval_init_parameters   (23 lines)  - standalone
_eval_bollinger_distances (43 lines) - standalone pure calcs
_eval_set_final_defaults (18 lines)  - standalone
determineMedMomentFlow  (26 lines)  - standalone
determine_Direction_percent_Flow (14 lines) - standalone
getProMEDSTD_MID        (203 lines) - BIG, standalone pure calc
determinePercentDistance (126 lines) - BIG, standalone pure calc
calculatePercentFcst    (23 lines)  - standalone math
determineFlow           (35 lines)  - standalone math
determinarRelativePercent (49 lines) - standalone
determinarIndicatorTendenceMomentBest (88 lines) - standalone
calculate_rsi           (45 lines)  - standalone, already in utils.py
simulateFlowConfigReview (1 line)   - just calls other method
```

**Total extractable with 0 refactor: ~800 lines across 26 methods**

## Dependency Groups (Methods that work together)

### Group 1: Price Data (uses dataBDMan + alpaca)
```
search_pricesDB           160 lines  - fetches from DB
search_prices_list        31 lines   - orchestrates price fetching
search_prices_list_local  28 lines   - local version
inserDataPrices           65 lines   - inserts to DB
search_prices_list_data_simulation  11 lines  - simulation mode
search_prices_list_data_simulation_INSERT 10 lines
```
**Potential extracted class:** `PriceDataManager(dataBDMan, alpaca)`

### Group 2: Config Management (uses config_obj)
```
createConfig              45 lines  - creates config section
initConfig               241 lines - inits from DB data
updateConfig             49 lines  - updates config
```
**Potential extracted class:** `ConfigManager(config_obj)`

### Group 3: Evaluation Core (uses many services, HIGH coupling)
```
evaluateNewAction        318 lines  - MAIN entry point for evaluation
evaluateActions           96 lines  - orchestrates evaluation
evaluateFcstPROB         108 lines  - forecast probability
calculateSpecialIndicators 138 lines - special calcs for BTC/ETH
extractResultsDataForAnalisys 178 lines - extracts data for analysis
```
**These are the hardest to extract - they use ALL services**

### Group 4: Indicator Calculation (uses analysisHelper, operations)
```
evaluateIndicators        28 lines  - calls _eval_* methods
evaluateActiveIndicators   8 lines  - delegates to analisisHelper
evaluateFinalIndicators   39 lines  - delegates to analisisHelper
calculateMinMax           20 lines  - min/max calculations
```
**Potential:** Keep in class but extract _eval_* helpers

### Group 5: Pure Math Utilities (no dependencies)
```
getProMEDSTD_MID         203 lines  - standalone (already extractable)
determinePercentDistance 126 lines  - standalone (already extractable)
calculatePrevRelativeValues 157 lines - calls determineFlow
determinarIndicatorTendenceMomentBest 88 lines - standalone
determinarFlujoSTDMEDIA   96 lines  - needs self.getDifTimeFromOpen
calculateHourlyFlow       93 lines  - needs self.calcular_minutos_entre_fechas
```
**These can be made standalone by passing dependencies as params**

## Existing Extracted Modules

| Module | Lines | Contents |
|--------|-------|----------|
| `core/simulation/` | 1,290 | simulate*, RealMode*, generateAnalisysData* |
| `core/models/utils.py` | 76 | calcular_angulo, calculate_rsi, determineFlow, etc. |

## Extraction Strategy: Dependency Injection

### Pattern to apply:
```python
# BEFORE (tightly coupled):
def search_pricesDB(self, active):
    current_value = self.alpaca.getCurrentPrice(...)
    data = self.dataBDMan.getAllWithNameForXdays(...)
    ...

# AFTER (dependency injection):
def search_pricesDB(dataBDMan, alpaca, active):
    current_value = alpaca.getCurrentPrice(...)
    data = dataBDMan.getAllWithNameForXdays(...)
    ...

# Class method becomes a thin wrapper:
def search_pricesDB(self, active):
    return search_pricesDB(self.dataBDMan, self.alpaca, active)
```

### This allows:
1. Methods become pure functions in modules
2. Class keeps backward compatibility (thin wrappers)
3. Easy testing with mock dependencies
4. Eventually remove the wrappers once all callers are updated

## Proposed Extraction Phases

### Phase 1: Pure Functions (0 self. refs) - LOW RISK
Extract 26 methods that don't use self at all. Just move to modules and add thin wrapper in class.

### Phase 2: Config Group - MEDIUM RISK  
Extract createConfig, initConfig, updateConfig into ConfigManager class.

### Phase 3: Price Data Group - MEDIUM RISK
Extract search_prices*, inserDataPrices into PriceDataManager class.

### Phase 4: Evaluation Core - HIGH RISK (defer)
This is where 90% of the complexity lives. Save for last.

### Phase 5: Evaluation Helpers (_eval_*)
These are mostly pure calculations. Extract after Phase 4.

## Backup Strategy

Before each phase:
1. Create branch: `refactor/phase-N`
2. Make changes
3. Run tests
4. Push branch
5. Merge to develop after validation

**ALWAYS keep MarketManager.py functional between phases**
