"""
Compatibility layer for legacy evaluator imports.
This allows existing code to continue working during migration.
"""
from typing import Dict, Any, Optional

from .factory import EvaluatorFactory
from .strategies import BollingerStrategy, EMAStrategy, DirectionStrategy, OnlyUpStrategy
from .strategies.medstd_strategy import MEDSTDStrategy
from .strategies.iblg_strategy import IBLGStrategy

# Map old evaluator names to new factory configurations
_EVALUATOR_MAP: Dict[str, Dict[str, Any]] = {
    # Bollinger evaluators
    'EvaluatorBOLLINGER_00': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 70}},
    'EvaluatorBOLLINGER_01': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 75}},
    'EvaluatorBOLLINGER_02': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 80}},
    'EvaluatorBOLLINGER_03': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 85}},
    'EvaluatorBOLLINGER_04': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 90}},
    'EvaluatorBOLLINGER_05': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 95}},
    'EvaluatorBOLLINGER_06': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 100}},
    'EvaluatorBOLLINGER_07': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 105}},
    'EvaluatorBOLLINGER_08': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 110}},
    'EvaluatorBOLLINGER_09': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 115}},
    'EvaluatorBOLLINGER_ONLY_UP_01': {'base_strategy': 'bollinger', 'params': {'only_up': True, 'blg_dist_percent': 70}},
    'EvaluatorBOLLINGER_ONLY_UP_02': {'base_strategy': 'bollinger', 'params': {'only_up': True, 'blg_dist_percent': 75}},
    'EvaluatorBOLLINGER_ONLY_UP_03': {'base_strategy': 'bollinger', 'params': {'only_up': True, 'blg_dist_percent': 80}},
    'EvaluatorBOLLINGER_ONLY_UP_03_01': {'base_strategy': 'bollinger', 'params': {'only_up': True, 'blg_dist_percent': 85}},

    # EMA evaluators
    'EvaluatorEMA_01': {'base_strategy': 'ema', 'params': {'ema_short': 10, 'ema_long': 20}},
    'EvaluatorEMA_02': {'base_strategy': 'ema', 'params': {'ema_short': 5, 'ema_long': 10}},
    'EvaluatorEMA_03': {'base_strategy': 'ema', 'params': {'ema_short': 12, 'ema_long': 26}},
    'EvaluatorEMA_04': {'base_strategy': 'ema', 'params': {'ema_short': 20, 'ema_long': 50}},
    'EvaluatorEMA_LONG_01': {'base_strategy': 'ema', 'params': {'ema_short': 10, 'ema_long': 20, 'only_up': True}},
    'EvaluatorEMA_LONG_02': {'base_strategy': 'ema', 'params': {'ema_short': 20, 'ema_long': 50, 'only_up': True}},

    # OnlyUp evaluators
    'EvaluatorOnlyUp01': {'base_strategy': 'only_up', 'params': {'uptrend_threshold': 0.0}},
    'EvaluatorOnlyUp02': {'base_strategy': 'only_up', 'params': {'uptrend_threshold': 0.01}},
    'EvaluatorOnlyUp03': {'base_strategy': 'only_up', 'params': {'uptrend_threshold': 0.02}},

    # Direction evaluators
    'EvaluatorDIRECTION_MEDSTD_01': {'base_strategy': 'direction', 'params': {'use_medstd': True, 'medstd_min_diff': 0.5}},
    'EvaluatorDIRECTION_MEDSTD_02': {'base_strategy': 'direction', 'params': {'use_medstd': True, 'medstd_min_diff': 0.6}},
    'EvaluatorDIRECTION_MEDSTD_03': {'base_strategy': 'direction', 'params': {'use_medstd': True, 'medstd_min_diff': 0.7}},

    # MEDSTD evaluators
    'EvaluatorMEDSTDOptimiz01': {'base_strategy': 'medstd', 'params': {'min_diff': 0.5}},
    'EvaluatorMEDSTDOptimiz02': {'base_strategy': 'medstd', 'params': {'min_diff': 0.6}},

    # IBLG evaluators
    'EvaluatorIBLG_LONG_00': {'base_strategy': 'iblg', 'params': {'use_angle': True, 'angle_up': 2.0}},
    'EvaluatorIBLG_LONG_01': {'base_strategy': 'iblg', 'params': {'use_angle': True, 'angle_up': 2.5}},
}


def get_legacy_evaluator(evaluator_name: str) -> Any:
    """Get a legacy evaluator using the new factory system.

    Args:
        evaluator_name: Name of the legacy evaluator

    Returns:
        Evaluator instance or None if not found
    """
    if evaluator_name not in _EVALUATOR_MAP:
        return None

    config = _EVALUATOR_MAP[evaluator_name].copy()
    config['name'] = evaluator_name
    return EvaluatorFactory.create_from_dict(config)


def create_legacy_evaluator_class(evaluator_name: str):
    """Create a class that mimics the legacy evaluator interface.

    Args:
        evaluator_name: Name of the legacy evaluator

    Returns:
        Class that wraps the new evaluator
    """
    config = _EVALUATOR_MAP.get(evaluator_name, {})
    base_strategy = config.get('base_strategy', 'bollinger')

    class LegacyEvaluator:
        """Legacy evaluator wrapper."""

        def __init__(self):
            full_config = config.copy()
            full_config['name'] = evaluator_name
            self._evaluator = EvaluatorFactory.create_from_dict(full_config)

        def evaluate(self, data, context=None):
            """Evaluate method compatible with old interface."""
            result = self._evaluator.evaluate(data, context)
            return result

        def evaluate_open(self, data, context=None):
            """Check if position should be opened."""
            return self._evaluator.evaluate_open(data, context)

        def evaluate_close(self, data, context=None):
            """Check if position should be closed."""
            return self._evaluator.evaluate_close(data, context)

        def getName(self):
            """Get evaluator name."""
            return evaluator_name

    return LegacyEvaluator


# Create backward-compatible class names
evaluator_classes = {}
for name in _EVALUATOR_MAP.keys():
    evaluator_classes[name] = create_legacy_evaluator_class(name)

# Export evaluator classes
globals().update(evaluator_classes)
