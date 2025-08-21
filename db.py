import sqlite3
from constants import DATABASE_NAME, CREATE_QUERY

def InitializeDatabase(): 
    print("Initializing database...")
    
    # define database connection
    connection = sqlite3.connect(DATABASE_NAME)
    print("Database connection established.")

    # define cursor used to query the database and execute SQL commands
    cursor = connection.cursor()

    # create the cigar_reviews table
    print("Creating database and tables if they do not exist...")
    command_create_db_if_exists = CREATE_QUERY 

    # execute the cursor to call the create table query (will not recreate if it already exists see the query in constants.py)
    cursor.execute(command_create_db_if_exists)
    print("Table creation command executed successfully.")
    
    # commit the changes to the database
    connection.commit()

    # fetching all cigars from the cigar_reviews table 
    #print("Fetching all records from cigar_reviews table...")
    #cursor.execute("SELECT * FROM cigar_reviews")
    #records = cursor.fetchall()
    #print(f"Fetched {len(records)} records from cigar_reviews table.")  
    #print(records)  # print the fetched records
    
    # close the cursor
    cursor.close()

    print("Database initialization completed successfully.")


def CloseDatabaseConnection():
    print("Closing database connection...")
    connection = sqlite3.connect(DATABASE_NAME)
    connection.close()
    print("Database connection closed.")

def AddCigarReview(brand, line, vitola, ring_gauge, country, wrapper, binder, filler, date_smoked, rating, notes, price_cents, humidor, tags):
    print("Adding a new cigar review...")
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    insert_query = """INSERT INTO cigar_reviews 
                      (brand, line, vitola, ring_gauge, country, wrapper, binder, filler, date_smoked, rating, notes, price_cents, humidor, tags) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    
    cursor.execute(insert_query, (brand, line, vitola, ring_gauge, country, wrapper, binder, filler, date_smoked, rating, notes, price_cents, humidor, tags))
    
    connection.commit()
    cursor.close()
    connection.close()
    print("Cigar review added successfully.")

    
