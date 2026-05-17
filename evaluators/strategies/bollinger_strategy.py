"""
Bollinger Bands strategy implementation.
Replaces: EvaluatorBOLLINGER_*.py (24 files)
"""
import pandas as pd
from typing import Dict, Any, Optional

from ..base.evaluator_base import EvaluatorBase, EvaluationResult
from ..factory import register_evaluator


@register_evaluator('bollinger')
class BollingerStrategy(EvaluatorBase):
    """Bollinger Bands based trading strategy.

    Replaces the following files:
    - EvaluatorBOLLINGER_00 through EvaluatorBOLLINGER_09
    - EvaluatorBOLLINGER_LARGE_01 through _03
    - EvaluatorBOLLINGER_ONLY_UP_01 through _03_01
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)

        # Default parameters (can be overridden by config)
        self.only_up = self.get_param('only_up', False)
        self.blg_dist_percent = self.get_param('blg_dist_percent', 70)
        self.medstd_min_diff = self.get_param('medstd_min_diff', 0.5)
        self.enable_control_open = self.get_param('enable_control_open', True)

    def evaluate(self, data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Evaluate Bollinger Bands conditions.

        Args:
            data: DataFrame with market data and Bollinger Band indicators
            context: Additional context

        Returns:
            EvaluationResult with trading signals
        """
        if len(data) == 0:
            return EvaluationResult()

        # Check open conditions
        open_conditions = self.conditions.get('open', [])
        close_conditions = self.conditions.get('close', [])

        should_open = self.check_conditions(open_conditions, data, context) if open_conditions else False
        should_close = self.check_conditions(close_conditions, data, context) if close_conditions else False

        # Apply OnlyUp filter if enabled
        if should_open and self.only_up:
            should_open = self._check_only_up_condition(data)

        # Calculate confidence based on distance from bands
        confidence = self._calculate_confidence(data)

        # Build metadata
        metadata = {
            'blg_dist_percent': self.blg_dist_percent,
            'only_up': self.only_up,
            'open_conditions_met': should_open,
            'close_conditions_met': should_close
        }

        # Add indicator values if available
        if 'blg_upper' in data.columns:
            metadata['blg_upper'] = data['blg_upper'].iloc[-1]
        if 'blg_lower' in data.columns:
            metadata['blg_lower'] = data['blg_lower'].iloc[-1]
        if 'blg_middle' in data.columns:
            metadata['blg_middle'] = data['blg_middle'].iloc[-1]

        return EvaluationResult(
            should_open=should_open,
            should_close=should_close,
            confidence=confidence,
            metadata=metadata
        )

    def _check_only_up_condition(self, data: pd.DataFrame) -> bool:
        """Check if OnlyUp condition is met (trend is positive).

        Args:
            data: DataFrame with market data

        Returns:
            True if trend is positive
        """
        if len(data) < 2:
            return False

        # Check if price is above middle band (uptrend)
        if 'blg_middle' in data.columns:
            current_price = data['Close'].iloc[-1]
            middle_band = data['blg_middle'].iloc[-1]
            return current_price > middle_band

        # Fallback: check if price is above moving average
        if 'SMA20' in data.columns:
            return data['Close'].iloc[-1] > data['SMA20'].iloc[-1]

        # Fallback: check recent price change
        if len(data) >= 2:
            return data['Close'].iloc[-1] > data['Close'].iloc[-2]

        return False

    def _calculate_confidence(self, data: pd.DataFrame) -> float:
        """Calculate confidence based on distance from Bollinger Bands.

        Args:
            data: DataFrame with market data

        Returns:
            Confidence value between 0.0 and 1.0
        """
        if 'blg_upper' not in data.columns or 'blg_lower' not in data.columns:
            return 0.0

        current_price = data['Close'].iloc[-1]
        upper = data['blg_upper'].iloc[-1]
        lower = data['blg_lower'].iloc[-1]
        middle = data['blg_middle'].iloc[-1] if 'blg_middle' in data.columns else (upper + lower) / 2

        # Calculate distance from middle band as percentage of band width
        band_width = upper - lower
        if band_width == 0:
            return 0.0

        distance_from_middle = abs(current_price - middle)
        confidence = min(distance_from_middle / band_width * 2, 1.0)

        return confidence
