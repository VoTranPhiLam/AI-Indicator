"""
Test JPY pip value detection
"""
from backtest_optimizer import get_pip_value

# Test various symbols
test_symbols = [
    "EURUSD",
    "GBPUSD",
    "AUDUSD",
    "USDCHF",
    "USDJPY",
    "EURJPY",
    "GBPJPY",
    "AUDJPY",
    "CHFJPY"
]

print("=" * 60)
print("TESTING PIP VALUE DETECTION")
print("=" * 60)

for symbol in test_symbols:
    pip_value = get_pip_value(symbol)
    digits = 3 if pip_value == 0.01 else 5
    print(f"{symbol:10s} → pip_value = {pip_value} ({digits} digits)")

print("\n✅ Test completed!")
print("\nExpected results:")
print("  - JPY pairs (USDJPY, EURJPY, etc.): 0.01 (3 digits)")
print("  - Other pairs: 0.0001 (5 digits)")
