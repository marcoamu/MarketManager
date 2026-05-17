"""
IBLG (Indicator Bollinger) strategy implementation.
Replaces: EvaluatorIBLG_*.py (45+ files)
"""
import pandas as pd
from typing import Dict, Any, Optional

from ..base.evaluator_base import EvaluatorBase, EvaluationResult
from ..factory import register_evaluator


@register_evaluator('iblg')
class IBLGStrategy(EvaluatorBase):
    """IBLG-based trading strategy.

    Replaces the following files:
    - EvaluatorIBLG_ANGLE_FLOW_01, _02
    - EvaluatorIBLG_ANGLE_FLOW_LONG_01 through _06
    - EvaluatorIBLG_ANGLE_ONLY_UP_00 through _05_test08
    - EvaluatorIBLG_LONG_00 through _09
    - EvaluatorIBLG_LONG_ANGLE_ONLY_UP_01 through _03
    - EvaluatorIBLG_LONG_ONLY_UP_00 through _08
    - EvaluatorIBLG_MID_LONG_01, _02
    - EvaluatorIBLG_PROB_FLOW_01, _02
    - EvaluatorIBLG_START_CLOSE_01 through _05
    - EvaluatorIBLG_WEEK_FLOW_01 through _03
    - EvaluatorIBLG_WEEK_TOP_ONLY_UP_01 through _04
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)

        # Default parameters
        self.use_angle = self.get_param('use_angle', False)
        self.angle_up = self.get_param('angle_up', 2.0)
        self.angle_down = self.get_param('angle_down', 2.0)
        self.use_flow = self.get_param('use_flow', False)
        self.use_week = self.get_param('use_week', False)
        self.only_up = self.get_param('only_up', False)
        self.use_probability = self.get_param('use_probability', False)

    def evaluate(self, data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Evaluate IBLG conditions.

        Args:
            data: DataFrame with market data and IBLG indicators
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

        # Fallback logic
        if not open_conditions:
            should_open = self._check_iblg_open(data)

        if not close_conditions:
            should_close = self._check_iblg_close(data)

        # Apply OnlyUp filter
        if should_open and self.only_up:
            should_open = self._check_only_up_condition(data)

        # Calculate confidence
        confidence = self._calculate_confidence(data)

        metadata = {
            'use_angle': self.use_angle,
            'angle_up': self.angle_up,
            'angle_down': self.angle_down,
            'use_flow': self.use_flow,
            'use_week': self.use_week,
            'only_up': self.only_up,
            'open_conditions_met': should_open,
            'close_conditions_met': should_close
        }

        # Add indicator values if available
        if 'iblg_angle' in data.columns:
            metadata['iblg_angle'] = data['iblg_angle'].iloc[-1]

        return EvaluationResult(
            should_open=should_open,
            should_close=should_close,
            confidence=confidence,
            metadata=metadata
        )

    def _check_iblg_open(self, data: pd.DataFrame) -> bool:
        """Check IBLG open condition.

        Args:
            data: DataFrame with market data

        Returns:
            True if open condition is met
        """
        if self.use_angle:
            return self._check_angle_condition(data, bullish=True)

        return False

    def _check_iblg_close(self, data: pd.DataFrame) -> bool:
        """Check IBLG close condition.

        Args:
            data: DataFrame with market data

        Returns:
            True if close condition is met
        """
        if self.use_angle:
            return self._check_angle_condition(data, bullish=False)

        return False

    def _check_angle_condition(self, data: pd.DataFrame, bullish: bool = True) -> bool:
        """Check angle condition.

        Args:
            data: DataFrame with market data
            bullish: If True, check for positive angle

        Returns:
            True if angle condition is met
        """
        if 'iblg_angle' not in data.columns or len(data) == 0:
            return False

        angle = data['iblg_angle'].iloc[-1]

        if bullish:
            return angle > self.angle_up
        else:
            return angle < -self.angle_down

    def _check_only_up_condition(self, data: pd.DataFrame) -> bool:
        """Check if trend is positive.

        Args:
            data: DataFrame with market data

        Returns:
            True if trend is positive
        """
        if 'week_flow' in data.columns:
            flow = data['week_flow'].iloc[-1]
            return flow == 'WEEK_FLOW_UP'

        if len(data) < 2:
            return False

        return data['Close'].iloc[-1] > data['Close'].iloc[-2]

    def _calculate_confidence(self, data: pd.DataFrame) -> float:
        """Calculate confidence.

        Args:
            data: DataFrame with market data

        Returns:
            Confidence value between 0.0 and 1.0
        """
        if 'iblg_angle' in data.columns and len(data) > 0:
            angle = abs(data['iblg_angle'].iloc[-1])
            confidence = min(angle / 10, 1.0)
            return confidence

        return 0.0
