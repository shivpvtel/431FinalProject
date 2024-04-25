import csv
import psycopg2

def safe_int(value, default=None):
    """Convert value to integer or return default if conversion fails."""
    try:
        return int(value)
    except ValueError:
        return default


conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


create_table_query = """
CREATE TABLE if not exists Club (
    ID INTEGER,
    Club VARCHAR(255),
    ClubNumber INTEGER,
    ClubJoined INTEGER,
    FOREIGN KEY (ID) REFERENCES Player_info(ID)
);
"""
cur.execute(create_table_query)  
conn.commit() 


csv_file_path = 'Club.csv'


with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  

    query = """
    INSERT INTO Club (ID, Club, ClubNumber, ClubJoined) 
    VALUES (%s, %s, %s, %s)
    """


    for row in reader:

        row[2] = safe_int(row[2], default=None) 
        row[3] = safe_int(row[3], default=None)  

        try:

            cur.execute(query, row)
            conn.commit()  
        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")
            conn.rollback()  

cur.close()
conn.close()
