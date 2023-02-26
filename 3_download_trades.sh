echo "[" > trades.json
while read ticker; do
  curl -o tmp.json "https://arkfunds.io/api/v2/stock/trades?symbol=$ticker&date_from=2020-01-01&date_to=2030-12-31"
  cat tmp.json >> trades.json
  echo "," >> trades.json
done < tickers.txt
echo "{}]" >> trades.json
rm tmp.json
