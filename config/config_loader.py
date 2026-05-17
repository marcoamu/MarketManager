"""
YAML Config Loader - Carga configuraciones de activos desde archivos YAML.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class ConfigLoader:
    """Cargador de configuraciones YAML para activos."""

    DEFAULT_CONFIG_DIR = Path(__file__).parent / "actives"

    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir) if config_dir else self.DEFAULT_CONFIG_DIR
        self._cache: Dict[str, Dict] = {}

    def load(self, symbol: str) -> Dict[str, Any]:
        """
        Carga configuración para un símbolo.

        Args:
            symbol: Símbolo del activo (ej: 'AAPL', 'NVDA')

        Returns:
            Diccionario con configuración
        """
        # Buscar en caché
        if symbol in self._cache:
            return self._cache[symbol]

        # Buscar archivo
        filename = f"{symbol.upper()}.yaml"
        filepath = self.config_dir / filename

        if not filepath.exists():
            return self._get_default_config(symbol)

        # Cargar archivo
        with open(filepath, 'r') as f:
            config = yaml.safe_load(f)

        # Guardar en caché
        self._cache[symbol] = config
        return config

    def load_all(self) -> Dict[str, Dict]:
        """Carga todas las configuraciones disponibles."""
        configs = {}

        for filepath in self.config_dir.glob("*.yaml"):
            symbol = filepath.stem
            configs[symbol] = self.load(symbol)

        return configs

    def save(self, symbol: str, config: Dict[str, Any]):
        """Guarda configuración para un símbolo."""
        filename = f"{symbol.upper()}.yaml"
        filepath = self.config_dir / filename

        with open(filepath, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)

        # Actualizar caché
        self._cache[symbol] = config

    def _get_default_config(self, symbol: str) -> Dict[str, Any]:
        """Retorna configuración por defecto."""
        return {
            'name': symbol,
            'description': f'Configuración para {symbol}',
            'parameters': {
                'difference': 0.25,
                'accumulate': 0.5,
                'unit': 0.06,
                'draw': False,
                'round': 2,
                'ima1': 5,
                'ima2': 10,
                'ima3': 20,
                'ima4': 50,
                'bollinger': 20,
                'ema10': 10,
                'ema20': 20,
                'weekend': False,
                'operate': True,
            }
        }

    def clear_cache(self):
        """Limpia la caché."""
        self._cache = {}


# Funciones de conveniencia
_loader: Optional[ConfigLoader] = None


def get_loader(config_dir: Optional[str] = None) -> ConfigLoader:
    """Obtiene instancia global del loader."""
    global _loader
    if _loader is None:
        _loader = ConfigLoader(config_dir)
    return _loader


def load_active_config(symbol: str) -> Dict[str, Any]:
    """Carga configuración de un activo."""
    return get_loader().load(symbol)


def save_active_config(symbol: str, config: Dict[str, Any]):
    """Guarda configuración de un activo."""
    get_loader().save(symbol, config)
