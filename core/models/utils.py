"""Standalone utility functions for MarketManager - models module."""

import math
import datetime


def calcular_angulo(x1, y1, x2, y2):
    """Calcula el ángulo entre dos puntos."""
    delta_y = y2 - y1
    delta_x = x2 - x1
    angulo_radianes = math.atan2(delta_y, delta_x)
    return math.degrees(angulo_radianes)


def calcular_minutos_entre_fechas(fecha1_str, fecha2_str):
    """Calcula los minutos entre dos fechas."""
    try:
        fecha1 = datetime.datetime.strptime(fecha1_str, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        fecha1 = datetime.datetime.strptime(fecha1_str, "%Y-%m-%d")
    try:
        fecha2 = datetime.datetime.strptime(fecha2_str, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        fecha2 = datetime.datetime.strptime(fecha2_str, "%Y-%m-%d")
    return (fecha2 - fecha1).total_seconds() / 60


def calculate_rsi(data, period=14):
    """Calculate RSI for given data."""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


def determineFlow(min, max, val):
    """Determine flow direction based on value position in range."""
    if max == min:
        return 0, 0, 0, 0
    percent = ((val - min) / (max - min)) * 100
    if val >= max:
        res = 2
    elif val <= min:
        res = -2
    else:
        res = -1 if percent < 33 else (1 if percent > 66 else 0)
    dist = ((max - min) / 2) - abs(val - ((max + min) / 2))
    dist_rel = dist / ((max - min) / 2) if (max - min) != 0 else 0
    return res, dist_rel, dist, percent


def calculatePercentFcst(min, max, val):
    """Calculate forecast percentage."""
    if max == min:
        return 0
    return ((val - min) / (max - min)) * 100
