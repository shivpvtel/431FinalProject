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
CREATE TABLE if not exists Physical_Attributes(	
    ID INTEGER,								
    Acceleration INTEGER, 
    SprintSpeed INTEGER, 
    Agility INTEGER, 
    Reactions INTEGER, 
    Balance INTEGER, 
    ShotPower INTEGER,
    Jumping INTEGER,
    Stamina INTEGER, 
    Strength INTEGER, 
    Aggression INTEGER, 
    Vision INTEGER, 
    Composure INTEGER,
    FOREIGN KEY (ID) REFERENCES Player_info(ID)
);
"""
cur.execute(create_table_query)  
conn.commit() 


csv_file_path = 'Physical_attributes.csv'


with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 


    query = """
    INSERT INTO Physical_Attributes (ID, Acceleration, SprintSpeed, Agility, Reactions, Balance, ShotPower, Jumping, Stamina, Strength, Aggression, Vision, Composure) 
    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s, %s)
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
