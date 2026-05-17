"""
New evaluator system - replaces 252 individual evaluator files.
"""
from .base import EvaluatorBase, EvaluationResult
from .factory import EvaluatorFactory, register_evaluator

# Import all strategies to register them
from .strategies import (
    BollingerStrategy,
    EMAStrategy,
    DirectionStrategy,
    OnlyUpStrategy,
)

# Additional strategies
from .strategies.medstd_strategy import MEDSTDStrategy
from .strategies.iblg_strategy import IBLGStrategy

__all__ = [
    'EvaluatorBase',
    'EvaluationResult',
    'EvaluatorFactory',
    'register_evaluator',
    'BollingerStrategy',
    'EMAStrategy',
    'DirectionStrategy',
    'OnlyUpStrategy',
    'MEDSTDStrategy',
    'IBLGStrategy',
]
