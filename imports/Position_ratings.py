

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
CREATE TABLE if not exists Position_ratings(	
    ID INTEGER,													
    STRating INTEGER,
    LWRating INTEGER,
    LFRating INTEGER,
    CFRating INTEGER,
    RFRating INTEGER,
    RWRating INTEGER,
    CAMRating INTEGER,
    LMRating INTEGER,
    CMRating INTEGER,
    RMRating INTEGER,
    LWBRating INTEGER,
    CDMRating INTEGER,
    RWBRating INTEGER,
    LBRating INTEGER,
    CBRating INTEGER,
    RBRating INTEGER,
    GKRating INTEGER,
    FOREIGN KEY (ID) REFERENCES Player_info(ID)
);
"""
cur.execute(create_table_query)  
conn.commit() 

# Path to your CSV file
csv_file_path = 'Position_rating.csv'


with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 
    query = """
    INSERT INTO Position_ratings (ID, STRating, LWRating, LFRating, CFRating, RFRating, RWRating, CAMRating, LMRating, CMRating, RMRating, LWBRating, CDMRating, RWBRating, LBRating, CBRating, RBRating, GKRating) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
