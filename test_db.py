import unittest
from unittest.mock import patch
import tempfile
import os

import db  # Import your db module

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        os.close(self.db_fd)  # Close the file descriptor; the module will handle connections

        # Patch DATABASE_NAME to use the temp file
        self.patch_db_name = patch('db.DATABASE_NAME', self.db_path)
        self.patch_db_name.start()

        # Patch CREATE_QUERY with the assumed table schema (based on your code's usage)
        self.patch_create_query = patch('db.CREATE_QUERY', """
            CREATE TABLE IF NOT EXISTS cigar_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand TEXT,
                line TEXT,
                vitola TEXT,
                ring_gauge INTEGER,
                country TEXT,
                wrapper TEXT,
                binder TEXT,
                filler TEXT,
                date_smoked DATE,
                rating REAL,
                notes TEXT,
                price_cents INTEGER,
                humidor TEXT,
                tags TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.patch_create_query.start()

        # Patch INSERT_QUERY with the assumed insert statement (matching the 14 parameters)
        self.patch_insert_query = patch('db.INSERT_QUERY', """
            INSERT INTO cigar_reviews 
            (brand, line, vitola, ring_gauge, country, wrapper, binder, filler, date_smoked, rating, notes, price_cents, humidor, tags) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """)
        self.patch_insert_query.start()

        # Initialize the database for each test
        db.InitializeDatabase()

    def tearDown(self):
        # Stop patches
        self.patch_db_name.stop()
        self.patch_create_query.stop()
        self.patch_insert_query.stop()

        # Clean up the temp database file
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_add_and_fetch_all_cigar_reviews(self):
        # Add a review
        db.AddCigarReview(
            brand='TestBrand', line='TestLine', vitola='TestVitola', ring_gauge=50,
            country='TestCountry', wrapper='TestWrapper', binder='TestBinder', filler='TestFiller',
            date_smoked='2023-01-01', rating=9.5, notes='Test notes', price_cents=1500,
            humidor='TestHumidor', tags='tag1,tag2'
        )

        # Fetch all
        records = db.FetchAllCigarReviews()
        self.assertEqual(len(records), 1)

        # Verify the inserted data (ignoring id, created_at, updated_at for exact matches, but check types/positions)
        record = records[0]
        self.assertEqual(record[1], 'TestBrand')  # brand
        self.assertEqual(record[2], 'TestLine')   # line
        self.assertEqual(record[3], 'TestVitola') # vitola
        self.assertEqual(record[4], 50)           # ring_gauge
        self.assertEqual(record[5], 'TestCountry')# country
        self.assertEqual(record[6], 'TestWrapper')# wrapper
        self.assertEqual(record[7], 'TestBinder') # binder
        self.assertEqual(record[8], 'TestFiller') # filler
        self.assertEqual(record[9], '2023-01-01') # date_smoked
        self.assertEqual(record[10], 9.5)         # rating
        self.assertEqual(record[11], 'Test notes')# notes
        self.assertEqual(record[12], 1500)        # price_cents
        self.assertEqual(record[13], 'TestHumidor')# humidor
        self.assertEqual(record[14], 'tag1,tag2') # tags
        self.assertIsNotNone(record[15])          # created_at
        self.assertIsNotNone(record[16])          # updated_at

    def test_fetch_cigar_review_by_id(self):
        # Add a review
        db.AddCigarReview(
            brand='TestBrand', line='TestLine', vitola='TestVitola', ring_gauge=50,
            country='TestCountry', wrapper='TestWrapper', binder='TestBinder', filler='TestFiller',
            date_smoked='2023-01-01', rating=9.5, notes='Test notes', price_cents=1500,
            humidor='TestHumidor', tags='tag1,tag2'
        )

        # Fetch by ID (assuming auto-increment starts at 1)
        record = db.FetchCigarReviewById(1)
        self.assertIsNotNone(record)
        self.assertEqual(record[1], 'TestBrand')

        # Test non-existent ID
        missing_record = db.FetchCigarReviewById(999)
        self.assertIsNone(missing_record)

    def test_update_cigar_review(self):
        # Add a review
        db.AddCigarReview(
            brand='OldBrand', line='OldLine', vitola='OldVitola', ring_gauge=40,
            country='OldCountry', wrapper='OldWrapper', binder='OldBinder', filler='OldFiller',
            date_smoked='2022-01-01', rating=8.0, notes='Old notes', price_cents=1000,
            humidor='OldHumidor', tags='oldtag'
        )

        # Update it
        db.UpdateCigarReview(
            id=1, brand='NewBrand', line='NewLine', vitola='NewVitola', ring_gauge=50,
            country='NewCountry', wrapper='NewWrapper', binder='NewBinder', filler='NewFiller',
            date_smoked='2023-01-01', rating=9.5, notes='New notes', price_cents=1500,
            humidor='NewHumidor', tags='newtag1,newtag2'
        )

        # Fetch and verify
        record = db.FetchCigarReviewById(1)
        self.assertEqual(record[1], 'NewBrand')
        self.assertEqual(record[2], 'NewLine')
        self.assertEqual(record[10], 9.5)  # rating
        self.assertEqual(record[14], 'newtag1,newtag2')  # tags

    def test_delete_cigar_review(self):
        # Add a review
        db.AddCigarReview(
            brand='TestBrand', line='TestLine', vitola='TestVitola', ring_gauge=50,
            country='TestCountry', wrapper='TestWrapper', binder='TestBinder', filler='TestFiller',
            date_smoked='2023-01-01', rating=9.5, notes='Test notes', price_cents=1500,
            humidor='TestHumidor', tags='tag1,tag2'
        )

        # Delete it
        db.DeleteCigarReview(1)

        # Fetch all and verify empty
        records = db.FetchAllCigarReviews()
        self.assertEqual(len(records), 0)

        # Fetch by ID should return None
        record = db.FetchCigarReviewById(1)
        self.assertIsNone(record)

    def test_close_database_connection(self):
        # This function opens and closes a connection; test it doesn't raise errors
        try:
            db.CloseDatabaseConnection()
        except Exception as e:
            self.fail(f"CloseDatabaseConnection raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()