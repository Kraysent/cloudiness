import psycopg2
import pandas.io.sql as sqlio
import pandas as pd
conn = psycopg2.connect("dbname='tools' user='saiuser' host='192.168.10.87' ")
# cursor = conn.cursor()
mysql="""SELECT * FROM "meteoData" ORDER BY "ID" DESC LIMIT 10000 ; """ 
meases = sqlio.read_sql_query(mysql, conn)
print(meases)

