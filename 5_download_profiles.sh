echo "[" > profiles.json
while read ticker; do
  curl -o tmp.json "https://arkfunds.io/api/v2/stock/profile?symbol=$ticker"
  cat tmp.json >> profiles.json
  echo "," >> profiles.json
done < tickers.txt
echo "{}]" >> profiles.json
rm tmp.json
