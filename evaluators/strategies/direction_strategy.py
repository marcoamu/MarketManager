"""
Direction-based strategy implementation.
Replaces: EvaluatorDIRECTION_*.py (15 files)
"""
import pandas as pd
from typing import Dict, Any, Optional

from ..base.evaluator_base import EvaluatorBase, EvaluationResult
from ..factory import register_evaluator


@register_evaluator('direction')
class DirectionStrategy(EvaluatorBase):
    """Direction-based trading strategy.

    Replaces the following files:
    - EvaluatorDIRECTION_CLEAN_Opt01 through _Opt05
    - EvaluatorDIRECTION_MEDSTD_01 through _04
    - EvaluatorDirectionMEDSTD01 through _04
    - EvaluatorDIRECTION_PROB_Opt01, _Opt02
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)

        # Default parameters
        self.use_medstd = self.get_param('use_medstd', True)
        self.medstd_min_diff = self.get_param('medstd_min_diff', 0.5)
        self.use_probability = self.get_param('use_probability', False)
        self.direction_threshold = self.get_param('direction_threshold', 0.0)

    def evaluate(self, data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Evaluate direction conditions.

        Args:
            data: DataFrame with market data and direction indicators
            context: Additional context

        Returns:
            EvaluationResult with trading signals
        """
        if len(data) == 0:
            return EvaluationResult()

        # Check configured conditions
        open_conditions = self.conditions.get('open', [])
        close_conditions = self.conditions.get('close', [])

        should_open = self.check_conditions(open_conditions, data, context) if open_conditions else False
        should_close = self.check_conditions(close_conditions, data, context) if close_conditions else False

        # Fallback: check direction indicators if no conditions configured
        if not open_conditions and not should_open:
            should_open = self._check_direction_open(data)

        if not close_conditions and not should_close:
            should_close = self._check_direction_close(data)

        # Calculate confidence
        confidence = self._calculate_confidence(data)

        metadata = {
            'use_medstd': self.use_medstd,
            'medstd_min_diff': self.medstd_min_diff,
            'use_probability': self.use_probability,
            'open_conditions_met': should_open,
            'close_conditions_met': should_close
        }

        # Add direction values
        if 'direction' in data.columns:
            metadata['direction'] = data['direction'].iloc[-1]
        if 'week_flow' in data.columns:
            metadata['week_flow'] = data['week_flow'].iloc[-1]

        return EvaluationResult(
            should_open=should_open,
            should_close=should_close,
            confidence=confidence,
            metadata=metadata
        )

    def _check_direction_open(self, data: pd.DataFrame) -> bool:
        """Check if open condition based on direction is met.

        Args:
            data: DataFrame with market data

        Returns:
            True if open condition is met
        """
        if 'direction' not in data.columns or len(data) == 0:
            return False

        direction = data['direction'].iloc[-1]

        # Check if direction is positive and above threshold
        if direction > self.direction_threshold:
            # Check MEDSTD filter if enabled
            if self.use_medstd:
                return self._check_medstd_condition(data)
            return True

        return False

    def _check_direction_close(self, data: pd.DataFrame) -> bool:
        """Check if close condition based on direction is met.

        Args:
            data: DataFrame with market data

        Returns:
            True if close condition is met
        """
        if 'direction' not in data.columns or len(data) == 0:
            return False

        direction = data['direction'].iloc[-1]

        # Close if direction is negative
        return direction < 0

    def _check_medstd_condition(self, data: pd.DataFrame) -> bool:
        """Check MEDSTD (mean/std) condition.

        Args:
            data: DataFrame with market data

        Returns:
            True if MEDSTD condition is met
        """
        # Look for MEDSTD indicator or calculate from available data
        if 'medstd' in data.columns and len(data) > 0:
            medstd = data['medstd'].iloc[-1]
            return medstd > self.medstd_min_diff

        # Calculate from Close prices if available
        if 'Close' in data.columns and len(data) >= 20:
            recent = data['Close'].tail(20)
            mean = recent.mean()
            std = recent.std()
            if mean != 0:
                medstd = std / mean
                return medstd > self.medstd_min_diff

        return True  # Pass through if can't calculate

    def _calculate_confidence(self, data: pd.DataFrame) -> float:
        """Calculate confidence based on direction strength.

        Args:
            data: DataFrame with market data

        Returns:
            Confidence value between 0.0 and 1.0
        """
        if 'direction' not in data.columns or len(data) == 0:
            return 0.0

        direction = abs(data['direction'].iloc[-1])
        confidence = min(direction / 10, 1.0)  # Scale, cap at 1.0

        return confidence
