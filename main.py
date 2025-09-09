import sys
from db import InitializeDatabase, CloseDatabaseConnection, AddCigarReview, FetchCigarReviewById, UpdateCigarReview, FetchAllCigarReviews, DeleteCigarReview
from constants import ALL_COLUMNS
import pandas as pd
import textwrap
from tabulate import tabulate
from rich.console import Console
from rich.table import Table
from validate import is_valid_date, is_valid_string, is_valid_integer

def main_menu():
    print("Starting MyLeafLedger")

    InitializeDatabase()    # Ensure the database is initialized
    while True: # this will keep the menu running until the user decides to exit or it crashes miserably
        print("\n🚬 My Leaf Ledger - Cigar Review CLI Main Menu: 🚬")
        print("1. Add a Cigar Review")
        print("2. Edit a Cigar Review")
        print("3. View All Reviews")
        print("4. Query Reviews")
        print("5. Fancy Report")
        print("6. Delete a Cigar Review")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print("You selected Option 1 to Add a Cigar Review")
            
            #brand
            while True:
                brand = input("Enter brand: ")
                if is_valid_string(brand):
                    print(f"Valid brand entered: {brand}")
                    break
                else:
                    print("Invalid brand. Please use only letters, numbers, spaces, hyphens, and apostrophes.")
            
            #line
            while True:
                line = input("Enter line: ")
                if is_valid_string(line):
                    print(f"Valid line entered: {line}")
                    break
                else:
                    print("Invalid line. Please use only letters, numbers, spaces, hyphens, and apostrophes.")

            #vitola
            while True:
                vitola = input("Enter vitola: ")
                if is_valid_string(vitola):
                    print(f"Valid vitola entered: {vitola}")
                    break
                else:
                    print("Invalid vitola. Please use only letters, numbers, spaces, hyphens, and apostrophes.")
            
            #ring_gauge
            while True:
                ring_gauge = input("Enter ring gauge (in mm): ")
                if is_valid_integer(ring_gauge):
                    print(f"Valid ring gauge entered: {ring_gauge}")
                    break
                else:
                    print("Invalid ring gauge. Please enter a valid integer (e.g., 50).")
            
            #country
            while True:
                country = input("Enter country: ")
                if is_valid_string(country):
                    print(f"Valid country entered: {country}")
                    break
                else:
                    print("Invalid country. Please use only letters, numbers, spaces, hyphens, and apostrophes.")
            
            #wrappper
            while True:
                wrapper = input("Enter wrapper (optional): ")
                if wrapper == "" or is_valid_string(wrapper):
                    print(f"Valid wrapper entered: {wrapper}")
                    break
                else:
                    print("Invalid wrapper. Please use only letters, numbers, spaces, hyphens, and apostrophes.")

            #binder
            while True:
                binder = input("Enter binder (optional): ")
                if binder == "" or is_valid_string(binder):
                    print(f"Valid binder entered: {binder}")
                    break
                else:
                    print("Invalid binder. Please use only letters, numbers, spaces, hyphens, and apostrophes.")
            

            #filler
            while True:
                filler = input("Enter filler (optional): ")
                if filler == "" or is_valid_string(filler):
                    print(f"Valid filler entered: {filler}")
                    break
                else:
                    print("Invalid filler. Please use only letters, numbers, spaces, hyphens, and apostrophes.")
            
            
            #date_smoked = input("Enter date smoked (YYYY-MM-DD): ")
            while True:
                date_smoked = input("Enter date smoked (YYYY-MM-DD): ")
                if is_valid_date(date_smoked):
                    print(f"Valid date entered: {date_smoked}")
                    break
                else:
                    print("Invalid date. Please use YYYY-MM-DD format (e.g., 2025-09-09).")

            #rating
            while True:
                rating = input("Enter rating (1-5): ")
                if is_valid_integer(rating) and 1 <= int(rating) <= 5:
                    print(f"Valid rating entered: {rating}")
                    break
                else:
                    print("Invalid rating. Please enter an integer between 1 and 5.")
            
            #notes
            while True:
                notes = input("Enter notes (optional): ")
                if notes == "" or is_valid_string(notes):
                    print(f"Valid notes entered: {notes}")
                    break
                else:
                    print("Invalid notes. Please use only letters, numbers, spaces, hyphens, and apostrophes.")

            #price
            while True:
                price_cents = input("Enter price in cents (optional): ")
                if price_cents == "" or (is_valid_integer(price_cents) and int(price_cents) >= 0):
                    print(f"Valid price entered: {price_cents}")
                    break
                else:
                    print("Invalid price. Please enter a non-negative integer (e.g., 500 for $5.00) or leave blank.")

            #humidor
            while True:
                humidor = input("Enter humidor location (optional): ")
                if humidor == "" or is_valid_string(humidor):
                    print(f"Valid humidor location entered: {humidor}")
                    break
                else:
                    print("Invalid humidor location. Please use only letters, numbers, spaces, hyphens, and apostrophes.")  
            
            #tags
            while True:
                tags = input("Enter tags (CSV, e.g. 'maduro,box-press') (optional): ")
                if tags == "" or all(is_valid_string(tag.strip()) for tag in tags.split(',')):
                    print(f"Valid tags entered: {tags}")
                    break
                else:
                    print("Invalid tags. Please use only letters, numbers, spaces, hyphens, and apostrophes in each tag, separated by commas.")
            
            try:
                AddCigarReview(brand, line, vitola, ring_gauge, country, wrapper, binder, filler, date_smoked, rating, notes, price_cents, humidor, tags)
            except Exception as e:
                print(f"Error adding review: {e}")
                continue    

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
            print("You selected Option 3 to view All Reviews")
            
            records = FetchAllCigarReviews()
            if records:   
                pd.set_option ('display.max_columns', None)  # Show all columns
                df = pd.DataFrame(records, columns=ALL_COLUMNS)
                df['notes'] = df['notes'].apply(lambda x: '\n'.join(textwrap.wrap(str(x), width=50))) # wrap notes column only with this voodoo
                pd.set_option('display.max_colwidth', None)
                print(tabulate(df, headers=ALL_COLUMNS, tablefmt='simple', showindex=False, maxcolwidths=[10] * len(ALL_COLUMNS)))  # None for unlimited, or e.g., 50 for 'notes'

        elif choice == '4':
            print("You selected Option 4 to Query Reviews")
            print("Feature not implemented yet. Stay tuned!")

        elif choice == '5':
            print("Option 5 Fancy Report")

            records = FetchAllCigarReviews()
            if records:   
                pd.set_option ('display.max_columns', None)  # Show all columns
                df = pd.DataFrame(records, columns=ALL_COLUMNS)
                df['notes'] = df['notes'].apply(lambda x: '\n'.join(textwrap.wrap(str(x), width=50))) # wrap notes column only with this voodoo
                pd.set_option('display.max_colwidth', None)
                #print(tabulate(df, headers=ALL_COLUMNS, tablefmt='simple', showindex=False, maxcolwidths=[10] * len(ALL_COLUMNS)))  # None for unlimited, or e.g., 50 for 'notes'
            # Create a rich console and table
            console = Console()
            table = Table(title="Cigar Reviews", show_header=True, header_style="bold cyan")
            
            # Add columns with optional styles (adjust as needed)
            for col in ALL_COLUMNS:
                if col == 'brand':
                    table.add_column(col, style="green", justify="left")
                elif col == 'rating':
                    table.add_column(col, style="magenta", justify="center")
                elif col == 'notes':
                    table.add_column(col, style="italic white", justify="left", width=50)  # Wider for wrapped notes
                else:
                    table.add_column(col, style="white", justify="left")
            
            # Add rows from DataFrame (convert all to str for safety)
            for _, row in df.iterrows():
                table.add_row(*[str(value) for value in row])
            
            # Print the rich table
            console.print(table)

        elif choice == '6':
            print("You selected Option 6 to Delete a Cigar Review")
            id = input("Enter the ID of the review to delete: ")
            record = FetchCigarReviewById(id)
            if record:
                confirm = input(f"Are you sure you want to delete the review with ID {id}? (yes/no): ")
                if confirm.lower() == 'yes':
                    DeleteCigarReview(id)
                    print(f"Review with ID {id} deleted successfully!")
                else:
                    print("Deletion cancelled.")

        elif choice == '7':
            print("Exiting MyLeafLedger. Goodbye!")
            # close the database connection before exiting
            CloseDatabaseConnection()
            break
        else:
            print("Invalid choice. Please try again.")
    
if __name__ == "__main__":
    main_menu()