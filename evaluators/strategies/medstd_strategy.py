"""
MEDSTD (Mean/Standard Deviation) strategy implementation.
Replaces: EvaluatorMEDSTD*.py (25 files)
"""
import pandas as pd
from typing import Dict, Any, Optional

from ..base.evaluator_base import EvaluatorBase, EvaluationResult
from ..factory import register_evaluator


@register_evaluator('medstd')
class MEDSTDStrategy(EvaluatorBase):
    """MEDSTD-based trading strategy.

    Replaces the following files:
    - EvaluatorMEDSTDOptimiz01 through EvaluatorMEDSTDOptimiz10
    - EvaluatorMEDSTDRelative01 through EvaluatorMEDSTDRelative04OnlyUP
    - EvaluatorMEDSTD_WEEK_Optimiz01 through _WEEK_MEDDIFF_01
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)

        # Default parameters
        self.period = self.get_param('period', 20)
        self.min_diff = self.get_param('min_diff', 0.5)
        self.use_week = self.get_param('use_week', False)
        self.relative = self.get_param('relative', False)
        self.only_up = self.get_param('only_up', False)

    def evaluate(self, data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Evaluate MEDSTD conditions.

        Args:
            data: DataFrame with market data
            context: Additional context

        Returns:
            EvaluationResult with trading signals
        """
        if len(data) == 0:
            return EvaluationResult()

        # Calculate or retrieve MEDSTD
        medstd = self._get_medstd(data)

        if medstd is None:
            return EvaluationResult()

        # Check configured conditions
        open_conditions = self.conditions.get('open', [])
        close_conditions = self.conditions.get('close', [])

        should_open = self.check_conditions(open_conditions, data, context) if open_conditions else False
        should_close = self.check_conditions(close_conditions, data, context) if close_conditions else False

        # Fallback logic if no conditions configured
        if not open_conditions:
            should_open = medstd > self.min_diff

        if not close_conditions:
            should_close = medstd <= self.min_diff

        # Apply OnlyUp filter
        if should_open and self.only_up:
            should_open = self._check_only_up_condition(data)

        # Calculate confidence
        confidence = min(medstd, 1.0) if medstd else 0.0

        metadata = {
            'medstd': medstd,
            'min_diff': self.min_diff,
            'period': self.period,
            'only_up': self.only_up,
            'open_conditions_met': should_open,
            'close_conditions_met': should_close
        }

        return EvaluationResult(
            should_open=should_open,
            should_close=should_close,
            confidence=confidence,
            metadata=metadata
        )

    def _get_medstd(self, data: pd.DataFrame) -> Optional[float]:
        """Calculate MEDSTD (mean/std) value.

        Args:
            data: DataFrame with market data

        Returns:
            MEDSTD value or None
        """
        # Try to get from data first
        if 'medstd' in data.columns and len(data) > 0:
            return data['medstd'].iloc[-1]

        # Calculate from Close prices
        if 'Close' not in data.columns or len(data) < self.period:
            return None

        recent = data['Close'].tail(self.period)
        mean = recent.mean()
        std = recent.std()

        if mean == 0 or std == 0:
            return 0.0

        if self.relative:
            return std / mean

        return std

    def _check_only_up_condition(self, data: pd.DataFrame) -> bool:
        """Check if trend is positive.

        Args:
            data: DataFrame with market data

        Returns:
            True if trend is positive
        """
        if len(data) < 2:
            return False

        current = data['Close'].iloc[-1]
        past = data['Close'].iloc[-2]

        return current > past
