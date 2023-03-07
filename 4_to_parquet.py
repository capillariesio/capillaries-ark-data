import pyarrow.csv as pv
import pyarrow.parquet as pq

table = pv.read_csv("txns.csv")
pq.write_table(table, "txns.parquet")

table = pv.read_csv("holdings.csv")
pq.write_table(table, "holdings.parquet")