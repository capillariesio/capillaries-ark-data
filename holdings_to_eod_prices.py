import sys
import json
import os
import datetime

if len(sys.argv) != 2:
    print("Specify holdings file name")
    sys.exit(1)

price_overrides = {
  "2021-01-07": {"ONVO": 12.78},
  "2021-01-08": {"ONVO": 12.78},
  "2021-01-11": {"ONVO": 13.97},
  "2021-01-20": {"ONVO": 14.27},
  "2021-01-26": {"ONVO": 12.79},
  "2021-02-04": {"ONVO": 19.39},
  "2021-02-10": {"ONVO": 14.22},
  "2021-02-17": {"ONVO": 13.00},
  "2021-03-01": {"CRM": 162.20,"IBKR": 75.20,"HIMS": 13.36},
  "2021-03-16": {"FLIR": 55.16,"HIMS": 14.45,"ROK": 265.24},
  "2021-03-24": {"SPFR": 10.15},
  "2021-04-12": {"GRMN": 140.60},
  "2021-04-14": {"COIN": 328.28},
  "2021-04-15": {"TSP": 40.0},
  "2021-04-21": {"PATH": 69.0},
  "2021-04-27": {"TEAM": 237.56},
  "2021-04-28": {"GLEO": 10.02},
  "2021-05-03": {"STNE": 63.98},
  "2021-05-14": {"DIS": 173.7},
  "2021-05-24": {"DRNA": 30.11},
  "2021-05-27": {"ONVO": 8.51},
  "2021-06-02": {"ETSY": 175.14},
  "2021-06-03": {"ONVO": 8.59},
  "2021-06-17": {"QSI": 8.1},
  "2021-07-06": {"FTCH": 48.56},
  "2021-07-12": {"CND": 10.45,"KVSB": 10.51},
  "2021-07-15": {"MKFG": 7.76},
  "2021-07-29": {"HOOD": 34.82},
  "2021-08-03": {"SRNG": 9.9},
  "2021-08-04": {"LPSN": 62.31},
  "2021-08-05": {"GENI": 16.81},
  "2021-08-11": {"GRMN": 167.52},
  "2021-08-18": {"PFE": 49.31},
  "2021-08-23": {"GRMN": 175.86},
  "2021-10-25": {"PAGS": 38.72},
  "2021-10-28": {"GRMN": 143.60},
  "2021-10-29": {"SLGCW": 2.25},
  "2021-11-01": {"ALLO": 20.140},
  "2021-11-10": {"ALLO": 19.50},
  "2021-11-15": {"GRMN": 142.80},
  "2021-11-16": {"BNR": 15.22},
  "2021-11-22": {"MNDY": 328.41},
  "2021-12-02": {"XPEV": 48.29},
  "2021-12-14": {"GRMN": 132.23},
  "2021-12-20": {"NRIX": 28.0},
  "2022-01-31": {"GLBE": 38.53},
  "2022-02-01": {"TCEHY": 59.1},
  "2022-03-25": {"NIO": 19.91},
  "2022-03-28": {"MTTR": 7.96},
  "2022-05-09": {"GM": 38.26},
  "2022-06-08": {"MRNA": 148.53,"ONVO": 8.57},
  "2022-08-08": {"DKNG": 20.67},
  "2022-08-22": {"CMPS": 16.98},
  "2022-09-02": {"DKNG": 17.63},
  "2022-09-07": {"DKNG": 18.02},
  "2022-09-12": {"DKNG": 18.60,"GRMN": 85.73},
  "2022-09-13": {"DKNG": 18.60},
  "2022-09-26": {"RKLB": 4.23},
  "2022-09-29": {"GRMN": 80.31},
  "2022-10-03": {"GRMN": 79.70},
  "2022-10-27": {"ONVO": 1.77},
  "2022-10-28": {"DKNG": 11.31},
  "2022-11-04": {"DKNG": 14.88},
  "2022-11-11": {"ONVO": 1.55},
  "2022-11-15": {"ONVO": 1.53},
  "2022-11-21": {"ONVO": 1.51},
  "2022-11-25": {"ONVO": 1.52},
  "2022-12-02": {"ONVO": 1.7},
  "2022-12-06": {"ONVO": 1.72},
  "2022-12-09": {"ONVO": 1.67},
  "2022-12-14": {"ONVO": 1.62},
  "2022-12-19": {"ONVO": 1.59},
  "2022-12-21": {"ONVO": 1.60},
  "2022-12-29": {"DKNG": 11.39},
  "2023-01-03": {"ONVO": 1.45},
  "2023-01-13": {"ONVO": 1.63},
  "2023-01-20": {"ONVO": 2.59},
  "2023-01-25": {"ONVO": 2.71},
  "2023-01-31": {"ONVO": 1.68}
}

eod_prices = {}

ticker_d_prices_map = {}
with open(sys.argv[1]) as f:
    data = json.load(f)
    for fund_holdings in data:
        if "symbol" not in fund_holdings:
            continue
        for h in fund_holdings["holdings"]:
            d = h["date"]
            ticker = h["ticker"]
            if ticker is None:
                continue
            if ticker not in ticker_d_prices_map:
                ticker_d_prices_map[ticker] = []
            ticker_d_prices_map[ticker].append(
                {"d": d, "price": h["share_price"]})

# Add overrides to ticker_d_prices_map
for d, ticker_price_override_map in price_overrides.items():
    for ticker, price in ticker_price_override_map.items():
        if ticker not in ticker_d_prices_map:
            ticker_d_prices_map[ticker] = []
        ticker_d_prices_map[ticker].append({"d": d, "price": price})

# Insert results, interpolate missing days if needed
for ticker, day_prices in ticker_d_prices_map.items():
    day_prices.sort(key=lambda x: x["d"])

    for i in range(len(day_prices)):
        d = day_prices[i]["d"]
        # Add to final
        if d not in eod_prices:
            eod_prices[d] = {}
        eod_prices[d][ticker] = day_prices[i]["price"]

        if i == 0:
            continue
        delta_days = (datetime.date.fromisoformat(
            d) - datetime.date.fromisoformat(day_prices[i-1]["d"])).days
        if delta_days >= 2:
            # print(f'Inserting synth between {day_prices[i-1]["d"]} / {day_prices[i-1]["price"]} and {d} / {day_prices[i]["price"]}')
            daily_price_inc = (
                day_prices[i]["price"] - day_prices[i-1]["price"]) / delta_days
            for j in range(1, delta_days):
                synth_day = (datetime.date.fromisoformat(
                    day_prices[i-1]["d"]) + datetime.timedelta(days=j)).isoformat()
                # This is how we findsynth prices later: 3 digits
                synth_price = round(
                    day_prices[i-1]["price"] + daily_price_inc * j, 3)
                # print(f'{synth_day} / {synth_price}')
                # Add synth to final
                if synth_day not in eod_prices:
                    eod_prices[synth_day] = {}
                eod_prices[synth_day][ticker] = synth_price


print(json.dumps(eod_prices, sort_keys=True, indent=2))
