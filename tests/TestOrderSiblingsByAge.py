import unittest
from GedcomDataReader import order_siblings_by_age

class TestOrderSiblingsByAge(unittest.TestCase):
    def test_empty_input(self):
        individuals = {}
        families = {}
        result = order_siblings_by_age(individuals, families)
        self.assertEqual(result, {})

    def test_single_family_with_no_children(self):
        individuals = {}
        families = {
            'F1': {'Children': []}
        }
        result = order_siblings_by_age(individuals, families)
        self.assertEqual(result, {'F1': []})

    def test_single_family_with_one_child(self):
        individuals = {
            'C1': {'birth': '1990-01-01'}
        }
        families = {
            'F1': {'Children': ['C1']}
        }
        result = order_siblings_by_age(individuals, families)
        self.assertEqual(result, {'F1': [{'birth': '1990-01-01'}]})

    def test_single_family_with_multiple_children(self):
        individuals = {
            'C1': {'birth': '1990-01-01'},
            'C2': {'birth': '1980-01-01'},
            'C3': {'birth': '1995-01-01'}
        }
        families = {
            'F1': {'Children': ['C1', 'C2', 'C3']}
        }
        result = order_siblings_by_age(individuals, families)
        self.assertEqual(result, {'F1': [{'birth': '1980-01-01'}, {'birth': '1990-01-01'}, {'birth': '1995-01-01'}]})

    def test_multiple_families(self):
        individuals = {
            'C1': {'birth': '1990-01-01'},
            'C2': {'birth': '1980-01-01'},
            'C3': {'birth': '1995-02-01'},
            'C4': {'birth': '1985-02-01'},
            'C5': {'birth': '1988-01-01'}
        }
        families = {
            'F1': {'Children': ['C1', 'C2']},
            'F2': {'Children': ['C3', 'C4', 'C5']}
        }
        result = order_siblings_by_age(individuals, families)
        expected_result = {'F1': [{'birth': '1980-01-01'}, {'birth': '1990-01-01'}], 
                           'F2': [{'birth': '1985-02-01'}, {'birth': '1988-01-01'}, {'birth': '1995-02-01'}]}
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()