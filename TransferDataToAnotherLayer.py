from psycopg2 import sql
import psycopg2
import os
import json


DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "123"

# 1. Подключение
conn = psycopg2.connect(
   client_encoding="utf-8",  # Важно!
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)
cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO "DWH".CARS (carid, carbrand, carmodel, cargeneration, operdate)
    SELECT DISTINCT *
    FROM "STAGING".NEWCARS stgc
    WHERE stgc.carid NOT IN (SELECT carid FROM "DWH".CARS);
    """
    )
conn.commit()  # Фиксируем изменения
                    
cursor.close()
conn.close()
print("Данные успешно перенесены!")


