import sqlite3

# Establish a connection to the database. If the database does not exist, create a new one
def create_database_connection(new_database):
    try:
        con = sqlite3.connect(new_database)
        return con
    except sqlite3.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# Creates a new table in the database
def create_table(database, new_table):
    try:
        con = create_database_connection(database)
        cursor = con.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {new_table} (id INTEGER PRIMARY KEY AUTOINCREMENT)")
        print(f"Created {new_table} successfully!")
        con.commit()
        cursor.close()
    except sqlite3.Error as err:
        print(f"Error creating {new_table} table: {err}")

# Executes SQL queries and returns the results
def execute_query(database, query, params=None):
    try:
        con = create_database_connection(database)
        cursor = con.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        con.commit()
        results = cursor.fetchall()
        cursor.close()
        return results
    except sqlite3.Error as err:
        print(f"Error executing query: {err}")
        return []

########## FUNCTIONS IN PROGRAM ##########

def add_entry(database, table, columns, values):
    placeholders = ", ".join(["?" for _ in values])
    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    execute_query(database, insert_query, values)
    print("Added entry successfully!")


