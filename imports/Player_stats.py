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
CREATE TABLE if not exists Player_stats (
    ID INTEGER,
    TotalStats INTEGER,
    BaseStats INTEGER,
    Overall INTEGER,
    Potential INTEGER,
    Growth INTEGER,
    FOREIGN KEY (ID) REFERENCES Player_info(ID)
);
"""
cur.execute(create_table_query)
conn.commit()

csv_file_path = 'Player_stats.csv'
with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 
    query = """
    INSERT INTO Player_stats (ID, TotalStats, BaseStats, Overall, Potential, Growth) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for row in reader:
        if len(row) == 6:  
            try:
                cur.execute(query, row)
                conn.commit()  
            except psycopg2.Error as e:
                print(f"Error inserting data: {e}")
                conn.rollback() 
        else:
            print(f"Skipped row due to incorrect number of columns: {row}")

cur.close()
conn.close()
