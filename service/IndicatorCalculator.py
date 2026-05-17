import pandas as pd
import numpy as np

class IndicatorCalculator:

    @staticmethod
    def calculate(df: pd.DataFrame) -> dict:
        close = df['close']
        volume = df['volume']

        result = {}

        # Precio actual
        result['price'] = close.iloc[-1]

        # Momentum
        result['momentum_5'] = (close.iloc[-1] / close.iloc[-5] - 1) * 100
        result['momentum_15'] = (close.iloc[-1] / close.iloc[-15] - 1) * 100

        # Velocidad / aceleración
        velocity = close.diff()
        result['velocity'] = velocity.iloc[-1]
        result['acceleration'] = velocity.diff().iloc[-1]

        # Volumen relativo
        result['volume'] = volume.iloc[-1]
        result['volume_rel'] = volume.iloc[-1] / volume.rolling(30).mean().iloc[-1]

        # Rango / breakout
        result['range_high'] = close.rolling(30).max().iloc[-1]
        result['range_low'] = close.rolling(30).min().iloc[-1]

        return result
