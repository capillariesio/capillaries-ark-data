#{"ts":"2001-01-05 00:01:35.123", "ticker":"TSLA", "qty":5, "price":0.9},

import sys,json, os
import datetime

earliest_holding_date = "2020-12-31"

if len(sys.argv) != 3:
   print("Specify trades.json and eod_prices.json, space-separated")
   sys.exit(1)

with open(sys.argv[2]) as f:
  eod_prices = json.load(f)

funds = set(["ARKF", "ARKG", "ARKK", "ARKQ", "ARKW", "ARKX"])
txns = []
trade_ts = 0

print("ts,account_id,ticker,qty,price")

with open(sys.argv[1]) as f:
    data = json.load(f)
    for ticker_trades in data:
      if "symbol" not in ticker_trades:
        continue
      ticker = ticker_trades["symbol"]
      if "trades" not in ticker_trades:
        continue
      for trade in ticker_trades["trades"]:
        if trade["fund"] not in funds:
           continue
        d = trade["date"]
        hours, remainder = divmod(trade_ts, 3600)
        minutes, seconds = divmod(remainder, 60)
        ts = trade["date"] + " " + '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))
        trade_ts += 1
        if trade_ts == 86400:
          trade_ts = 0

        if d in eod_prices and ticker in eod_prices[d]:
           price = eod_prices[d][ticker]
        else:
          if d < earliest_holding_date:
            # We will not need this trade/txn price anyways
            continue
          raise RuntimeError(f"no price for {ticker} on {d} or adjacent days, trade: {trade}")

          # This piece helps for txns, but we better have eod_prices more complete, so let's fix it by adding price overrides
          # and using price interpolation

          # # Find previous/next price
          # price = None
          # for delta in range(1,3): # Tweak it if a price is missing for too long, or better - add a price override
          #   prev_day = (datetime.date.fromisoformat(d) + datetime.timedelta(days=-delta)).isoformat()
          #   if prev_day in eod_prices and ticker in eod_prices[prev_day]:
          #     price = eod_prices[prev_day][ticker]
          #     break
          #   else:
          #     next_day = (datetime.date.fromisoformat(d) + datetime.timedelta(days=delta)).isoformat()
          #     if next_day in eod_prices and ticker in eod_prices[next_day]:
          #       price = eod_prices[next_day][ticker]
          #       break
          #if price == None:
          #  #raise RuntimeError(f"no price for {ticker} on {d} or adjacent days, trade: {trade}")
          #  print(f"no price for {ticker} on {d} or adjacent days, trade: {trade}")
        
        print(f'{ts},{trade["fund"]},{ticker},{trade["shares"] * (1 if trade["direction"] == "Buy" else -1)},{price}')