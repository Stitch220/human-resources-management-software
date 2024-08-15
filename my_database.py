import sqlite3

########## INITIALIZING FUNCTIONS ##########

# Establish a connection to the database. If the database does not exist, create a new one
def create_database_connection(new_database):
    try:
        con = sqlite3.connect(new_database)
        return con
    except sqlite3.Error as err:
        print(f"Error connecting to database: {err}")
        return None


# Creates a new table in the database with initial columns
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

########## DYNAMIC COLUMN FUNCTIONS ##########

# Adds a new column to the table
def add_column(database, table, column_name, column_type="TEXT"):

    # Check if the column already exists
    if not column_exists(database, table, column_name):
        alter_query = f"ALTER TABLE {table} ADD COLUMN {column_name} {column_type}"
        execute_query(database, alter_query)
        print(f"Added column {column_name} to {table} successfully!")
    else:
        print(f"Column {column_name} already exists in {table}.")


# Checks if column already exists
def column_exists(database, table, column_name):
    query = f"PRAGMA table_info({table})"
    columns = execute_query(database, query)
    for col in columns:
        if col[1] == column_name:
            return True
    return False
          
########## DATA ENTRY FUNCTION ##########

# Adds entrys to the table. If column does not exist, creates a new one
def add_entry(database, table, data):
    for column_name, value in data.items():
        if not column_exists(database, table, column_name):
            add_column(database, table, column_name, "TEXT")

    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data.values()])
    values = tuple(data.values())
    
    insert_query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    execute_query(database, insert_query, values)
    print(f"Added entry successfully!")


# Updates an existing entry. If entry does not exist creates a new one
def update_entry(database, table, data, entry_id):
    
    for column_name, value in data.items():
        if not column_exists(database, table, column_name):
            add_column(database, table, column_name, "TEXT")

    set_clause = ", ".join([f"{column} = ?" for column in data.keys()])
    values = tuple(data.values()) + (entry_id,)

    update_query = f"UPDATE {table} SET {set_clause} WHERE id = ?"
    
    execute_query(database, update_query, values)
    print(f"Entry {entry_id} updated successfully!")


# Reads a single entry (row)
def read_single_entry(database, table, entry_id):
    select_query = f"SELECT * FROM {table} WHERE id = ?"
    results = execute_query(database, select_query, (entry_id,))
    if len(results) == 1:
        print(f"Retrieved entry {entry_id} successfully!")
        return results[0]
    else:
        print(f"Entry {entry_id} not found!")
        return None
    

# Reads a specific stat from entry
def read_specific_entry(database, table, select_column, where_column, value_column):
    select_query = f"SELECT {select_column} FROM {table} WHERE {where_column} = ?"
    results = execute_query(database, select_query, (value_column,))
    if results:
        print(f"Retrieved Data successfully!")
        return results
    else:
        print(f"Entry not found!")
        return None


# Deletes entry
def delete_entry(database, table, entry_id):
    delete_query = "DELETE FROM {table} WHERE id = ?"
    execute_query(delete_query, entry_id)
    print(f"Deleted entry: {entry_id} successfully!")