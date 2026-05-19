# MarketManager — Arquitectura y Documentación

> Última actualización: 2026-05-19

---

## Visión General

El proyecto tiene **~15,700 líneas** de Python en archivos principales:

| Archivo | Líneas | Responsabilidad |
|---------|--------|-----------------|
| `MarketManager.py` | 7,392 | Core — trading, evaluation, simulation |
| `ActiveHelper.py` | 4,189 | Preparación de activos y evaluadores |
| `MarketSQLManager.py` | 2,181 | Acceso a base de datos |
| `AlpacaServiceBot.py` | 1,185 | Broker API (Alpaca) |
| `MarketPublicAPI.py` | 516 | API REST pública |
| `trading_executor.py` | 275 | Ejecución de órdenes |

---

## MarketManager.py — 7,392 líneas

### Estructura interna

```
Líneas 28-36:     Decoradores (mide_tiempo)
Líneas 38-101:    MarketManager.__init__ + init()
Líneas 102-424:   Configuración (createConfig, initConfig, reviewControls)
Líneas 425-947:   Review results y evaluación
Líneas 947-1504:  Cálculos relative values, 3-days, intervals
Líneas 1504-2072: Determinación de flujo (determinar_flujo, WEEK, STDMEDIA)
Líneas 2072-2455: Búsqueda de precios (Yahoo, DB, local)
Líneas 2455-2915: Mensajes, drawActiveAction, evaluateNewAction
Líneas 2915-3362: Análisis, actions, applyNewAction, closeAndNewAction
Líneas 3362-3618: Indicadores (evaluateActions, inserDataPrices)
Líneas 3618-4081: Indicadores internos (_eval_* methods)
Líneas 4081-4322: Finalización (MinMax, Week indicators, ProbFlow)
Líneas 4322-4641: Special indicators BTC/ETH
Líneas 4641-5357: Predicción y valores relativos
Líneas 5357-5856: Simulation methods
Líneas 5856-6727: Módulos de simulación (simulateFlowConfig, etc.)
Líneas 6727-7355: Simulate evaluators específicos
Líneas 7355-7392: main()
```

### Métodos públicos principales (para entender el flujo)

```python
# Init
MarketManager.__init__(simulation, isDBData, useConfig, showLog, ...)
MarketManager.init()
MarketManager.createConfig(active)
MarketManager.initConfig(active, data)

# Price
MarketManager.search_pricesYahoo(active)
MarketManager.search_prices_list_local(actives)

# Evaluation
MarketManager.evaluateNewAction(results, active, isFastReview, isfcst)
MarketManager.evaluateActions(data, results, active, isFastReview)
MarketManager.evaluateActiveIndicators(results, data, active)

# Simulation
MarketManager.simulateFlowConfigReview(active, start, end, draw, isDBData)
MarketManager.simulateFlow()
MarketManager.RealMode()

# Alerts
MarketManager.processAlerts(alert, results, active)
```

### Secrets y Config

- Alpaca API Key: `AK...` (en config/alpaca_config.json o env)
- Alpaca Secret: `sk...` (en config/alpaca_config.json o env)
- Variables: `MARKET_DATA_DIR`, `POSTGRES_PASSWORD`, etc.

---

## ActiveHelper.py — 4,189 líneas

### Métodos prepare* (generan listas de activos con evaluadores)

```python
prepareActivesEvaluators(active)         # Original — pocos evaluadores
prepareActivesEvaluators2(active)        # Variante 2
prepareActivesEvaluators3(active)        # Variante 3 (17 evaluadores)
prepareActivesEvaluators4(active)        # 206 evaluadores (AUTO-GENERATED)
prepareActivesEvaluatorsONLYUP(active)   # Solo evaluadores ONLY_UP
prepareActivesEvaluatorsONLYUPNEW(active)# 11 evaluadores BTC/ETH (en uso)
```

**prepareActivesEvaluators4** (206 evaluadores — generado por `prepare_evaluators.py`):
- Excluye: ONLY_UP, BTC, ETH, base classes
- Se regenera con: `python3 prepare_evaluators.py`

### Métodos prepareAssets* (generan listas de activos)

```python
prepareAAPL() / prepareTSLA() / prepareMSFT() / ... (23 assets)
```

### Helpers de flujo y análisis

```python
determinar_flujo(data)
determinar_flujo_WEEK(data)
getProbFlow(results, active)
calculateHourlyFlow(data, results, active)
collectFlowAnalisis(data, results, active)
```

---

## AlpacaServiceBot.py — 1,185 líneas

### Responsabilidad: comunicación con broker Alpaca

```python
submit_order(symbol, qty, side, type, time_in_force)
get_position(symbol)
get_all_positions()
cancel_order(order_id)
close_position(symbol)
close_all_positions()
get_account_info()
```

### Flags de operate

```python
self.operate = True  # BTC/ETH ahora en False (bloqueado)
```

---

## MarketPublicAPI.py — 516 líneas

### Endpoints principales

```
GET  /health
GET  /trading/positions
GET  /trading/orders
DELETE /trading/orders/{id}
POST /trading/close-all
POST /asset/{name}/stop-loss
POST /trading/daily-loss-limit
```

---

## trading_executor.py — 275 líneas

```python
execute_trade(action, active, marketService)
cancel_open_orders()
apply_stop_loss(position, active)
```

---

## Evaluators — 206 archivos

Carpeta: `/home/MarketManager/evaluators/`

- `EvaluatorBOLLINGER_*.py` — 13 evaluadores
- `EvaluatorEMA_*.py` — 25 evaluadores
- `EvaluatorIBLG_*.py` — 55 evaluadores
- `EvaluatorIMA1_*.py` — 20 evaluadores
- `EvaluatorMEDSTD*.py` — 20 evaluadores
- `EvaluatorMEDMOMENT_*.py` — 15 evaluadores
- `EvaluatorDIRECTION_*.py` — 10 evaluadores
- `EvaluatorDIST_*.py` — 15 evaluadores
- `EvaluatorBTCUSD_*.py` — 1 (bloqueado)
- `EvaluatorETHUSD_*.py` — 1 (bloqueado)

**NO USAR (ONLY_UP — crypto):**
- `Evaluator*ONLY_UP*.py` — 55 archivos (ruidosos, no funcionan bien)

---

## Parámetros de Configuración

```python
#Ubicación: /home/MarketManager/params/
ParamBTC06.py   → self.operate = False (BTC bloqueado)
ParamETH03.py   → self.operate = False (ETH bloqueado)
```

---

## Flags importantes del sistema

| Flag | Ubicación | Efecto |
|------|-----------|--------|
| `self.operate = False` | ParamBTC06/ETH03 | Bloquea trading crypto |
| `simulation=True` | MarketManager.__init__ | Modo simulación |
| `isDBData=True` | MarketManager.__init__ | Usa datos históricos DB |
| `useConfig=True` | MarketManager.__init__ | Usa config de archivo |

---

## Flujo de Trading Real

```
1. AlpacaServiceBot.start() — inicia polling
2. AlpacaServiceBot.checkTimeControls() — verifica hora trading
3. MarketManager.evaluateNewAction() — evalúa señal
4. Si signal → AlpacaServiceBot.submit_order() — envía orden
5. MarketManager.updateConfig() — guarda resultado
```

---

## Próximos pasos (Refactoring)

1. ✅ Documentar (este archivo)
2. ⬜ Separar MarketManager.py en módulos (core/evaluation/simulation)
3. ⬜ Tests de smoke para cada sección
4. ⬜ Actualizar prepareActivesEvaluators4 con winners del ranking
5. ⬜ Mejorar logs y errores
6. ⬜ Dashboard Grafana con métricas de evaluación

---

## Notas

- MarketManager.py tiene funciones sueltas en módulo (generateAnalisysData, simulateFlow, etc.)
- Hay código duplicado entre ActiveHelper y MarketManager
- Los métodos _eval_* son internos de evaluateActiveIndicators
- El archivo de 7,392 líneas es difícil de mantener — cualquier cambio requiere tests

---

_Last updated: 2026-05-19_