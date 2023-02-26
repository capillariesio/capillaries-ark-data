python3 trades_to_txns.py trades.json eod_prices.json > txns.csv
python3 remove_unused_eod_prices.py eod_prices.json txns.csv > eod_prices.json