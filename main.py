import sqlite3
from constants import DATABASE_NAME, CREATE_QUERY


def main():
    print("Starting MyLeafLedger")

    print("Establishing database connection...")
    # define database connection
    connection = sqlite3.connect(DATABASE_NAME)

    print("Database connection established.")
    # define cursor used to query the database and execute SQL commands
    cursor = connection.cursor()

    # create the cigar_reviews table
    command_create_db_if_exists = CREATE_QUERY

    # execute the cursor to call the create table query (will not recreate if it already exists) - my first technical debt!
    # todo:// check if table exists before creating
    print("Executing command to create table if it does not exist...")
    cursor.execute(command_create_db_if_exists)
    print("Table creation command executed successfully.")
    # commit the changes to the database
    connection.commit()

    # fetching all cigars from the cigar_reviews table 
    print("Fetching all records from cigar_reviews table...")
    cursor.execute("SELECT * FROM cigar_reviews")
    records = cursor.fetchall()
    print(f"Fetched {len(records)} records from cigar_reviews table.")  
    print(records)  # print the fetched records
    
 
    # close the cursor
    cursor.close()

    # close the connection
    connection.close()
    print("Database connection closed.")
    print("Database operations completed successfully.")
    
    

if __name__ == "__main__":
    main()