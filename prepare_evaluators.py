#!/usr/bin/env python3
"""
Auto-genera prepareActivesEvaluators4 con TODOS los evaluadores de la carpeta
(excluye ONLY_UP, BTC, ETH, base classes)
Uso: python3 prepare_evaluators.py
"""
import os, re

EVAL_DIR = "/home/MarketManager/evaluators"
EXCLUDE_PREFIXES = [
    "__init__", "base", "Apertura", "Cierre", "compat", "DESCRIPTION",
    "Evaluator0", "Evaluator.py"  # Validator01-04 y base
]
EXCLUDE_NAMES = ["BTC", "ETH"]  # cryptos
EXCLUDE_IN_NAME = ["ONLY_UP", "BTC", "ETH"]

def to_camel(s):
    """EvaluatorEMA_LONG_02_02.py → EvaluatorEMA_LONG_02_02"""
    return s[:-3]  # remove .py

files = sorted(os.listdir(EVAL_DIR))
evaluators = []
for f in files:
    if not f.endswith(".py"):
        continue
    # Exclude by prefix
    skip = False
    for prefix in EXCLUDE_PREFIXES:
        if f.startswith(prefix):
            skip = True
            break
    # Exclude crypto
    for ex in EXCLUDE_NAMES:
        if ex in f:
            skip = True
            break
    # Exclude in name
    for ex in EXCLUDE_IN_NAME:
        if ex in f:
            skip = True
            break
    if skip:
        continue
    evaluators.append(to_camel(f))

print(f"Encontrados: {len(evaluators)} evaluadores")
print(f"Ejemplos: {evaluators[:5]}")

# Generar método
lines = [
    "    def prepareActivesEvaluators4(self, active):",
    "        activeList = list()",
    ""
]

for i, ev in enumerate(evaluators, 1):
    lines.append(f"        active{i} = copy.deepcopy(active)")
    lines.append(f"        active{i}.evaluator = {ev}()")
    lines.append(f"        activeList.append(active{i})")
    lines.append("")

lines.append("        return activeList")

method = "\n".join(lines)

# Save to file
output = f"""# AUTO-GENERATED — NO EDITAR A MANO
# Run: python3 prepare_evaluators.py to regenerate

{method}
"""
with open("/home/MarketManager/service/_generated_evaluators.txt", "w") as f:
    f.write(output)

print(f"\nGenerado: /home/MarketManager/service/_generated_evaluators.txt")
print(f"Lineas: {len(lines)}")

# Show first 30 and last 5
print("\n--- PREVIEW (primeros 30) ---")
for l in lines[:60]:
    print(l)
print("... [truncated] ...")