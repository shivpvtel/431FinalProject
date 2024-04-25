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
CREATE TABLE if not exists Player_info (
    ID INTEGER,
    Name VARCHAR(255),
    FullName VARCHAR(255),
    Age INTEGER,
    PhotoUrl TEXT,
    Nationality VARCHAR(100),
    PRIMARY KEY (ID)
);
"""
cur.execute(create_table_query)
conn.commit()  
csv_file_path = 'Player_info.csv'

with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  
    query = """
    INSERT INTO player_info (ID, Name, FullName, Age, PhotoUrl, Nationality) 
    VALUES (%s, %s, %s, %s, %s, %s)
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
