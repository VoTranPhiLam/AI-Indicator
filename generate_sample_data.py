"""
Generate sample AUDCAD M15 data for testing
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_ohlcv_data(
    start_date: str,
    num_candles: int,
    initial_price: float = 0.89500,
    volatility: float = 0.0003
):
    """
    Generate realistic OHLCV data for AUDCAD M15 timeframe.

    Args:
        start_date: Starting date (YYYY-MM-DD)
        num_candles: Number of 15-minute candles to generate
        initial_price: Starting price
        volatility: Price volatility (standard deviation)
    """
    np.random.seed(42)  # For reproducibility

    data = []
    current_time = datetime.strptime(start_date, '%Y-%m-%d')
    current_price = initial_price

    for i in range(num_candles):
        # Skip weekends
        while current_time.weekday() >= 5:  # Saturday = 5, Sunday = 6
            current_time += timedelta(minutes=15)

        # Generate price movement (random walk with drift)
        price_change = np.random.normal(0, volatility)
        current_price = current_price * (1 + price_change)

        # Generate OHLC
        # High and Low around the current price
        high_offset = abs(np.random.normal(0, volatility * 0.5))
        low_offset = abs(np.random.normal(0, volatility * 0.5))

        open_price = current_price
        close_price = current_price * (1 + np.random.normal(0, volatility * 0.3))
        high_price = max(open_price, close_price) + high_offset
        low_price = min(open_price, close_price) - low_offset

        # Generate volume (random)
        volume = np.random.randint(50, 500)

        # Format data
        date_str = current_time.strftime('%Y.%m.%d')
        time_str = current_time.strftime('%H:%M')

        data.append({
            'Date': date_str,
            'Time': time_str,
            'Open': round(open_price, 5),
            'High': round(high_price, 5),
            'Low': round(low_price, 5),
            'Close': round(close_price, 5),
            'Volume': volume
        })

        # Move to next candle (15 minutes)
        current_time += timedelta(minutes=15)
        current_price = close_price

    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generating sample AUDCAD M15 data...")

    # Generate ~1 month of M15 data (approximately 2000 candles)
    df = generate_ohlcv_data(
        start_date='2024-01-01',
        num_candles=2500,  # Extra to account for weekend skips
        initial_price=0.89500,
        volatility=0.0003
    )

    # Save to CSV
    output_file = 'AUDCAD15.csv'
    df.to_csv(output_file, index=False)

    print(f"✓ Generated {len(df)} candles")
    print(f"✓ Date range: {df['Date'].iloc[0]} to {df['Date'].iloc[-1]}")
    print(f"✓ Price range: {df['Low'].min():.5f} to {df['High'].max():.5f}")
    print(f"✓ Saved to: {output_file}")
