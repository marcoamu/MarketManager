"""
ActiveHelper refactored to use the new evaluator factory pattern.
Replaces the 200+ static imports with dynamic evaluator creation.
"""
import datetime
import time
from typing import List, Optional, Dict, Any
from pathlib import Path

from service.Active import Active
from service.Parameters import Parameters
from evaluators.factory import EvaluatorFactory
from core.config import get_config
import copy


class ActiveHelper:
    """Helper class for creating and configuring trading actives.

    This refactored version uses the evaluator factory pattern
    instead of static imports for all 252 evaluators.
    """

    # Evaluator configuration mappings
    _EVALUATOR_CONFIGS: Dict[str, Dict[str, Any]] = {
        # Bollinger evaluators
        'BOLLINGER_00': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 70}},
        'BOLLINGER_01': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 75}},
        'BOLLINGER_02': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 80}},
        'BOLLINGER_03': {'base_strategy': 'bollinger', 'params': {'blg_dist_percent': 85}},
        'BOLLINGER_ONLY_UP_03': {'base_strategy': 'bollinger', 'params': {'only_up': True, 'blg_dist_percent': 80}},

        # EMA evaluators
        'EMA_01': {'base_strategy': 'ema', 'params': {'ema_short': 10, 'ema_long': 20}},
        'EMA_LONG_01': {'base_strategy': 'ema', 'params': {'ema_short': 10, 'ema_long': 20, 'only_up': True}},

        # Direction evaluators
        'DIRECTION_MEDSTD_03': {'base_strategy': 'direction', 'params': {'use_medstd': True, 'medstd_min_diff': 0.7}},

        # OnlyUp evaluators
        'ONLY_UP_01': {'base_strategy': 'only_up', 'params': {'uptrend_threshold': 0.0}},

        # MEDSTD evaluators
        'MEDSTD_01': {'base_strategy': 'medstd', 'params': {'min_diff': 0.5}},

        # IBLG evaluators
        'IBLG_LONG_01': {'base_strategy': 'iblg', 'params': {'use_angle': True, 'angle_up': 2.0}},
    }

    # Asset parameter mappings (replaces 90+ Param*.py files)
    _ASSET_DEFAULTS: Dict[str, Dict[str, Any]] = {
        # === ACCIONES TECH ===
        'AAPL': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'BOLLINGER_ONLY_UP_03'
        },
        'MSFT': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'EMA_LONG_01'
        },
        'GOOG': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'DIRECTION_MEDSTD_03'
        },
        'AMZN': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'BOLLINGER_03'
        },
        'NVDA': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'BOLLINGER_ONLY_UP_03'
        },
        'META': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'DIRECTION_MEDSTD_03'
        },
        'TSLA': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'EMA_LONG_01'
        },
        # === ENTRETENIMIENTO ===
        'NFLX': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'ONLY_UP_01'
        },
        'DIS': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'EMA_01'
        },
        # === SEMICONDUCTORES ===
        'AMD': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'IBLG_LONG_01'
        },
        'INTC': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'BOLLINGER_00'
        },
        # === CONSUMO ===
        'KO': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'ONLY_UP_01'
        },
        'MCD': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'EMA_LONG_01'
        },
        'SBUX': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'BOLLINGER_02'
        },
        'HD': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'DIRECTION_MEDSTD_03'
        },
        # === OTROS ===
        'VTI': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'EMA_01'
        },
        'GLD': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'EMA_LONG_01'
        },
        'BABA': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'BOLLINGER_ONLY_UP_03'
        },
        'SONY': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.10,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'MEDSTD_01'
        },
        # === CRIPTOMONEDAS ===
        'BTC': {
            'difference': 1.0,
            'accumulate': 1.0,
            'unit': 0.001,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'IBLG_LONG_01'
        },
        'ETH': {
            'difference': 0.50,
            'accumulate': 1.0,
            'unit': 0.01,
            'bollinger_period': 20,
            'ema_short': 10,
            'ema_long': 20,
            'evaluator': 'MEDSTD_01'
        },
    }

    def __init__(self, simulation: bool = False, isDBData: bool = False):
        """Initialize ActiveHelper.

        Args:
            simulation: Whether to use simulation mode
            isDBData: Whether data comes from database
        """
        self.simulation = simulation
        self.isDBData = isDBData
        self._config = get_config()

    def create_evaluator(self, evaluator_name: str) -> Any:
        """Create an evaluator by name using the factory.

        Args:
            evaluator_name: Name of the evaluator configuration

        Returns:
            Evaluator instance
        """
        if evaluator_name in self._EVALUATOR_CONFIGS:
            config = self._EVALUATOR_CONFIGS[evaluator_name].copy()
            config['name'] = evaluator_name
            return EvaluatorFactory.create_from_dict(config)

        # Try to load from config file
        config_path = Path(f"evaluators/config/{evaluator_name.lower().replace('_', '/')}.json")
        if config_path.exists():
            return EvaluatorFactory.create(str(config_path))

        raise ValueError(f"Unknown evaluator: {evaluator_name}")

    def get_asset_params(self, symbol: str, variant: Optional[str] = None) -> Dict[str, Any]:
        """Get default parameters for an asset.

        Args:
            symbol: Asset symbol (e.g., 'AAPL', 'BTC')
            variant: Optional variant name for different configurations

        Returns:
            Dictionary with asset parameters
        """
        # Clean symbol (remove /USD for crypto)
        base_symbol = symbol.replace('/', '').replace('USD', '') if 'USD' in symbol else symbol

        # Get defaults
        defaults = self._ASSET_DEFAULTS.get(base_symbol, self._ASSET_DEFAULTS.get(symbol, {}))

        # Apply variant if specified (e.g., 'AAPL_01', 'AAPL_02')
        if variant:
            # Look for variant-specific overrides in YAML configs
            yaml_path = Path(f"config/actives/{symbol.lower()}{variant}.yaml")
            if yaml_path.exists():
                import yaml
                with open(yaml_path) as f:
                    variant_config = yaml.safe_load(f)
                    defaults.update(variant_config.get('parameters', {}))

        return copy.deepcopy(defaults)

    def create_active(self, symbol: str, params: Optional[Dict[str, Any]] = None,
                     evaluator_name: Optional[str] = None) -> Active:
        """Create an Active instance with configuration.

        Args:
            symbol: Asset symbol
            params: Optional parameter overrides
            evaluator_name: Optional specific evaluator to use

        Returns:
            Configured Active instance
        """
        # Get default params
        default_params = self.get_asset_params(symbol)

        # Merge with provided params
        if params:
            default_params.update(params)

        # Override evaluator if specified
        if evaluator_name:
            default_params['evaluator'] = evaluator_name

        # Create the Active
        active = Active(symbol, **default_params)

        # Create and assign the evaluator
        if 'evaluator' in default_params:
            evaluator = self.create_evaluator(default_params['evaluator'])
            active.evaluator = evaluator

        return active

    def prepareActives(self, skipDayControl: bool = False) -> List[Active]:
        """Prepare the list of active trading assets.

        Args:
            skipDayControl: Whether to skip day control checks

        Returns:
            List of configured Active instances
        """
        actives = []

        # Tech stocks (high priority - optimized)
        actives.append(self.prepareNVDA())
        actives.append(self.prepareMSFT())
        actives.append(self.prepareAAPL())
        actives.append(self.prepareGOOG())
        actives.append(self.prepareMETA())

        # Entertainment
        actives.append(self.prepareNFLX())
        actives.append(self.prepareDIS())

        # Semiconductors
        actives.append(self.prepareAMD())
        actives.append(self.prepareINTC())

        # Consumer
        actives.append(self.prepareKO())
        actives.append(self.prepareMCD())
        actives.append(self.prepareSBUX())
        actives.append(self.prepareHD())

        # Other
        actives.append(self.prepareAMZN())
        actives.append(self.prepareBABA())
        actives.append(self.prepareSONY())
        actives.append(self.prepareVTI())

        # Crypto
        actives.append(self.prepareBTC())
        actives.append(self.prepareETH())

        # Commodities
        actives.append(self.prepareGLD())

        # Additional
        actives.append(self.prepareTSLA())

        return actives

    def prepareAllActives(self) -> List[Active]:
        """Prepare ALL available actives for maximum coverage."""
        actives = []

        # Tech
        for symbol in ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA']:
            actives.append(self.create_active(symbol))

        # Entertainment
        for symbol in ['NFLX', 'DIS']:
            actives.append(self.create_active(symbol))

        # Semiconductors
        for symbol in ['AMD', 'INTC']:
            actives.append(self.create_active(symbol))

        # Consumer
        for symbol in ['KO', 'MCD', 'SBUX', 'HD']:
            actives.append(self.create_active(symbol))

        # Other
        for symbol in ['VTI', 'BABA', 'SONY']:
            actives.append(self.create_active(symbol))

        # Crypto
        for symbol in ['BTC', 'ETH']:
            actives.append(self.create_active(symbol))

        # Commodities
        actives.append(self.create_active('GLD'))

        return actives

    # Convenience methods for backward compatibility
    def prepareAAPL7(self) -> Active:
        """Prepare AAPL variant 7."""
        return self.create_active('AAPL', {'evaluator': 'BOLLINGER_ONLY_UP_03'})

    def prepareTSLA02(self) -> Active:
        """Prepare TSLA variant 2."""
        return self.create_active('TSLA', {'evaluator': 'EMA_LONG_01'})

    def prepareBTC3(self) -> Active:
        """Prepare BTC variant 3."""
        return self.create_active('BTCUSD', {'evaluator': 'IBLG_LONG_01'})

    def prepareETH2(self) -> Active:
        """Prepare ETH variant 2."""
        return self.create_active('ETHUSD', {'evaluator': 'MEDSTD_01'})

    def prepareNVDA06(self) -> Active:
        """Prepare NVDA variant 6."""
        return self.create_active('NVDA', {'evaluator': 'BOLLINGER_ONLY_UP_03'})

    def prepareMSFT04(self) -> Active:
        """Prepare MSFT variant 4."""
        return self.create_active('MSFT', {'evaluator': 'EMA_LONG_01'})

    def prepareGOOG5(self) -> Active:
        """Prepare GOOG variant 5."""
        return self.create_active('GOOG', {'evaluator': 'DIRECTION_MEDSTD_03'})

    def prepareNFLX5(self) -> Active:
        """Prepare NFLX variant 5."""
        return self.create_active('NFLX', {'evaluator': 'ONLY_UP_01'})

    def prepareAMZN4(self) -> Active:
        """Prepare AMZN variant 4."""
        return self.create_active('AMZN', {'evaluator': 'BOLLINGER_03'})

    def prepareDIS08(self) -> Active:
        """Prepare DIS variant 8."""
        return self.create_active('DIS', {'evaluator': 'EMA_01'})

    def prepareINTC(self) -> Active:
        """Prepare INTC."""
        return self.create_active('INTC', {'evaluator': 'BOLLINGER_00'})

    def prepareMCD02(self) -> Active:
        """Prepare MCD variant 2."""
        return self.create_active('MCD', {'evaluator': 'EMA_LONG_01'})

    def prepareMETA02(self) -> Active:
        """Prepare META variant 2."""
        return self.create_active('META', {'evaluator': 'DIRECTION_MEDSTD_03'})

    def prepareKO3(self) -> Active:
        """Prepare KO variant 3."""
        return self.create_active('KO', {'evaluator': 'ONLY_UP_01'})

    def prepareSBUX(self) -> Active:
        """Prepare SBUX."""
        return self.create_active('SBUX', {'evaluator': 'BOLLINGER_02'})

    def prepareVTI02(self) -> Active:
        """Prepare VTI variant 2."""
        return self.create_active('VTI', {'evaluator': 'EMA_01'})

    def prepareHD01(self) -> Active:
        """Prepare HD variant 1."""
        return self.create_active('HD', {'evaluator': 'DIRECTION_MEDSTD_03'})

    def prepareAMD06(self) -> Active:
        """Prepare AMD variant 6."""
        return self.create_active('AMD', {'evaluator': 'IBLG_LONG_01'})

    def prepareSONY03(self) -> Active:
        """Prepare SONY variant 3."""
        return self.create_active('SONY', {'evaluator': 'MEDSTD_01'})

    def prepareBABA02(self) -> Active:
        """Prepare BABA variant 2."""
        return self.create_active('BABA', {'evaluator': 'BOLLINGER_ONLY_UP_03'})

    def prepareGLD(self) -> Active:
        """Prepare GLD."""
        return self.create_active('GLD', {'evaluator': 'EMA_LONG_01'})

    # Alias methods for compatibility
    def prepareAAPL(self) -> Active:
        return self.prepareAAPL7()

    def prepareTSLA(self) -> Active:
        return self.prepareTSLA02()

    def prepareBTC(self) -> Active:
        return self.prepareBTC3()

    def prepareETH(self) -> Active:
        return self.prepareETH2()

    def prepareNVDA(self) -> Active:
        return self.prepareNVDA06()

    def prepareMSFT(self) -> Active:
        return self.prepareMSFT04()

    def prepareGOOG(self) -> Active:
        return self.prepareGOOG5()

    def prepareNFLX(self) -> Active:
        return self.prepareNFLX5()

    def prepareAMZN(self) -> Active:
        return self.prepareAMZN4()

    def prepareDIS(self) -> Active:
        return self.prepareDIS08()

    def prepareMCD(self) -> Active:
        return self.prepareMCD02()

    def prepareMETA(self) -> Active:
        return self.prepareMETA02()

    def prepareKO(self) -> Active:
        return self.prepareKO3()

    def prepareVTI(self) -> Active:
        return self.prepareVTI02()

    def prepareHD(self) -> Active:
        return self.prepareHD01()

    def prepareAMD(self) -> Active:
        return self.prepareAMD06()

    def prepareSONY(self) -> Active:
        return self.prepareSONY03()

    def prepareBABA(self) -> Active:
        return self.prepareBABA02()

    # For drawing
    def prepareActiveForDraw(self) -> List[Active]:
        """Prepare actives for visualization/drawing."""
        actives = []
        actives.append(self.prepareAAPL())
        actives.append(self.prepareDIS())
        actives.append(self.prepareAMZN())
        actives.append(self.prepareKO())
        actives.append(self.prepareNFLX())
        actives.append(self.prepareTSLA())
        actives.append(self.prepareMSFT())
        actives.append(self.prepareNVDA())
        actives.append(self.prepareGOOG())
        actives.append(self.prepareINTC())
        actives.append(self.prepareMCD())
        actives.append(self.prepareSBUX())
        actives.append(self.prepareMETA())
        actives.append(self.prepareVTI())
        actives.append(self.prepareSONY())
        actives.append(self.prepareBABA())
        actives.append(self.prepareAMD())
        actives.append(self.prepareETH())
        actives.append(self.prepareBTC())
        return actives

    def prepareActivesSimulation(self) -> List[Active]:
        """Prepare actives for simulation."""
        actives = []
        actives.append(self.prepareAAPL())
        return actives
