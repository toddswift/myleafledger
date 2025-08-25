import sys
from db import InitializeDatabase, CloseDatabaseConnection, AddCigarReview, FetchCigarReviewById, UpdateCigarReview, FetchAllCigarReviews, DeleteCigarReview
from constants import ALL_COLUMNS
import pandas as pd
import textwrap
from tabulate import tabulate

def main_menu():
    print("Starting MyLeafLedger")

    InitializeDatabase()    # Ensure the database is initialized
    while True: # this will keep the menu running until the user decides to exit or it crashes miserably
        print("\n🚬 My Leaf Ledger - Cigar Review CLI Main Menu: 🚬")
        print("1. Add a Cigar Review")
        print("2. Edit a Cigar Review")
        print("3. View Reviews")
        print("4. Coming Soon... Reports")
        print("5. Delete a Cigar Review")
        print("6. Exit")
        
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
            print("You selected Option 2 to Update a Cigar Review")
            id = input("Enter the ID of the review to update: ")
            record = FetchCigarReviewById(id)
            if record:
                print("Current review details:")
                print(record)
                brand = input("Enter new brand: ")
                line = input("Enter new line: ")
                vitola = input("Enter new vitola: ")
                ring_gauge = input("Enter new ring gauge (in mm): ")
                country = input("Enter new country: ")
                wrapper = input("Enter new wrapper (optional): ")
                binder = input("Enter new binder (optional): ")
                filler = input("Enter new filler (optional): ")
                date_smoked = input("Enter new date smoked (YYYY-MM-DD): ")
                rating = input("Enter new rating (1-5): ")
                notes = input("Enter new notes (optional): ")
                price_cents = input("Enter new price in cents (optional): ")
                humidor = input("Enter new humidor location (optional): ")
                tags = input("Enter new tags (CSV, e.g. 'maduro,box-press') (optional): ")
                
                UpdateCigarReview(id, brand, line, vitola, ring_gauge, country, wrapper, binder, filler, date_smoked, rating, notes, price_cents, humidor, tags)
                print(f"Review with ID {id} updated successfully!")

        elif choice == '3':
            print("You selected Option 3 to view Reviews")
            
            records = FetchAllCigarReviews()
            if records:   
                pd.set_option ('display.max_columns', None)  # Show all columns
                df = pd.DataFrame(records, columns=ALL_COLUMNS)
                df['notes'] = df['notes'].apply(lambda x: '\n'.join(textwrap.wrap(str(x), width=50))) # wrap notes column only with this voodoo
                pd.set_option('display.max_colwidth', None)
                print(tabulate(df, headers=ALL_COLUMNS, tablefmt='simple', showindex=False, maxcolwidths=[10] * len(ALL_COLUMNS)))  # None for unlimited, or e.g., 50 for 'notes'

        elif choice == '4':
            print("Option 4 for Reports is coming soon!")

        elif choice == '5':
            print("You selected Option 5 to Delete a Cigar Review")
            id = input("Enter the ID of the review to delete: ")
            record = FetchCigarReviewById(id)
            if record:
                confirm = input(f"Are you sure you want to delete the review with ID {id}? (yes/no): ")
                if confirm.lower() == 'yes':
                    DeleteCigarReview(id)
                    print(f"Review with ID {id} deleted successfully!")
                else:
                    print("Deletion cancelled.")

        elif choice == '6':
            print("Exiting MyLeafLedger. Goodbye!")
            # close the database connection before exiting
            CloseDatabaseConnection()
            break
        else:
            print("Invalid choice. Please try again.")
    
if __name__ == "__main__":
    main_menu()