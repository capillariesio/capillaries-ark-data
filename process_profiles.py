import sys,json, os

if len(sys.argv) != 2:
   print("Specify downloaded profiles file name")
   sys.exit(1)

ticker_sector_map = {}
ticker_override = {
  "ACIC": {
    "country": "United States",
    "name": "ATLAS CREST INVESTMENT COR-A",
    "sectors": ["Financial Services"]
  },
  "GBTC": {
    "country": "United States",
    "name": "Grayscale Bitcoin Trust (BTC)",
    "sectors": ["Financial Services"]
  },
  "1833": {
    "country": "China",
    "name": "PING AN HEALTHCARE AND TECHN",
    "sectors": ["Healthcare"]
  },
  "3690": {
    "country": "China",
    "name": "MEITUAN-CLASS B",
    "sectors": ["Consumer Cyclical"]
  },
  "4477": {
    "country": "Japan",
    "name": "BASE INC",
    "sectors": ["Communication Services"]
  },
  "6060": {
    "country": "China",
    "name": "ZHONGAN ONLINE P&C INSURAN-H",
    "sectors": ["Financial Services"]
  },
  "6301 JT": {
    "country": "Japan",
    "name": "KOMATSU LTD",
    "sectors": ["Industrials"]
  },
  "6618": {
    "country": "China",
    "name": "JD HEALTH INTERNATIONAL INC",
    "sectors": ["Consumer Cyclical"]
  },
  "8473": {
    "country": "Japan",
    "name": "SBI HOLDINGS INC",
    "sectors": ["Financial Services"]
  },
  "9923": {
    "country": "China",
    "name": "YEAHKA LTD",
    "sectors": ["Technology"]
  },
  "AIR FP": {
    "country": "Netherlands",
    "name": "AIRBUS SE",
    "sectors": ["Industrials"]
  },
  "AONE": {
    "country": "United States",
    "name": "ONE - CLASS A",
    "sectors": ["Financial Services"]
  },
  "ARCT UQ": {
    "country": "United States",
    "name": "ARCTURUS THERAPEUTICS HOLDIN",
    "sectors": ["Healthcare"]
  },
  "ATAI UQ": {
    "country": "Germany",
    "name": "ATAI LIFE SCIENCES NV",
    "sectors": ["Healthcare"]
  },
  "CMLF": {
    "country": "United States",
    "name": "CM LIFE SCIENCES INC-CLASS A",
    "sectors": ["Financial Services"]
  },
  "DKNG UW": {
    "country": "United States",
    "name": "DRAFTKINGS INC",
    "sectors": ["Consumer Cyclical"]
  },
  "DRNA": {
    "country": "United States",
    "name": "DICERNA PHARMACEUTICALS INC",
    "sectors": ["Healthcare"]
  },
  "DSY": {
    "country": "France",
    "name": "DASSAULT SYSTEMES SE",
    "sectors": ["Technology"]
  },
  "DSY FP": {
    "country": "France",
    "name": "DASSAULT SYSTEMES SE",
    "sectors": ["Technology"]
  },
  "EDR  UN": {
    "country": "United States",
    "name": "ENDEAVOR GROUP HOLD-CLASS A",
    "sectors": ["Communication Services"]
  },
  "EXPC": {
    "country": "United States",
    "name": "EXPERIENCE INVESTMENT-A",
    "sectors": ["Financial Services"]
  },
  "FB": {
    "country": "United States",
    "name": "FACEBOOK INC-CLASS A",
    "sectors": ["Technology"]
  },
  "FLIR": {
    "country": "United States",
    "name": "FLIR SYSTEMS INC",
    "sectors": ["Industrials"]
  },
  "GLEO": {
    "country": "Cayman Islands",
    "name": "GALILEO ACQUISITION CORP",
    "sectors": ["Financial Services"]
  },
  "GRMN U": {
    "country": "Switzerland",
    "name": "GARMIN LTD",
    "sectors": ["Technology"]
  },
  "GRMN UN": {
    "country": "Switzerland",
    "name": "GARMIN LTD",
    "sectors": ["Technology"]
  },
  "HO FP": {
    "country": "France",
    "name": "THALES SA",
    "sectors": ["Industrials"]
  },
  "IPOB": {
    "country": "United States",
    "name": "SOCIAL CAPITAL HEDOSOPHIA-A",
    "sectors": ["Financial Services"]
  },
  "KVSB": {
    "country": "United States",
    "name": "KHOSLA VENTURES ACQUISITIO-A",
    "sectors": ["Financial Services"]
  },
  "LGVW": {
    "country": "United States",
    "name": "LONGVIEW ACQUISITION-A",
    "sectors": ["Financial Services"]
  },
  "NU UN": {
    "country": "Brasil",
    "name": "NU HOLDINGS LTD/CAYMAN ISL-A",
    "sectors": ["Financial Services"]
  },
  "PRNT": {
    "country": "United States",
    "name": "The 3D Printing ETF",
    "sectors": ["Technology"]
  },
  "PRNT UF": {
    "country": "United States",
    "name": "THE 3D PRINTING ETF",
    "sectors": ["Technology"]
  },
  "PSTI": {
    "country": "Israel",
    "name": "PLURISTEM THERAPEUTICS INC",
    "sectors": ["Healthcare"]
  },
  "RAVN": {
    "country": "United States",
    "name": "RAVEN INDUSTRIES INC",
    "sectors": ["Technology"]
  },
  "RTP": {
    "country": "Cayman Islands",
    "name": "REINVENT TECHNOLOGY-CLASS A",
    "sectors": ["Financial Services"]
  },
  "SMFR": {
    "country": "United States",
    "name": "SEMA4 HOLDINGS CORP",
    "sectors": ["Healthcare"]
  },
  "SPFR": {
    "country": "United States",
    "name": "JAWS SPITFIRE ACQUISITION-A",
    "sectors": ["Financial Services"]
  },
  "SRNG": {
    "country": "United States",
    "name": "SOARING EAGLE ACQU - CL A",
    "sectors": ["Financial Services"]
  },
  "TAK UN": {
    "country": "Japan",
    "name": "TAKEDA PHARMACEUTIC-SP ADR",
    "sectors": ["Healthcare"]
  },
  "TCS LI": {
    "country": "Cyprus",
    "name": "TCS GROUP HOLDING-GDR REG S",
    "sectors": ["Financial Services"]
  },
  "TREE UW": {
    "country": "United States",
    "name": "LENDINGTREE INC",
    "sectors": ["Financial Services"]
  },
  "TWTR": {
    "country": "United States",
    "name": "Twitter, Inc. (delisted)",
    "sectors": ["Communication Services"]
  },
  "USD": {
    "country": "United States",
    "name": "ProShares Ultra Semiconductors",
    "sectors": ["Technology"]
  },
  "WORK": {
    "country": "United States",
    "name": "SLACK TECHNOLOGIES INC- CL A",
    "sectors": ["Technology"]
  },
  "XLNX": {
    "country": "United States",
    "name": "XILINX INC",
    "sectors": ["Technology"]
  },
  "XONE": {
    "country": "United States",
    "name": "Bondbloxx Bloomberg One Year Target Duration US Treasury ETF",
    "sectors": ["Financial Services"]
  },
  "2618":{
    "name": "JD LOGISTICS",
    "country": "China",
    "sectors":["Consumer Cyclical"],
  },
  "4689":{
    "name": "Z HOLDINGS CORP",
    "country": "Japan",
    "sectors":["Consumer Cyclical"],
  },
  "6301":{
    "name": "KOMATSU LTD",
    "country": "Japan",
    "sectors":["Industrials"],
  },
  "ADYEN":{
    "name": "ADYEN NV",
    "country": "Netherlands",
    "sectors":["Technology"],
  },
  "CND":{
    "name": "CONCORD ACQUISITION CORP -A",
    "country": "United States",
    "sectors":["Financial Services"],
  },
  "DYNS":{
    "name": "DYNAMICS SPECIAL PURPOSE C-A",
    "country": "United States",
    "sectors":["Financial Services"],
  },
  "HO":{
    "name": "THALES SA",
    "country": "France",
    "sectors":["Industrials"],
  },
  "KSPI":{
    "name": "JSC KASPI.KZ GDR-REG S",
    "country": "Kazakhstan",
    "sectors":["Technology"],
  },
  "ZY":{
    "name": "ZYMERGEN INC",
    "country": "United States",
    "sectors":["Healthcare"],
  }}

with open(sys.argv[1]) as f:
    data = json.load(f)
    for ticker_profile in data:
      if "symbol" not in ticker_profile:
        continue
      ticker = ticker_profile["symbol"]
      if ticker in ticker_override:
        ticker_sector_map[ticker] = ticker_override[ticker]
        continue
      
      if "profile" not in ticker_profile:
        ticker_sector_map[ticker] = {}
        continue
      o = {"name":None, "country":None, "sectors":[]}
      p = ticker_profile["profile"]
      if "name" in p:
        o["name"] = p["name"].replace("\u00f6","o")
      if "country" in p:
        o["country"] = p["country"]
      if "sector" in p:
        o["sectors"] = [p["sector"]]
      ticker_sector_map[ticker] = o

print(json.dumps(ticker_sector_map, sort_keys=True, indent=2))