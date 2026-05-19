#!/usr/bin/env python3
"""
Auto-genera prepareActivesEvaluators4 con TODOS los evaluadores de la carpeta
(excluye ONLY_UP, BTC, ETH, base classes)
Incluye los IMPORTS necesarios para ActiveHelper.py

Uso: python3 prepare_evaluators.py
"""
import os, re

EVAL_DIR = "/home/MarketManager/evaluators"
EXCLUDE_PREFIXES = [
    "__init__", "base", "Apertura", "Cierre", "compat", "DESCRIPTION",
    "Evaluator0", "Evaluator.py"  # Validator01-04 y base
]
EXCLUDE_NAMES = ["BTC", "ETH"]
EXCLUDE_IN_NAME = ["ONLY_UP", "BTC", "ETH"]

def to_camel(s):
    return s[:-3]

files = sorted(os.listdir(EVAL_DIR))
evaluators = []
for f in files:
    if not f.endswith(".py"):
        continue
    skip = False
    for prefix in EXCLUDE_PREFIXES:
        if f.startswith(prefix):
            skip = True
            break
    for ex in EXCLUDE_NAMES:
        if ex in f:
            skip = True
            break
    for ex in EXCLUDE_IN_NAME:
        if ex in f:
            skip = True
            break
    if skip:
        continue
    evaluators.append(to_camel(f))

print(f"Encontrados: {len(evaluators)} evaluadores")

# Generate imports (only the ones not already imported)
imports = []
for ev in evaluators:
    import_line = f"from evaluators import {ev}"
    if import_line not in imports:
        imports.append(import_line)

# Generate method
method_lines = [
    "    def prepareActivesEvaluators4(self, active):",
    "        activeList = list()",
    ""
]

for i, ev in enumerate(evaluators, 1):
    method_lines.append(f"        active{i} = copy.deepcopy(active)")
    method_lines.append(f"        active{i}.evaluator = {ev}()")
    method_lines.append(f"        activeList.append(active{i})")
    method_lines.append("")

method_lines.append("        return activeList")

# Build output
imports_str = "\n".join(sorted(set(imports)))
method_str = "\n".join(method_lines)

output = f"""# AUTO-GENERATED — NO EDITAR A MANO
# Run: python3 prepare_evaluators.py to regenerate
# Created: {len(evaluators)} evaluadores

# === IMPORTS for evaluators ===
{imports_str}

# === METHOD ===
{method_str}
"""

with open("/home/MarketManager/service/_generated_evaluators.txt", "w") as f:
    f.write(output)

print(f"Generado: _generated_evaluators.txt")
print(f"Imports: {len(imports_str.split(chr(10)))}")
print(f"Method lines: {len(method_lines)}")
print()
print("--- PREVIEW ---")
print(output[:2000])
print("... [truncated] ...")
print(f"\nTotal evaluadores: {len(evaluators)}")