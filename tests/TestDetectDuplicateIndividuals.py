import unittest
from GedcomDataReader import detect_duplicate_individuals

class TestDetectDuplicateIndividuals(unittest.TestCase):
    def setUp(self):
        self.individuals_with_duplicates = {
            'I1': {'name': 'James/Smith/', 'birth': '2000-12-30', 'death': '2023-09-22'},
            'I2': {'name': 'John/Doe/', 'birth': '1990-01-01'},
            'I3': {'name': 'John/Doe/', 'birth': '1990-01-01'},
            'I4': {'name': 'Jane/Doe/', 'birth': '1990-02-01'}
        }
        self.individuals_without_duplicates = {
            'I1': {'name': 'James/Smith/', 'birth': '2000-12-30', 'death': '2023-09-22'},
            'I2': {'name': 'John/Doe/', 'birth': '1990-01-01'},
            'I3': {'name': 'Joylene/Summers/', 'birth': '1960-03-02'},
        }

    def test_no_duplicates(self):
        """Ensure no duplicates are detected when all individuals are unique."""
        duplicates = detect_duplicate_individuals(self.individuals_without_duplicates)
        self.assertEqual(duplicates, [], "Expected no duplicates, but found some.")

    def test_duplicates(self):
        """Ensure duplicates are correctly identified and their details are returned."""
        duplicates = detect_duplicate_individuals(self.individuals_with_duplicates)
        expected_duplicates = [('John/Doe/', '1990-01-01', 'I2', 'I3')]
        self.assertEqual(duplicates, expected_duplicates, "Duplicates detection mismatch.")

if __name__ == '__main__':
    unittest.main()