"""
Base evaluator class with common functionality.
Replaces the duplicated code in 252 evaluator files.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import pandas as pd


class EvaluationResult:
    """Result of an evaluation."""
    def __init__(self, should_open: bool = False, should_close: bool = False,
                 confidence: float = 0.0, metadata: Optional[Dict[str, Any]] = None):
        self.should_open = should_open
        self.should_close = should_close
        self.confidence = confidence
        self.metadata = metadata or {}

    def __bool__(self):
        return self.should_open or self.should_close


class EvaluatorBase(ABC):
    """Base class for all evaluators."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize evaluator with configuration.

        Args:
            config: Dictionary with evaluator parameters and conditions
        """
        self.config = config or {}
        self.params = self.config.get('params', {})
        self.conditions = self.config.get('conditions', {})
        self.name = self.config.get('name', self.__class__.__name__)

    @abstractmethod
    def evaluate(self, data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> EvaluationResult:
        """Evaluate market conditions.

        Args:
            data: DataFrame with market data and indicators
            context: Additional context (positions, account info, etc.)

        Returns:
            EvaluationResult with trading signals
        """
        pass

    def evaluate_open(self, data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> bool:
        """Evaluate if position should be opened.

        Args:
            data: DataFrame with market data and indicators
            context: Additional context

        Returns:
            True if position should be opened
        """
        result = self.evaluate(data, context)
        return result.should_open

    def evaluate_close(self, data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> bool:
        """Evaluate if position should be closed.

        Args:
            data: DataFrame with market data and indicators
            context: Additional context

        Returns:
            True if position should be closed
        """
        result = self.evaluate(data, context)
        return result.should_close

    def check_conditions(self, conditions: List[Dict[str, Any]],
                        data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> bool:
        """Check if all conditions are met.

        Args:
            conditions: List of condition dictionaries with 'indicator', 'op', 'value'
            data: DataFrame with market data
            context: Additional context

        Returns:
            True if all conditions are met
        """
        for condition in conditions:
            if not self._evaluate_condition(condition, data, context):
                return False
        return True

    def _evaluate_condition(self, condition: Dict[str, Any],
                           data: pd.DataFrame, context: Optional[Dict[str, Any]] = None) -> bool:
        """Evaluate a single condition.

        Args:
            condition: Dictionary with 'indicator', 'op', 'value'
            data: DataFrame with market data
            context: Additional context

        Returns:
            True if condition is met
        """
        indicator = condition.get('indicator')
        op = condition.get('op', '==')
        value = condition.get('value')

        # Get indicator value from data
        if indicator in data.columns:
            indicator_value = data[indicator].iloc[-1] if len(data) > 0 else None
        elif context and indicator in context:
            indicator_value = context[indicator]
        else:
            return False

        # Handle special operators
        if op == '==':
            return indicator_value == value
        elif op == '!=':
            return indicator_value != value
        elif op == '>':
            return indicator_value > value if indicator_value is not None else False
        elif op == '<':
            return indicator_value < value if indicator_value is not None else False
        elif op == '>=':
            return indicator_value >= value if indicator_value is not None else False
        elif op == '<=':
            return indicator_value <= value if indicator_value is not None else False
        elif op == 'in':
            return indicator_value in value if isinstance(value, (list, tuple)) else False

        return False

    def get_param(self, name: str, default: Any = None) -> Any:
        """Get a parameter value."""
        return self.params.get(name, default)

    def get_indicator_value(self, data: pd.DataFrame, indicator: str, default: Any = None) -> Any:
        """Get the last value of an indicator from data."""
        if indicator in data.columns and len(data) > 0:
            return data[indicator].iloc[-1]
        return default
