"""
OnlyUp strategy implementation.
Replaces: EvaluatorOnlyUp*.py (10 files)
"""
import pandas as pd
from typing import Dict, Any, Optional

from ..base.evaluator_base import EvaluatorBase, EvaluationResult
from ..factory import register_evaluator


@register_evaluator('only_up')
class OnlyUpStrategy(EvaluatorBase):
    """OnlyUp trading strategy - only opens positions in uptrends.

    Replaces the following files:
    - EvaluatorOnlyUp01 through EvaluatorOnlyUp09
    - EvaluatorOnlyUpMARKET01
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)

        # Default parameters
        self.uptrend_threshold = self.get_param('uptrend_threshold', 0.0)
        self.min_price_change = self.get_param('min_price_change', 0.01)
        self.lookback_period = self.get_param('lookback_period', 5)
        self.use_ema = self.get_param('use_ema', True)
        self.ema_period = self.get_param('ema_period', 20)

    def evaluate(self, data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Evaluate OnlyUp conditions.

        Args:
            data: DataFrame with market data
            context: Additional context

        Returns:
            EvaluationResult with trading signals
        """
        if len(data) == 0:
            return EvaluationResult()

        # Check if we're in an uptrend
        in_uptrend = self._is_uptrend(data)

        # Check configured conditions
        open_conditions = self.conditions.get('open', [])
        close_conditions = self.conditions.get('close', [])

        # For OnlyUp, only open if in uptrend AND conditions are met
        base_open = self.check_conditions(open_conditions, data, context) if open_conditions else False
        should_open = in_uptrend and base_open

        should_close = self.check_conditions(close_conditions, data, context) if close_conditions else False

        # Also close if trend reverses (optional, based on config)
        if self.get_param('close_on_downtrend', False) and not in_uptrend:
            should_close = True

        # Calculate confidence based on trend strength
        confidence = self._calculate_confidence(data, in_uptrend)

        metadata = {
            'in_uptrend': in_uptrend,
            'uptrend_threshold': self.uptrend_threshold,
            'lookback_period': self.lookback_period,
            'open_conditions_met': should_open,
            'close_conditions_met': should_close
        }

        # Add trend indicators
        if len(data) >= 2:
            metadata['price_change'] = (data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2] if data['Close'].iloc[-2] != 0 else 0

        return EvaluationResult(
            should_open=should_open,
            should_close=should_close,
            confidence=confidence,
            metadata=metadata
        )

    def _is_uptrend(self, data: pd.DataFrame) -> bool:
        """Check if market is in an uptrend.

        Args:
            data: DataFrame with market data

        Returns:
            True if in uptrend
        """
        if len(data) < self.lookback_period:
            return False

        # Method 1: Use EMA if available and configured
        if self.use_ema:
            ema_col = f'EMA{self.ema_period}'
            if ema_col in data.columns:
                current_price = data['Close'].iloc[-1]
                ema_value = data[ema_col].iloc[-1]
                return current_price > ema_value * (1 + self.uptrend_threshold)

        # Method 2: Compare current price to N periods ago
        current = data['Close'].iloc[-1]
        past = data['Close'].iloc[-self.lookback_period]

        if past == 0:
            return False

        change = (current - past) / past
        return change > self.uptrend_threshold

    def _calculate_confidence(self, data: pd.DataFrame, in_uptrend: bool) -> float:
        """Calculate confidence based on trend strength.

        Args:
            data: DataFrame with market data
            context: Additional context

        Returns:
            Confidence value between 0.0 and 1.0
        """
        if not in_uptrend or len(data) < self.lookback_period:
            return 0.0

        current = data['Close'].iloc[-1]
        past = data['Close'].iloc[-self.lookback_period]

        if past == 0:
            return 0.0

        change = abs(current - past) / past
        confidence = min(change * 10, 1.0)  # Scale up, cap at 1.0

        return confidence
