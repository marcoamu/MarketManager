class SignalEngine:

    @staticmethod
    def evaluate(indicators: dict) -> dict:
        signals = {}

        signals['breakout_up'] = int(indicators['price'] > indicators['range_high'])
        signals['breakout_down'] = int(indicators['price'] < indicators['range_low'])

        signals['volume_spike'] = int(indicators['volume_rel'] > 2)

        # Score simple (ajustable)
        score = 0
        score += indicators['momentum_5'] * 2
        score += indicators['momentum_15']
        score += indicators['volume_rel'] * 5
        score += indicators['acceleration'] * 10

        signals['signal_score'] = score

        signals['alert_triggered'] = int(
            score > 10 and signals['volume_spike']
        )

        signals['alert_type'] = (
            'breakout_up' if signals['breakout_up'] else None
        )

        return signals
