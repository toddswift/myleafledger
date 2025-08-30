import unittest
from unittest.mock import patch
import io
import sys

import main  # Assuming the file is named main.py

# Define the columns based on the db schema
ALL_COLUMNS = [
    'id', 'brand', 'line', 'vitola', 'ring_gauge', 'country', 'wrapper', 'binder', 'filler',
    'date_smoked', 'rating', 'notes', 'price_cents', 'humidor', 'tags', 'created_at', 'updated_at'
]

class TestMainMenu(unittest.TestCase):
    def setUp(self):
        # Patch ALL_COLUMNS
        self.patch_all_columns = patch('main.ALL_COLUMNS', ALL_COLUMNS)
        self.patch_all_columns.start()

    def tearDown(self):
        self.patch_all_columns.stop()

    def run_main_menu_with_inputs(self, inputs):
        original_stdout = sys.stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        sys.stdin = io.StringIO(inputs)
        
        try:
            main.main_menu()
        finally:
            sys.stdout = original_stdout
            sys.stdin = sys.__stdin__  # Restore original stdin
        
        return captured_output.getvalue()

    @patch('main.CloseDatabaseConnection')
    @patch('main.InitializeDatabase')
    @patch('main.AddCigarReview')
    def test_add_review(self, mock_add, mock_init, mock_close):
        inputs = (
            '1\n'  # Choice
            'TestBrand\n'  # brand
            'TestLine\n'  # line
            'TestVitola\n'  # vitola
            '50\n'  # ring_gauge
            'TestCountry\n'  # country
            'TestWrapper\n'  # wrapper
            'TestBinder\n'  # binder
            'TestFiller\n'  # filler
            '2023-01-01\n'  # date_smoked
            '4.5\n'  # rating
            'Test notes\n'  # notes
            '1500\n'  # price_cents
            'TestHumidor\n'  # humidor
            'tag1,tag2\n'  # tags
            '7\n'  # Exit
        )
        output = self.run_main_menu_with_inputs(inputs)
        
        mock_init.assert_called_once()
        mock_add.assert_called_once_with(
            'TestBrand', 'TestLine', 'TestVitola', '50', 'TestCountry',
            'TestWrapper', 'TestBinder', 'TestFiller', '2023-01-01', '4.5',
            'Test notes', '1500', 'TestHumidor', 'tag1,tag2'
        )
        mock_close.assert_called_once()
        
        self.assertIn('Review for', output)
        self.assertIn('added successfully!', output)
        self.assertIn('Exiting MyLeafLedger. Goodbye!', output)

    @patch('main.CloseDatabaseConnection')
    @patch('main.InitializeDatabase')
    @patch('main.UpdateCigarReview')
    @patch('main.FetchCigarReviewById')
    def test_edit_review(self, mock_fetch, mock_update, mock_init, mock_close):
        mock_fetch.return_value = (1, 'OldBrand', 'OldLine', 'OldVitola', 50, 'OldCountry',
                                   'OldWrapper', 'OldBinder', 'OldFiller', '2023-01-01', 4.5,
                                   'Old notes', 1500, 'OldHumidor', 'old,tag', '2023-01-01', '2023-01-01')
        
        inputs = (
            '2\n'  # Choice
            '1\n'  # ID
            'NewBrand\n'  # brand
            'NewLine\n'  # line
            'NewVitola\n'  # vitola
            '52\n'  # ring_gauge
            'NewCountry\n'  # country
            'NewWrapper\n'  # wrapper
            'NewBinder\n'  # binder
            'NewFiller\n'  # filler
            '2024-01-01\n'  # date_smoked
            '5.0\n'  # rating
            'New notes\n'  # notes
            '2000\n'  # price_cents
            'NewHumidor\n'  # humidor
            'new,tag\n'  # tags
            '7\n'  # Exit
        )
        output = self.run_main_menu_with_inputs(inputs)
        
        mock_init.assert_called_once()
        mock_fetch.assert_called_once_with('1')
        mock_update.assert_called_once_with(
            '1', 'NewBrand', 'NewLine', 'NewVitola', '52', 'NewCountry',
            'NewWrapper', 'NewBinder', 'NewFiller', '2024-01-01', '5.0',
            'New notes', '2000', 'NewHumidor', 'new,tag'
        )
        mock_close.assert_called_once()
        
        self.assertIn('Current review details:', output)
        self.assertIn('updated successfully!', output)
        self.assertIn('Exiting MyLeafLedger. Goodbye!', output)

    @patch('main.CloseDatabaseConnection')
    @patch('main.InitializeDatabase')
    @patch('main.FetchAllCigarReviews')
    def test_view_all_reviews(self, mock_fetch_all, mock_init, mock_close):
        mock_fetch_all.return_value = [
            (1, 'TestBrand', 'TestLine', 'TestVitola', 50, 'TestCountry',
             'TestWrapper', 'TestBinder', 'TestFiller', '2023-01-01', 4.5,
             'Test notes that are a bit longer to test wrapping', 1500, 'TestHumidor', 'tag1,tag2',
             '2023-01-01 00:00:00', '2023-01-01 00:00:00')
        ]
        
        inputs = '3\n7\n'  # View all, then exit
        output = self.run_main_menu_with_inputs(inputs)
        
        mock_init.assert_called_once()
        mock_fetch_all.assert_called_once()
        mock_close.assert_called_once()
        
        self.assertIn('TestBrand', output)
        self.assertIn('4.5', output)
        self.assertIn('Test notes that are a bit', output)  # Part of wrapped notes
        self.assertIn('Exiting MyLeafLedger. Goodbye!', output)

    @patch('main.CloseDatabaseConnection')
    @patch('main.InitializeDatabase')
    def test_query_reviews(self, mock_init, mock_close):
        inputs = '4\n7\n'  # Query, then exit
        output = self.run_main_menu_with_inputs(inputs)
        
        mock_init.assert_called_once()
        mock_close.assert_called_once()
        
        self.assertIn('Feature not implemented yet. Stay tuned!', output)
        self.assertIn('Exiting MyLeafLedger. Goodbye!', output)

    @patch('main.CloseDatabaseConnection')
    @patch('main.InitializeDatabase')
    @patch('main.FetchAllCigarReviews')
    def test_fancy_report(self, mock_fetch_all, mock_init, mock_close):
        mock_fetch_all.return_value = [
            (1, 'TestBrand', 'TestLine', 'TestVitola', 50, 'TestCountry',
             'TestWrapper', 'TestBinder', 'TestFiller', '2023-01-01', 4.5,
             'Test notes that are a bit longer to test wrapping', 1500, 'TestHumidor', 'tag1,tag2',
             '2023-01-01 00:00:00', '2023-01-01 00:00:00')
        ]
        
        inputs = '5\n7\n'  # Fancy report, then exit
        output = self.run_main_menu_with_inputs(inputs)
        
        mock_init.assert_called_once()
        mock_fetch_all.assert_called_once()
        mock_close.assert_called_once()
        
        # Check for rich table elements (ANSI codes might be present, but check content)
        self.assertIn('Cigar Reviews', output)
        self.assertIn('TestBrand', output)
        self.assertIn('4.5', output)
        self.assertIn('Test notes', output)
        self.assertIn('Exiting MyLeafLedger. Goodbye!', output)

    @patch('main.CloseDatabaseConnection')
    @patch('main.InitializeDatabase')
    @patch('main.DeleteCigarReview')
    @patch('main.FetchCigarReviewById')
    def test_delete_review_confirm(self, mock_fetch, mock_delete, mock_init, mock_close):
        mock_fetch.return_value = (1, 'TestBrand', 'TestLine', 'TestVitola', 50, 'TestCountry',
                                   'TestWrapper', 'TestBinder', 'TestFiller', '2023-01-01', 4.5,
                                   'Test notes', 1500, 'TestHumidor', 'tag1,tag2', '2023-01-01', '2023-01-01')
        
        inputs = (
            '6\n'  # Choice
            '1\n'  # ID
            'yes\n'  # Confirm
            '7\n'  # Exit
        )
        output = self.run_main_menu_with_inputs(inputs)
        
        mock_init.assert_called_once()
        mock_fetch.assert_called_once_with('1')
        mock_delete.assert_called_once_with('1')
        mock_close.assert_called_once()
        
        self.assertIn('Are you sure', output)
        self.assertIn('deleted successfully!', output)
        self.assertIn('Exiting MyLeafLedger. Goodbye!', output)

    @patch('main.CloseDatabaseConnection')
    @patch('main.InitializeDatabase')
    @patch('main.DeleteCigarReview')
    @patch('main.FetchCigarReviewById')
    def test_delete_review_cancel(self, mock_fetch, mock_delete, mock_init, mock_close):
        mock_fetch.return_value = (1, 'TestBrand', 'TestLine', 'TestVitola', 50, 'TestCountry',
                                   'TestWrapper', 'TestBinder', 'TestFiller', '2023-01-01', 4.5,
                                   'Test notes', 1500, 'TestHumidor', 'tag1,tag2', '2023-01-01', '2023-01-01')
        
        inputs = (
            '6\n'  # Choice
            '1\n'  # ID
            'no\n'  # Confirm
            '7\n'  # Exit
        )
        output = self.run_main_menu_with_inputs(inputs)
        
        mock_init.assert_called_once()
        mock_fetch.assert_called_once_with('1')
        mock_delete.assert_not_called()
        mock_close.assert_called_once()
        
        self.assertIn('Are you sure', output)
        self.assertIn('Deletion cancelled.', output)
        self.assertIn('Exiting MyLeafLedger. Goodbye!', output)

    @patch('main.CloseDatabaseConnection')
    @patch('main.InitializeDatabase')
    def test_invalid_choice(self, mock_init, mock_close):
        inputs = '8\n7\n'  # Invalid, then exit
        output = self.run_main_menu_with_inputs(inputs)
        
        mock_init.assert_called_once()
        mock_close.assert_called_once()
        
        self.assertIn('Invalid choice. Please try again.', output)
        self.assertIn('Exiting MyLeafLedger. Goodbye!', output)

if __name__ == '__main__':
    unittest.main()