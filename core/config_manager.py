"""
ConfigManager - Gestión de configuración del sistema.
Extraído de MarketManager.py para mejorar mantenibilidad.
"""

import configparser
import platform
from pathlib import Path
from typing import Optional


class ConfigManager:
    """Manejo de configuración centralizado."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_obj = configparser.ConfigParser()
        self.config_path = config_path
        self.env = self._detect_environment()
        self._load_config()

    def _detect_environment(self) -> str:
        """Detecta el entorno de ejecución (Windows/Linux)."""
        config = configparser.ConfigParser()
        config.read('config.ini')
        try:
            return config['DEFAULT']['DEF_CONF']
        except Exception:
            sistema = platform.system()
            if sistema == "Windows":
                return "WINDOWS"
            else:
                return "LINUX"

    def _load_config(self):
        """Carga la configuración desde el archivo."""
        if self.config_path is None:
            self.config_path = self._get_default_config_path()
        self.config_obj.read(self.config_path)

    def _get_default_config_path(self) -> str:
        """Retorna el path por defecto según el SO."""
        if "WINDOWS" in self.env:
            return r"F:\WORK\2026\MarketManager\config\config.ini"
        else:
            return "/home/MarketManager/config/config.ini"

    def get(self, section: str, key: str, fallback: Optional[str] = None) -> Optional[str]:
        """Obtiene un valor de configuración."""
        try:
            return self.config_obj.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback

    def set(self, section: str, key: str, value: str):
        """Establece un valor de configuración."""
        if not self.config_obj.has_section(section):
            self.config_obj.add_section(section)
        self.config_obj.set(section, key, value)

    def write(self):
        """Guarda la configuración al archivo."""
        with open(self.config_path, 'w') as configfile:
            self.config_obj.write(configfile)

    def get_active_config(self, active_name: str) -> dict:
        """Obtiene la configuración completa para un activo."""
        try:
            section = self.config_obj[active_name]
            return dict(section)
        except configparser.NoSectionError:
            return {}

    def update_active_config(self, active_name: str, updates: dict):
        """Actualiza la configuración de un activo."""
        self.set(active_name, 'value', updates.get('value', '0'))
        self.set(active_name, 'action', updates.get('action', 'WAIT'))
        self.set(active_name, 'action_acum', updates.get('action_acum', '0'))
        self.set(active_name, 'action_count', updates.get('action_count', '0'))
        self.set(active_name, 'min', updates.get('min', '99999'))
        self.set(active_name, 'max', updates.get('max', '0'))
        self.set(active_name, 'direction', updates.get('direction', 'DIR_WAIT'))
        self.set(active_name, 'min_dir', updates.get('min_dir', '99999'))
        self.set(active_name, 'max_dir', updates.get('max_dir', '0'))
        self.set(active_name, 'flujo', updates.get('flujo', 'NONE'))
        self.write()

    def get_path(self) -> str:
        """Retorna el path de configuración actual."""
        return self.config_path
