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
CREATE TABLE if not exists InGame_Attributes(
    ID INTEGER,																						
    WeakFoot INTEGER,
    SkillMoves INTEGER,
    Crossing INTEGER,
    Finishing INTEGER,
    HeadingAccuracy INTEGER,
    ShortPassing INTEGER,
    Volleys	 INTEGER,
    Dribbling INTEGER,
    Curve INTEGER,
    FKAccuracy INTEGER,
    LongPassing INTEGER,
    BallControl INTEGER,
    LongShots INTEGER,
    Interceptions INTEGER,
    Positioning	 INTEGER,
    Penalties INTEGER,
    Marking INTEGER,
    StandingTackle INTEGER,
    SlidingTackle INTEGER,
    GKDiving INTEGER,
    GKHandling INTEGER,
    GKKicking INTEGER,
    GKPositioning INTEGER,
    GKReflexes INTEGER,
    FOREIGN KEY (ID) REFERENCES Player_info(ID)
);
"""
cur.execute(create_table_query)  
conn.commit() 


csv_file_path = 'In_game_attributes.csv'


with open(csv_file_path, newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(reader) 

    query = """
    INSERT INTO InGame_Attributes (ID, WeakFoot, SkillMoves, Crossing, Finishing, HeadingAccuracy, ShortPassing, Volleys, Dribbling, Curve, FKAccuracy,
    LongPassing, BallControl, LongShots, Interceptions, Positioning, Penalties, Marking, StandingTackle, SlidingTackle,
    GKDiving, GKHandling, GKKicking, GKPositioning, GKReflexes) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
