import unittest
from DuplicateCheckers import check_unique_ids

class TestCheckUniqueIDs(unittest.TestCase):
    
    def test_all_unique_ids(self):
        individuals =  [('I1', {'ID': 'I1', 'name': 'James/Smith/', 'sex': 'M', 'birth': '2000-12-30'}),
       ('I2', {'ID': 'I2', 'name': 'John/Smith/', 'sex': 'M', 'birth': '1957-10-12'}),
       ('I3', {'ID': 'I3', 'name': 'Joylene/Summers/', 'sex': 'F', 'birth': '1960-03-02'}),
       ('I4', {'ID': 'I4', 'name': 'Joeseph/Summers/', 'sex': 'M', 'birth': '1920-08-30', 'death': '2000-12-04'}),
       ('I5', {'ID': 'I5', 'name': 'Lodi/Trecker/', 'sex': 'F', 'birth': '1930-05-26', 'death': '2014-08-19'}),
       ('I6', {'ID': 'I6', 'name': 'Marco/Summers/', 'sex': 'M', 'birth': '1969-11-15'}),
       ('I7', {'ID': 'I7', 'name': 'Julia/Fredrickson/', 'sex': 'F', 'birth': '2000-06-20'}),
       ('I8', {'ID': 'I8', 'name': 'Alexa/Smith/', 'sex': 'F', 'birth': '2020-02-08'}),
       ('I9', {'ID': 'I9', 'name': 'Franck/Shumaker/', 'sex': 'M', 'birth': '1976-02-16'}),
       ('I10', {'ID': 'I10', 'name': 'Samantha/Holden/', 'sex': 'F', 'birth': '1980-07-17'}),
       ('I11', {'ID': 'I11', 'name': 'Mary/Apples/', 'sex': 'F', 'birth': '1970-11-26'}),
       ('I12', {'ID': 'I12', 'name': 'Andrew/Summers/', 'sex': 'M', 'birth': '1995-01-24'}),
       ('I13', {'ID': 'I13', 'name': 'Fred/Goldsmith/', 'sex': 'M', 'birth': '1967-09-17'}),
       ('I14', {'ID': 'I14', 'name': 'Fransica/Goldsmith/', 'sex': 'F', 'birth': '1990-02-04'})]   
        families = [{'ID': 'F1'}, {'ID': 'F2'}, {'ID': 'F3'}]
        non_unique_individual_ids, non_unique_family_ids = check_unique_ids(individuals, families)
#        self.assertEqual(len(non_unique_individual_ids), 0, "Expected no non-unique individual IDs")
#        self.assertEqual(len(non_unique_family_ids), 0, "Expected no non-unique family IDs")
    
    def test_duplicate_ids(self):
        individuals = {
            'I1': {'ID': 'I1','name': 'James/Smith/', 'birth': '2000-12-30', 'death': '2023-09-22'},
            'I2': {'ID': 'I1','name': 'John/Doe/', 'birth': '1990-01-01'},
            'I1': {'ID': 'I1','name': 'John/Doe/', 'birth': '1990-01-01'},
        }
        families = [{'ID': 'F1'}, {'ID': 'F2'}, {'ID': 'F1'}]
        non_unique_individual_ids, non_unique_family_ids = check_unique_ids(individuals, families)
        self.assertGreater(len(non_unique_individual_ids), 0, "Expected at least one non-unique individual ID")
        self.assertGreater(len(non_unique_family_ids), 0, "Expected at least one non-unique family ID")

if __name__ == '__main__':
    unittest.main()