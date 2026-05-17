"""
TimeManager - Gestión de tiempo y horarios del mercado.
Extraído de MarketManager.py para mejorar mantenibilidad.
"""

import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class TimeIntervals:
    """Intervalos de tiempo para diferentes momentos del día."""
    closeStart: int
    closeEnd: int
    iniStart: int
    iniEnd: int
    normalIntervalStart: int
    normalIntervalEnd: int
    prepRelStart: int
    prepRelEnd: int
    closeAnalisisIntervalStart: Optional[int] = None
    closeAnalisisIntervalEnd: Optional[int] = None


class TimeManager:
    """Gestión de horarios y季节 (temporadas) del mercado."""

    # Presets de intervalos para diferentes temporadas
    PRESETS = {
        'default': TimeIntervals(
            closeStart=2050,
            closeEnd=2055,
            iniStart=1430,
            iniEnd=1435,
            normalIntervalStart=1500,
            normalIntervalEnd=1505,
            prepRelStart=1420,
            prepRelEnd=1430,
            closeAnalisisIntervalStart=2050,
            closeAnalisisIntervalEnd=2055,
        ),
        '1430': TimeIntervals(
            closeStart=2040,
            closeEnd=2100,
            iniStart=1430,
            iniEnd=1500,
            normalIntervalStart=1600,
            normalIntervalEnd=1605,
            prepRelStart=1430,
            prepRelEnd=1500,
            closeAnalisisIntervalStart=2040,
            closeAnalisisIntervalEnd=2100,
        ),
        'invierno': TimeIntervals(
            closeStart=2140,
            closeEnd=2200,
            iniStart=1530,
            iniEnd=1600,
            normalIntervalStart=1600,
            normalIntervalEnd=1605,
            prepRelStart=1530,
            prepRelEnd=1600,
            closeAnalisisIntervalStart=2140,
            closeAnalisisIntervalEnd=2200,
        ),
        'verano': TimeIntervals(
            closeStart=2140,
            closeEnd=2200,
            iniStart=1530,
            iniEnd=1550,
            normalIntervalStart=1600,
            normalIntervalEnd=1605,
            prepRelStart=1530,
            prepRelEnd=1550,
            closeAnalisisIntervalStart=2140,
            closeAnalisisIntervalEnd=2200,
        ),
    }

    def __init__(self, preset: str = 'default'):
        self.set_preset(preset)
        self.name = "M3_15min"
        self.intervalTime = 15

    def set_preset(self, preset: str = 'default'):
        """Establece el preset de intervalos."""
        if preset not in self.PRESETS:
            preset = 'default'
        intervals = self.PRESETS[preset]
        self.closeStart = intervals.closeStart
        self.closeEnd = intervals.closeEnd
        self.iniStart = intervals.iniStart
        self.iniEnd = intervals.iniEnd
        self.normalIntervalStart = intervals.normalIntervalStart
        self.normalIntervalEnd = intervals.normalIntervalEnd
        self.prepRelStart = intervals.prepRelStart
        self.prepRelEnd = intervals.prepRelEnd
        if intervals.closeAnalisisIntervalStart:
            self.closeAnalisisIntervalStart = intervals.closeAnalisisIntervalStart
        if intervals.closeAnalisisIntervalEnd:
            self.closeAnalisisIntervalEnd = intervals.closeAnalisisIntervalEnd

    def prepare1430(self):
        """Configuración para horario 1430."""
        self.set_preset('1430')

    def prepareInvierno(self):
        """Configuración para invierno."""
        self.set_preset('invierno')

    def prepareVerano(self):
        """Configuración para verano."""
        self.set_preset('verano')

    def get_current_time(self) -> int:
        """Obtiene la hora actual como entero (HHMM)."""
        t = time.localtime()
        current_time_h = time.strftime("%H", t)
        current_time_min = time.strftime("%M", t)
        return int(current_time_h + current_time_min)

    def is_in_initial_window(self, current_time: Optional[int] = None) -> bool:
        """Verifica si está en la ventana inicial (apertura)."""
        if current_time is None:
            current_time = self.get_current_time()
        return int(self.iniStart) <= current_time < int(self.iniEnd)

    def is_in_normal_window(self, current_time: Optional[int] = None) -> bool:
        """Verifica si está en la ventana normal (horario regular)."""
        if current_time is None:
            current_time = self.get_current_time()
        return int(self.normalIntervalStart) <= current_time < int(self.normalIntervalEnd)

    def is_in_close_window(self, current_time: Optional[int] = None) -> bool:
        """Verifica si está en la ventana de cierre."""
        if current_time is None:
            current_time = self.get_current_time()
        return int(self.closeStart) <= current_time < int(self.closeEnd)

    def get_market_period(self, current_time: Optional[int] = None) -> str:
        """Retorna el período actual del mercado: 'initial', 'normal', 'close'."""
        if current_time is None:
            current_time = self.get_current_time()

        if self.is_in_initial_window(current_time):
            return 'initial'
        elif self.is_in_close_window(current_time):
            return 'close'
        elif self.is_in_normal_window(current_time):
            return 'normal'
        else:
            return 'outside_hours'

    def get_interval(self, current_time: Optional[int] = None) -> int:
        """Obtiene el intervalo recomendado según el horario."""
        if current_time is None:
            current_time = self.get_current_time()

        if self.is_in_initial_window(current_time):
            return 5  # Intervalo de 5 minutos en apertura
        elif self.is_in_close_window(current_time):
            return 10  # Intervalo de 10 minutos en cierre
        else:
            return self.intervalTime  # Intervalo normal
