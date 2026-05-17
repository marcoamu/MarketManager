CREATE TABLE IF NOT EXISTS MARKET_DATA (
    symbol TEXT,
    timestamp TEXT,

    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume REAL,
    trade_count INTEGER,
    vwap REAL,

    return_pct REAL,
    range_pct REAL,
    velocity REAL,
    acceleration REAL,

    ema9 REAL,
    ema21 REAL,
    ema50 REAL,
    rsi14 REAL,
    atr14 REAL,

    volume_avg_20 REAL,
    volume_ratio REAL,

    PRIMARY KEY (symbol, timestamp)
);
