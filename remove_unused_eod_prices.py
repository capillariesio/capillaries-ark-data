import sys,json,datetime,csv
from dateutil.relativedelta import relativedelta

if len(sys.argv) != 3:
   print("Specify eod_prices.json and txns.csv file names")
   sys.exit(1)

with open(sys.argv[1]) as f:
  eod_prices = json.load(f)

used_dates = set()

cur_period_start = datetime.date.fromisoformat("1970-01-01")
while cur_period_start < datetime.date.fromisoformat("2030-01-01"):
  used_dates.add((cur_period_start + datetime.timedelta(days=-1)).isoformat())
  cur_period_start = cur_period_start + relativedelta(months=1)

# Read txns csv one by one and add date if needed
with open(sys.argv[2], "r") as f:
  reader = csv.reader(f, delimiter=",")
  for i, line in enumerate(reader):
    ts = line[0] # We know ts is the first column
    d = ts.split(" ")[0]
    used_dates.add(d)

# Leave only used_dates in eod_prices
for d in set(eod_prices) - used_dates:
    del eod_prices[d]

print(json.dumps(eod_prices,sort_keys=True,indent=2))