import csv
import psycopg2

# Establish database connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
create_table_query = """
CREATE TABLE if not exists Positions (
    ID INTEGER,
    Positions Varchar(100),
    BestPosition Varchar(20),
    ClubPosition Varchar(20),
    NationalPosition Varchar(20),
    FOREIGN KEY (ID) REFERENCES Player_info(ID)
);
"""
cur.execute(create_table_query)
conn.commit()
csv_file_path = 'Positions.csv'

with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 
    query = """
    INSERT INTO Positions (ID, Positions, BestPosition, ClubPosition, NationalPosition) 
    VALUES (%s, %s, %s, %s, %s)
    """
    for row in reader:
        if len(row) == 5:
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
