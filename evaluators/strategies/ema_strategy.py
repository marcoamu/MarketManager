"""
EMA (Exponential Moving Average) strategy implementation.
Replaces: EvaluatorEMA_*.py (25 files)
"""
import pandas as pd
from typing import Dict, Any, Optional

from ..base.evaluator_base import EvaluatorBase, EvaluationResult
from ..factory import register_evaluator


@register_evaluator('ema')
class EMAStrategy(EvaluatorBase):
    """EMA-based trading strategy.

    Replaces the following files:
    - EvaluatorEMA_01 through EvaluatorEMA_04
    - EvaluatorEMA_LONG_01 through EvaluatorEMA_LONG_03_09
    - EvaluatorEMA_LONG_ONLY_UP_01 through EvaluatorEMA_LONG_ONLY_UP_04_01
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)

        # Default parameters
        self.only_up = self.get_param('only_up', False)
        self.ema_short = self.get_param('ema_short', 10)
        self.ema_long = self.get_param('ema_long', 20)
        self.use_angle = self.get_param('use_angle', False)
        self.angle_threshold = self.get_param('angle_threshold', 2.0)

    def evaluate(self, data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Evaluate EMA conditions.

        Args:
            data: DataFrame with market data and EMA indicators
            context: Additional context

        Returns:
            EvaluationResult with trading signals
        """
        if len(data) == 0:
            return EvaluationResult()

        # Check configured conditions first
        open_conditions = self.conditions.get('open', [])
        close_conditions = self.conditions.get('close', [])

        should_open = self.check_conditions(open_conditions, data, context) if open_conditions else False
        should_close = self.check_conditions(close_conditions, data, context) if close_conditions else False

        # Fallback: check EMA crossover if no conditions configured
        if not open_conditions and not should_open:
            should_open = self._check_ema_crossover(data, bullish=True)

        if not close_conditions and not should_close:
            should_close = self._check_ema_crossover(data, bullish=False)

        # Apply OnlyUp filter if enabled
        if should_open and self.only_up:
            should_open = self._check_only_up_condition(data)

        # Calculate confidence based on EMA relationship
        confidence = self._calculate_confidence(data)

        metadata = {
            'ema_short': self.ema_short,
            'ema_long': self.ema_long,
            'only_up': self.only_up,
            'open_conditions_met': should_open,
            'close_conditions_met': should_close
        }

        # Add indicator values
        ema_short_col = f'EMA{self.ema_short}'
        ema_long_col = f'EMA{self.ema_long}'
        if ema_short_col in data.columns:
            metadata['ema_short_value'] = data[ema_short_col].iloc[-1]
        if ema_long_col in data.columns:
            metadata['ema_long_value'] = data[ema_long_col].iloc[-1]

        return EvaluationResult(
            should_open=should_open,
            should_close=should_close,
            confidence=confidence,
            metadata=metadata
        )

    def _check_ema_crossover(self, data: pd.DataFrame, bullish: bool = True) -> bool:
        """Check for EMA crossover signal.

        Args:
            data: DataFrame with EMA indicators
            bullish: If True, check for bullish crossover (short above long)

        Returns:
            True if crossover condition is met
        """
        if len(data) < 2:
            return False

        ema_short_col = f'EMA{self.ema_short}'
        ema_long_col = f'EMA{self.ema_long}'

        if ema_short_col not in data.columns or ema_long_col not in data.columns:
            return False

        # Get current and previous values
        curr_short = data[ema_short_col].iloc[-1]
        curr_long = data[ema_long_col].iloc[-1]
        prev_short = data[ema_short_col].iloc[-2]
        prev_long = data[ema_long_col].iloc[-2]

        # Check for crossover
        if bullish:
            # Bullish: short EMA crosses above long EMA
            return curr_short > curr_long and prev_short <= prev_long
        else:
            # Bearish: short EMA crosses below long EMA
            return curr_short < curr_long and prev_short >= prev_long

    def _check_only_up_condition(self, data: pd.DataFrame) -> bool:
        """Check if trend is positive.

        Args:
            data: DataFrame with market data

        Returns:
            True if trend is positive
        """
        ema_short_col = f'EMA{self.ema_short}'
        ema_long_col = f'EMA{self.ema_long}'

        if ema_short_col in data.columns and ema_long_col in data.columns:
            return data[ema_short_col].iloc[-1] > data[ema_long_col].iloc[-1]

        return False

    def _calculate_confidence(self, data: pd.DataFrame) -> float:
        """Calculate confidence based on EMA separation.

        Args:
            data: DataFrame with market data

        Returns:
            Confidence value between 0.0 and 1.0
        """
        ema_short_col = f'EMA{self.ema_short}'
        ema_long_col = f'EMA{self.ema_long}'

        if ema_short_col not in data.columns or ema_long_col not in data.columns:
            return 0.0

        short_val = data[ema_short_col].iloc[-1]
        long_val = data[ema_long_col].iloc[-1]
        current_price = data['Close'].iloc[-1]

        if long_val == 0:
            return 0.0

        # Calculate separation as percentage
        separation = abs(short_val - long_val) / long_val
        confidence = min(separation * 10, 1.0)  # Scale up, cap at 1.0

        return confidence
