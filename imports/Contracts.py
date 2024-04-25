import csv
import psycopg2

def safe_int(value, default=None):
    """Convert value to integer or return default if conversion fails."""
    try:
        return int(value)
    except ValueError:
        return default

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
CREATE TABLE if not exists Contracts (
    ID INTEGER,
    ValueEUR INTEGER,
    WageEUR INTEGER,
    ContractUntil INTEGER,
    ReleaseClause INTEGER,
    FOREIGN KEY (ID) REFERENCES Player_info(ID)
);
"""
cur.execute(create_table_query)
conn.commit()


csv_file_path = 'Contracts.csv' 


with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  
    query = """
    INSERT INTO Contracts (ID, ValueEUR, WageEUR, ContractUntil, ReleaseClause) 
    VALUES (%s, %s, %s, %s, %s)
    """

    for row in reader:

        row[1] = safe_int(row[1], default=None) 
        row[2] = safe_int(row[2], default=None)  
        row[3] = safe_int(row[3], default=None) 
        row[4] = safe_int(row[4], default=None)  

        try:
  
            cur.execute(query, row)
            conn.commit()  
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")
            conn.rollback()  

cur.close()
conn.close()
