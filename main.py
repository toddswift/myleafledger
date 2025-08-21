import sys
from db import InitializeDatabase, CloseDatabaseConnection, AddCigarReview
from constants import DATABASE_NAME, CREATE_QUERY


def main_menu():
    print("Starting MyLeafLedger")

    InitializeDatabase()    # Ensure the database is initialized
    while True: # this will keep the menu running until the user decides to exit or it crashes miserably
        print("\n🚬 My Leaf Ledger - Cigar Review CLI Main Menu: 🚬")
        print("1. Add a Cigar Review")
        print("2. Edit a Cigar Review (coming soon...)")
        print("3. View Reviews (coming soon...)")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("You selected Option 1 to Add a Cigar Review")
            brand = input("Enter brand: ")
            line = input("Enter line: ")
            vitola = input("Enter vitola: ")
            ring_gauge = input("Enter ring gauge (in mm): ")
            country = input("Enter country: ")
            wrapper = input("Enter wrapper (optional): ")
            binder = input("Enter binder (optional): ")
            filler = input("Enter filler (optional): ")
            date_smoked = input("Enter date smoked (YYYY-MM-DD): ")
            rating = input("Enter rating (1-5): ")
            notes = input("Enter notes (optional): ")
            price_cents = input("Enter price in cents (optional): ")
            humidor = input("Enter humidor location (optional): ")
            tags = input("Enter tags (CSV, e.g. 'maduro,box-press') (optional): ")
            
            AddCigarReview(brand, line, vitola, ring_gauge, country, wrapper, binder, filler, date_smoked, rating, notes, price_cents, humidor, tags)

            print(f"Review for {brand, line, vitola} added successfully!")   

        elif choice == '2':
            print("You selected Option 2")
            # Add functionality for Option 2 here
        elif choice == '3':
            print("You selected Option 3")
            # Add functionality for Option 3 here
        elif choice == '4':
            print("Exiting MyLeafLedger. Goodbye!")
            # close the database connection before exiting
            CloseDatabaseConnection()
            break
        else:
            print("Invalid choice. Please try again.")
    

if __name__ == "__main__":
    main_menu()