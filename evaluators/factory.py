"""
Factory pattern for creating evaluators based on configuration.
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Type
from .base.evaluator_base import EvaluatorBase

class EvaluatorFactory:
    """Factory for creating evaluators from configuration files."""
    _strategies: Dict[str, Type[EvaluatorBase]] = {}
    _registry: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str, strategy_class: Type[EvaluatorBase]) -> None:
        """Register a strategy class.

        Args:
            name: Strategy identifier
            strategy_class: Class inheriting from EvaluatorBase
        """
        if not issubclass(strategy_class, EvaluatorBase):
            raise ValueError(f'Strategy {name} must inherit from EvaluatorBase')
        cls._strategies[name] = strategy_class

    @classmethod
    def unregister(cls, name: str) -> None:
        """Unregister a strategy."""
        cls._strategies.pop(name, None)

    @classmethod
    def create(cls, config_path: str) -> EvaluatorBase:
        """Create an evaluator from a configuration file.

        Args:
            config_path: Path to JSON or YAML configuration file

        Returns:
            Configured EvaluatorBase instance

        Raises:
            ValueError: If strategy not registered or config invalid
        """
        config = cls._load_config(config_path)
        base_strategy = config.get('base_strategy')
        if base_strategy not in cls._strategies:
            raise ValueError(f"Strategy '{base_strategy}' not registered. Available: {list(cls._strategies.keys())}")
        strategy_class = cls._strategies[base_strategy]
        return strategy_class(config)

    @classmethod
    def create_from_dict(cls, config: Dict[str, Any]) -> EvaluatorBase:
        """Create an evaluator from a configuration dictionary.

        Args:
            config: Configuration dictionary with 'base_strategy' key

        Returns:
            Configured EvaluatorBase instance
        """
        base_strategy = config.get('base_strategy')
        if base_strategy not in cls._strategies:
            raise ValueError(f"Strategy '{base_strategy}' not registered. Available: {list(cls._strategies.keys())}")
        strategy_class = cls._strategies[base_strategy]
        return strategy_class(config)

    @classmethod
    def _load_config(cls, path: str) -> Dict[str, Any]:
        """Load configuration from file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f'Config file not found: {path}')
        content = path.read_text()
        if path.suffix in ['.yaml', '.yml']:
            return yaml.safe_load(content)
        elif path.suffix == '.json':
            return json.loads(content)
        else:
            raise ValueError(f'Unsupported config format: {path.suffix}')

    @classmethod
    def list_strategies(cls) -> list:
        """List available strategy names."""
        return list(cls._strategies.keys())

    @classmethod
    def get_strategy_class(cls, name: str) -> Optional[Type[EvaluatorBase]]:
        """Get strategy class by name."""
        return cls._strategies.get(name)

def register_evaluator(name: str):
    """Decorator to register an evaluator class.

    Usage:
        @register_evaluator('bollinger')
        class BollingerStrategy(EvaluatorBase):
            ...
    """

    def decorator(cls: Type[EvaluatorBase]):
        EvaluatorFactory.register(name, cls)
        return cls
    return decorator