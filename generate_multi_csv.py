"""
Generate sample CSV files for multi-symbol multi-timeframe testing
Format: No header, tab-separated
Columns: Date Time Open High Low Close Volume
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path


def generate_ohlcv_data(
    symbol: str,
    timeframe_minutes: int,
    num_candles: int,
    initial_price: float,
    volatility: float = 0.0003
):
    """
    Generate OHLCV data without header.

    Args:
        symbol: Currency pair (e.g., AUDUSD, EURUSD)
        timeframe_minutes: Timeframe in minutes
        num_candles: Number of candles to generate
        initial_price: Starting price
        volatility: Price volatility
    """
    np.random.seed(hash(symbol) % 10000)  # Consistent but different per symbol

    data = []
    current_time = datetime(2025, 11, 19, 0, 0)  # Start date
    current_price = initial_price

    for i in range(num_candles):
        # Skip weekends
        while current_time.weekday() >= 5:  # Saturday = 5, Sunday = 6
            current_time += timedelta(minutes=timeframe_minutes)

        # Generate price movement
        price_change = np.random.normal(0, volatility)
        current_price = current_price * (1 + price_change)

        # Generate OHLC
        high_offset = abs(np.random.normal(0, volatility * 0.5))
        low_offset = abs(np.random.normal(0, volatility * 0.5))

        open_price = current_price
        close_price = current_price * (1 + np.random.normal(0, volatility * 0.3))
        high_price = max(open_price, close_price) + high_offset
        low_price = min(open_price, close_price) - low_offset

        # Generate volume
        volume = np.random.randint(50, 500)

        # Format: Date Time Open High Low Close Volume (tab-separated, no header)
        date_str = current_time.strftime('%Y.%m.%d')
        time_str = current_time.strftime('%H:%M')

        data.append([
            date_str,
            time_str,
            round(open_price, 5),
            round(high_price, 5),
            round(low_price, 5),
            round(close_price, 5),
            volume
        ])

        # Move to next candle
        current_time += timedelta(minutes=timeframe_minutes)
        current_price = close_price

    return data


def save_csv_no_header(data, filepath):
    """Save data to CSV without header, tab-separated."""
    df = pd.DataFrame(data)
    df.to_csv(filepath, sep='\t', header=False, index=False)


def main():
    """Generate sample CSV files for testing."""

    # Create CSV folder
    csv_folder = Path('CSV')
    csv_folder.mkdir(exist_ok=True)

    # Configuration
    symbols_config = {
        'AUDUSD': 0.66400,
        'EURUSD': 1.05500,
        'GBPUSD': 1.26500,
        'USDJPY': 150.500,
    }

    timeframes = {
        '5': (5, 2000),    # M5: 2000 candles
        '15': (15, 2000),  # M15: 2000 candles
        '30': (30, 1500),  # M30: 1500 candles
        '60': (60, 1000),  # H1: 1000 candles
    }

    print("Generating sample CSV files...")
    print("="*60)

    for symbol, initial_price in symbols_config.items():
        for tf_name, (tf_minutes, num_candles) in timeframes.items():
            filename = f"{symbol}{tf_name}.csv"
            filepath = csv_folder / filename

            # Generate data
            data = generate_ohlcv_data(
                symbol=symbol,
                timeframe_minutes=tf_minutes,
                num_candles=num_candles,
                initial_price=initial_price
            )

            # Save to CSV (no header, tab-separated)
            save_csv_no_header(data, filepath)

            print(f"✓ {filename:20s} - {num_candles} candles")

    print("="*60)
    print(f"✓ Generated {len(symbols_config) * len(timeframes)} files in 'CSV/' folder")
    print("\nFiles created:")
    for file in sorted(csv_folder.glob('*.csv')):
        size_kb = file.stat().st_size / 1024
        print(f"  - {file.name:20s} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
