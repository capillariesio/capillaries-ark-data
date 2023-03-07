import json,datetime


g_last_eoq_date = datetime.date(2022,12,31)


def get_prev_eom(d):
    return (datetime.date.fromisoformat(d).replace(day=1) + datetime.timedelta(days=-1)).isoformat()

ticker_date_price_map = {} # [ticker][d]->price
account_ticker_date_txn_map = {} # [account_id][d][ticker]->{qty,price}
account_first_txn_date_map = {} # [account_id]->d

with open("snapshot.json") as f:
    data = json.load(f)
    with open('holdings.csv', 'w') as f_holdings, open('txns.csv', 'w') as f_txns:
        
        f_holdings.write('account_id,d,ticker,qty\n')
        f_txns.write('ts,account_id,ticker,qty,price\n')

        for account_id, account_data in data.items():
            account_ticker_date_txn_map[account_id] = {}

            # Convert date format
            account_holding_history = sorted([{
                "d":'{2:04}-{0:02}-{1:02}'.format(*[int(n) for n in o["date"].split("/")]),
                "ticker":o["ticker"],
                "qty":int(float(o["shares"])),
                "price":round(float(o["value"])/float(o["shares"]),2)
                } for o in account_data if o["ticker"] != ""], key = lambda x: x["d"])
            
            prev_holding_qtys = {}
            prev_holding_dates = {}
            prev_holding_prices = {}
            prev_eom_holding_dates = {}

            for o in account_holding_history:
                ticker = o["ticker"]
                d = o["d"]
                price = o["price"]
                holding_qty = o["qty"]

                # Duplicate (by mistake maybe) holding data, ignore it, we do not want duplicates in our output
                if ticker in prev_holding_dates and prev_holding_dates[ticker] == d:
                    continue

                # Write price
                if ticker not in ticker_date_price_map:
                    ticker_date_price_map[ticker] = {}
                ticker_date_price_map[ticker][d] = price

                if d > g_last_eoq_date.isoformat():
                     break

                # Save txn
                if ticker not in account_ticker_date_txn_map[account_id]:
                    account_ticker_date_txn_map[account_id][ticker] = {}

                if ticker not in prev_holding_qtys:
                    # Synth txn for the very first holding, do not save zero txn
                    if holding_qty != 0:
                        account_ticker_date_txn_map[account_id][ticker][d] = {"qty":holding_qty,"price":price}
                        if account_id not in account_first_txn_date_map:
                            account_first_txn_date_map[account_id] = d
                else:
                    # Regular txn, do not save zero txn
                    txn_qty = holding_qty - prev_holding_qtys[ticker]
                    if txn_qty != 0:
                        account_ticker_date_txn_map[account_id][ticker][d] = {"qty": txn_qty, "price":price}
                        if account_id not in account_first_txn_date_map:
                            account_first_txn_date_map[account_id] = d

                prev_holding_qtys[ticker] = holding_qty
                prev_holding_dates[ticker] = d

        # We have all available txns and all available prices, build holdings
        for account_id, account_data in data.items():
            for ticker, date_txn_map in account_ticker_date_txn_map[account_id].items():
                cur_date = datetime.date.fromisoformat(account_first_txn_date_map[account_id]).replace(day=1) + datetime.timedelta(days=-1)
                cur_qty = 0
                cur_price = None
                while cur_date <= g_last_eoq_date:
                    d = cur_date.isoformat()
                    if cur_date < g_last_eoq_date or cur_qty == 0:
                        if d in date_txn_map:
                            cur_qty += date_txn_map[d]["qty"]
                            cur_price = date_txn_map[d]["price"]
                        # If it's an eom and eoq - write to holdings
                        if (cur_date + datetime.timedelta(days=1)).month != cur_date.month and cur_date.month % 3 == 0:
                            # Holdings record with cur_qty
                            f_holdings.write(f'{account_id},{d},{ticker},{cur_qty}\n')
                    else:
                        # Adjust g_last_eoq_date holding by adding a synth txn
                        if d in date_txn_map:
                            # There was a txn on that last eom date, adjust its qty
                            date_txn_map[d]["qty"] -= cur_qty
                        else:
                            # There was no txn on the last eom date, add a synth txn with the last known price
                            # (the price will be inaccurate, but this is the best we can do)
                            date_txn_map[d] = {"qty":-cur_qty, "price":cur_price}

                        # Add a synth price record. Again: it may be months after the last known price,
                        #  but there is nothing we can do: source holdings data does not add up
                        ticker_date_price_map[ticker][d] = cur_price

                        # Holdings record with zero qty
                        f_holdings.write(f'{account_id},{d},{ticker},0\n')

                    cur_date += datetime.timedelta(days=1)

                for d, txn in date_txn_map.items():
                    f_txns.write(f'{d},{account_id},{ticker},{txn["qty"]},{txn["price"]}\n')

# At this point, we have collected prices for all txn days for a specific account/ticker.
# But we also will need prices for all tickers used for this account to calculate twr.
# Also, we need prices for all eoms for all accounts.
# If we calculate and save all those prices, the result map will be too large.
# So, save just the key points (max and min), and interpolate at runtime.

ticker_price_history = {}

# Convert maps to lists so the end user can interpolate
for ticker, date_price_map in ticker_date_price_map.items():
    full_price_history = sorted([{"d":d,"p":price} for d,price in date_price_map.items()],key=lambda x:x["d"])
    # Walk through the list and remove everything but min/max
    prev_item = None
    prev_direction = None
    filtered_price_history = []
    for item in full_price_history:
        if prev_item is None:
            prev_item = item
            filtered_price_history.append(prev_item)
            continue

        new_direction = +1 if item["p"] >= prev_item["p"] else -1
        if prev_direction is None:
            prev_direction = new_direction
            prev_item = item
            continue

        if new_direction != prev_direction:
            filtered_price_history.append(prev_item)

        prev_direction = new_direction
        prev_item = item

    filtered_price_history.append(prev_item)
    ticker_price_history[ticker] = filtered_price_history

with open("company_info.json", "r") as f_company_info:
    company_info = json.load(f_company_info)
    missing_tickers = sorted(list(set(ticker_price_history.keys()) - set(company_info.keys())))
    if len(missing_tickers) > 0:
        print("Missing company info for (requires manual editing of company_info.json):")
        for ticker in missing_tickers:
            print(ticker)

with open("eod_prices.json", "w") as f_prices:
    s = json.dumps(ticker_price_history, sort_keys=True).replace("],","],\n  ").replace('": ','":').replace("}, {","},{").replace('", ','",')
    f_prices.write(s)
