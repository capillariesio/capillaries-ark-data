import sys,json, os

if len(sys.argv) != 2:
   print("Specify holdings file name")
   sys.exit(1)

tickers = set()

with open(sys.argv[1]) as f:
    data = json.load(f)
    for fund_holdings in data:
      if "symbol" not in fund_holdings:
        continue
      for h in fund_holdings["holdings"]:
        ticker = h["ticker"]
        if ticker is not None:
          tickers.add(ticker)

for ticker in sorted(list(tickers)):
  print(ticker)