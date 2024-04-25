

import csv
import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
create_table_query = """
CREATE TABLE if not exists Work_rates (
    ID INTEGER,
    AttackingWorkRate Text,
    DefensiveWorkRate Text,
    FOREIGN KEY (ID) REFERENCES Player_info(ID)
);
"""
cur.execute(create_table_query) 
conn.commit() 
csv_file_path = 'Work_rates.csv'

with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 

    query = """
    INSERT INTO Work_rates (ID, AttackingWorkRate, DefensiveWorkRate) 
    VALUES (%s, %s, %s)
    """

    for row in reader:
        try:
            cur.execute(query, row)
            conn.commit()  
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")
            conn.rollback()  
cur.close()
conn.close()
