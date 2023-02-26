echo "[" > holdings.json
for fund in ARKK ARKW ARKF ARKQ ARKG ARKX
do
   curl -o tmp.json "https://arkfunds.io/api/v2/etf/holdings?symbol=$fund&date_from=2020-01-01&date_to=2030-12-31"
   cat tmp.json >> holdings.json
   echo "," >> holdings.json
done
echo "{}]" >> holdings.json
rm tmp.json