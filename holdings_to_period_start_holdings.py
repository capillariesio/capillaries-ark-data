import sys,json,os,datetime
from dateutil.relativedelta import relativedelta

if len(sys.argv) != 2:
   print("Specify holdings file name")
   sys.exit(1)

print("d,account_id,ticker,qty")

eom_dates = set()

cur_period_start = datetime.date.fromisoformat("1970-01-01")
while cur_period_start < datetime.date.fromisoformat("2030-01-01"):
   eom_dates.add((cur_period_start + datetime.timedelta(days=-1)).isoformat())
   cur_period_start = cur_period_start + relativedelta(months=1)

with open(sys.argv[1]) as f:
    data = json.load(f)
    for fund_holdings in data:
      if "symbol" not in fund_holdings:
        continue
      for h in fund_holdings["holdings"]:
        if h["date"] not in eom_dates:
            continue
        fund = h["fund"]
        d = h["date"]
        ticker = h["ticker"]
        if ticker is None:
            continue
        print(f"{h['date']},{h['fund']},{h['ticker']},{h['shares']}")
      # If no holdings for this fund found for this date, assume it was not existing,
      # no holding records is fine