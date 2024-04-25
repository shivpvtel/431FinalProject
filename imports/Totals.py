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
CREATE TABLE if not exists Totals (	
    ID INTEGER,			
    PaceTotal INTEGER,	
    ShootingTotal INTEGER,	
    PassingTotal INTEGER,	
    DribblingTotal INTEGER, 
    DefendingTotal INTEGER, 
    PhysicalityTotal INTEGER,
    FOREIGN KEY (ID) REFERENCES Player_info(ID)
);
"""
cur.execute(create_table_query)  
conn.commit()
csv_file_path = 'Totals.csv'

with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 
    query = """
    INSERT INTO Totals (ID, PaceTotal, ShootingTotal, PassingTotal, DribblingTotal, DefendingTotal, PhysicalityTotal) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)
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
