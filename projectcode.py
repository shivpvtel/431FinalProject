import psycopg2
import sys

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

tables = {
        '1': 'Player_info \n    Columns names: ID, Name, FullName, Age, PhotoUrl, Nationality',
        '2': 'Player_body_component \n  ID, PreferredFoot, Height, Weight',
        '3': 'Positions\n   Columns names: ID, Positions, BestPosition, ClubPosition, NationalPosition',
        '4': 'Player_stats\n    Columns names: ID, TotalStats, BaseStats, Overall, Potential, Growth',
        '5': 'Club\n    Columns names: ID, Club, ClubNumber, ClubJoined',
        '6': 'National\n    Columns names: ID, National, IntReputation, NationalNumber',
        '7': 'Contracts\n   Columns names: ID, ValueEUR, WageEUR, ContractUntil, ReleaseClause',
        '8': 'Work_rates\n  Columns names: ID, AttackingWorkRate, DefensiveWorkRate',
        '9': 'Totals\n  Columns names: ID, PaceTotal, ShootingTotal, PassingTotal, DribblingTotal, DefendingTotal, PhysicalityTotal',
        '10': 'Physical_attributes\n    Columns names: ID, Acceleration, SprintSpeed, Agility, Reactions, Balance, ShotPower, Jumping, Stamina, Strength, Aggression, Vision, Composure',
        '11': 'In_game_attributes\n Columns names: ID, WeakFoot, SkillMoves, Crossing, Finishing, HeadingAccuracy, ShortPassing, Volleys, Dribbling, Curve, FKAccuracy, LongPassing, BallControl, LongShots, Interceptions, Positioning, Penalties, Marking, StandingTackle, SlidingTackle, GKDiving, GKHandling, GKKicking, GKPositioning, GKReflexes',
        '12': 'Position_ratings\n   Columns names:  ID, STRating, LWRating, LFRating, CFRating, RFRating, RWRating, CAMRating, LMRating, CMRating, RMRating, LWBRating, CDMRating, RWBRating, LBRating, CBRating, RBRating, GKRating'
    }

def mainMenu():
    print('\nWelcome to the Database CLI Interface!\n')
    print('Please select an option:')
    print('1. Insert Data')
    print('2. Delete Data')
    print('3. Update Data')
    print('4. Search Data')
    print('5. Aggregate Functions')
    print('6. Sorting')
    print('7. Joins')
    print('8. Grouping')
    print('9. Subqueries')
    print('10. Transactions')
    print('11. Error Handling')
    print('12. Exit')
    choice = input('Enter your choice (1-12): ')
    return choice

def insert_data():
    print('\nInsert Data selected.')

    for key, desc in tables.items():
        print(f"{key}. {desc.split('\n')[0]}")  

    choice = input('Choose a table number to insert data into: ')
    if choice in tables:
        info = tables[choice]
        table_name = info.split('\n')[0]
        columns = info.split('\n')[1].strip().split(': ')[1].split(', ')
        print(f"Selected Table: {table_name}")
        print("Enter the following details:")

        column_data = []
        for column in columns:
            value = input(f"Enter {column}: ")
            column_data.append(value)

        columns_joined = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))

        query = f"INSERT INTO {table_name} ({columns_joined}) VALUES ({placeholders})"
        try:
            cur.execute(query, tuple(column_data))
            conn.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(f"Error inserting data: {e}")
            conn.rollback()
    else:
        print("Invalid table selection.")

        input('Press Enter to return to main menu...')

def delete_data():
    for key, desc in tables.items():
        table_name = desc.split('\n')[0] 
        print(f"{key}. {table_name}")

    choice = input('Choose a table number to delete from: ')
    if choice in tables:
        info = tables[choice]
        table_name = info.split('\n')[0]
        print(f"Selected Table: {table_name}")

        columns_part = info.split('\n')[1].strip()
        columns = columns_part.split(': ')[1].split(', ')
        print(f"Columns names: {', '.join(columns)}")

        column = input("Enter the column name to condition the deletion on (e.g., ID): ")
        if column not in columns:
            print("Invalid column name. Please try again.")
            return
        value = input(f"Enter the value of {column} for the record to delete: ")
        query = f"DELETE FROM {table_name} WHERE {column} = %s"

        try:
            cur.execute(query, (value,))
            conn.commit()
            print("Record deleted successfully.")
        except Exception as e:
            print(f"Error deleting data: {e}")
            conn.rollback()
    else:
        print("Invalid table selection.")
    input('Press Enter to return to main menu...')

def update_data():
    print('\n Update Data selected.')

    for key, desc in tables.items(): print(f"{key}. {desc.split('\n')[0]}")  

    choice = input('Choose a table number to update: ')
    if choice in tables:
        info = tables[choice]
        table_name = info.split('\n')[0] 
        columns = info.split('\n')[1].strip().split(': ')[1].split(', ') 
        print(f"Selected Table: {table_name}")

        print("Available Columns:", ', '.join(columns)) 
        column = input("Enter the column name for the record to update (e.g., ID): ")
        if column not in columns:
            print("Invalid column name.")
            return
        value = input(f"Enter the value of {column} for the record to update: ")
        update_field = input("Enter the column name you want to update: ")
        if update_field not in columns:
            print("Invalid update column name.")
            return
        new_value = input(f"Enter the new value for {update_field}: ")

        query = f"UPDATE {table_name} SET {update_field} = %s WHERE {column} = %s"
        
        try:
            cur.execute(query, (new_value, value))
            conn.commit()
            print("Record updated successfully.")
        except Exception as e:
            print(f"Error updating data: {e}")
            conn.rollback()
    else:
        print("Invalid table selection.")

    input('Press Enter to return to main menu...')

def search_data():
    print('\nSearch Data selected.')

    for key, desc in tables.items():
        table_name = desc.split('\n')[0] 
        print(f"{key}. {table_name}") 

    choice = input('Choose a table number to search in: ')
    if choice in tables:
        info = tables[choice].split('\n')[0]
        print(f"Selected Table: {info}")

        column = input("Enter the column name to search by (e.g., Name): ")
        condition = input(f"Enter the search condition (e.g., =, >, <, LIKE): ")
        value = input(f"Enter the search value: ")

        if condition.upper() == 'LIKE':
            value = f"%{value}%"  

        query = f"SELECT * FROM {info} WHERE {column} {condition} %s"

        try:
            cur.execute(query, (value,))
            results = cur.fetchall()
            if results:
                print(f"Search results from {info}:")
                for row in results:
                    print(row)
            else:
                print("No records found.")
        except Exception as e:
            print(f"Error performing search: {e}")

    else:
        print("Invalid selection. Please enter a valid number.")
    input('Press Enter to return to main menu...')

def aggregate_function():
    print('\nAggregate Functions selected.')

    for key, desc in tables.items():
        table_name = desc.split('\n')[0]  
        print(f"{key}. {table_name}")

    choice = input('Choose a table number for aggregation: ')
    if choice in tables:

        info = tables[choice].split('\n')[0]
        print(f"Selected Table for Aggregation: {info}")

        column = input('Enter the column name to perform the aggregation on: ')
        operation = input('Enter the operation (sum, avg, count, min, max): ').lower()

        if operation in ['sum', 'avg', 'count', 'min', 'max']:
            if operation == 'avg':
                sql_operation = 'AVG'
            else:
                sql_operation = operation.upper()

            query = f"SELECT {sql_operation}({column}) FROM {info}"

            try:
                cur.execute(query)
                result = cur.fetchone()
                if result and result[0] is not None:
                    print(f"The result of {sql_operation}({column}) on {info} is: {result[0]}")
                else:
                    print(f"No data to aggregate in {info} with the given column.")
                    
            except Exception as e:
                print(f"Error performing aggregate function: {e}")
                conn.rollback()
        else:
            print("Invalid aggregation operation. Please choose sum, avg, count, min, or max.")
    else:
        print("Invalid table selection. Please enter a valid number.")
    input('Press Enter to return to main menu...')

def sorting():
    print('\n Sorting selected.')

    for key, desc in tables.items():
        table_name = desc.split('\n')[0]  
        print(f"{key}. {table_name}")

    choice = input('Choose a table number to sort by: ')
    if choice in tables:

        info = tables[choice].split('\n')[0]
        print(f"Selected Table for sorting: {info}")

        column = input('Enter the column name to sort by: ')
        order = input("Enter the sort order (ASC for ascending or DESC for descending): ").upper()

        if order not in ['ASC', 'DESC']:
            print("Invalid sort order. Please enter 'ASC' or 'DESC'.")
            return


        query = f"SELECT * FROM {info} ORDER BY {column} {order}"

        try:
            cur.execute(query)
            results = cur.fetchall()
            if results:
                print(f"Sorted results from {info}:")
                for row in results:
                    print(row)
            else:
                print("No records found.")
        except Exception as e:
            print(f"Error performing sorting: {e}")
    else:
        print("Invalid table selection. Please enter a valid number.")

    input('Press Enter to return to main menu...')

def joins():
    print('Join selected.')
    table1 = input('Enter the first table name: ')
    table2 = input('Enter the second table name: ')
    key1 = input(f'Enter the join key from {table1} (e.g., column name in {table1}): ')
    key2 = input(f'Enter the join key from {table2} (e.g., column name in {table2}): ')
    join_type = input("Enter the type of join (INNER, LEFT OUTER, RIGHT OUTER, FULL OUTER): ").upper()

    if join_type not in ['INNER', 'LEFT OUTER', 'RIGHT OUTER', 'FULL OUTER']:
        print("Invalid join type. Please enter 'INNER', 'LEFT OUTER', 'RIGHT OUTER', or 'FULL OUTER'.")
        return


    query = f""" SELECT * FROM {table1} {join_type} JOIN {table2} ON {table1}.{key1} = {table2}.{key2} """

    try:
        cur.execute(query)
        results = cur.fetchall()
        if results:
            print(f"Results from joining {table1} and {table2}:")
            for row in results:
                print(row)
        else:
            print("No records found.")
    except Exception as a:
        print(f"Error performing join: {a}")

    input('Press Enter to return to main menu...')

def grouping():
    for key, desc in tables.items():
        table_name = desc.split('\n')[0]  
        print(f"{key}. {table_name}")
    choice = input('Choose a table number: ')
    if choice in tables:
        sd = tables[choice]
        st = sd.split('\n')[0]
        selected_columns_part = sd.split('\n')[1].strip()
        selected_columns = selected_columns_part.split(': ')[1].split(', ')

        print(f"Selected Table: {st}")
        print(f"Columns available: {', '.join(selected_columns)}")

        column = input("Enter the column name to group by: ")
        ac = input("Enter the column name to apply the aggregate function on: ")
        af = input("Enter the aggregate function (COUNT, SUM, AVG, MAX, MIN): ").upper()

        query = f"SELECT {column}, {af}({ac}) FROM {st} GROUP BY {column}"
        
        try:
            cur.execute(query)
            results = cur.fetchall()
            if results:
                print(f"Results of {af}({ac}) grouped by {column}:")
                for result in results:
                    print(result)
            else:
                print("No results found.")
        except Exception as e:
            print(f"Error executing grouping query: {e}")
    else:
        print("Invalid table selection. Please try again.")

    input('Press Enter to return to main menu...')

def subqueries():
    print('\n Subqueries selected.')
    
    print("You can enter any SQL query to execute. Make sure it is correctly formatted.\n")
    
    entry = input("Please enter your SQL query: ")
    
    print("Your SQL query: " + entry)
    confirm = input("Do you want to execute this query? (yes/no): ").lower()
    if confirm == 'yes':
        try:
            cur.execute(entry) 
            if cur.description:  
                results = cur.fetchall()
                print("Query results:")
                for row in results:
                    print(row)
                if not results:
                    print("No data found.")
            else:
                conn.commit()
                print("Query done successfully.")
        except Exception as e:
            print(f"Error executing query: {e}")
            conn.rollback()  
    else:
        print("Query execution canceled.")

    input('Press Enter to return to main menu...')

def transactions():
    print('\n Transactions selected.')
    while True:
        print("Available actions:")
        print("1. Insert Data")
        print("2. Delete Data")
        print("3. Update Data")
        print("4. Exit this menu")
        
        action = input("Choose an action (1-4): ")

        if action == '1':
            insert_data() 
        elif action == '2':
            delete_data() 
        elif action == '3':
            update_data()  
        elif action == '4':
            print("Exiting transactions menu.")
            break 
        else:
            print("Invalid selection.")
        print("\n")
    input('Press Enter to return to main menu...')

def error_handling():
    print('\n Error Handling selected.')
    print('\n Python script already uses error handling at every function call to ensure correctness.\n')
    input('Press Enter to return to main menu...')


if __name__ == '__main__':
    try:
        while True:
            user_choice = mainMenu()
            if user_choice == '1':
                insert_data()
            elif user_choice == '2':
                delete_data()
            elif user_choice == '3':
                update_data()
            elif user_choice == '4':
                search_data()        
            elif user_choice == '5':
                aggregate_function()
            elif user_choice == '6':
                sorting()
            elif user_choice == '7':
                joins()  
            elif user_choice == '8':
                grouping()  
            elif user_choice == '9':
                subqueries()
            elif user_choice == '10':
                transactions()  
            elif user_choice == '11':
                error_handling()                
            elif user_choice == '12':
                print('\nExiting the Database CLI. Goodbye!')
                sys.exit()
            else:
                print('\nInvalid choice, please select a number between 1 and 12.')
    except  KeyboardInterrupt:
        print('\n Thanks....Passive Aggresively....')  
