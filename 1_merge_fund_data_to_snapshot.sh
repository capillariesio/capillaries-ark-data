echo "{" > snapshot.json
for fund in ARKK ARKW ARKF ARKQ ARKG ARKX
do
   echo '"'$fund'": '  >> snapshot.json
   cat $fund.json >> snapshot.json
   echo "," >> snapshot.json
done
echo '"none":{}}' >> snapshot.json
