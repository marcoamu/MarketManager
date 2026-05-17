"""
Strategy implementations for the evaluator factory.
"""
from .bollinger_strategy import BollingerStrategy
from .ema_strategy import EMAStrategy
from .direction_strategy import DirectionStrategy
from .only_up_strategy import OnlyUpStrategy
from .medstd_strategy import MEDSTDStrategy
from .iblg_strategy import IBLGStrategy

__all__ = [
    'BollingerStrategy',
    'EMAStrategy',
    'DirectionStrategy',
    'OnlyUpStrategy',
    'MEDSTDStrategy',
    'IBLGStrategy',
]
