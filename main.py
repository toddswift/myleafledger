import sqlite3
from constants import DATABASE_NAME, CREATE_QUERY


def main():
    print("Starting MyLeafLedger")

    # define database connection
    connection = sqlite3.connect(DATABASE_NAME)

    # define cursor used to query the database and execute SQL commands
    cursor = connection.cursor()

    # create the cigar_reviews table query
    command_create_db_if_exists = CREATE_QUERY

    # create the cursor and create a table if it does not exist
    cursor.execute(command_create_db_if_exists)

    # commit the changes to the database
    connection.commit()
    


if __name__ == "__main__":
    main()