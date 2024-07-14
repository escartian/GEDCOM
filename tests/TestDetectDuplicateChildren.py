import unittest
from DuplicateCheckers import detect_duplicate_children

class TestDetectDuplicateChildren(unittest.TestCase):
    def setUp(self):
        """Set up test data."""
        self.individuals = {'I1': {'name': 'Joeseph/Summers/', 'sex': 'M', 'birth': '1920-08-30', 'death': '2000-12-04'},
        'I3': {'name': 'Joylene/Summers/', 'sex': 'F', 'birth': '1960-03-02', 'death': 'Unknown'},
        'I5': {'name': 'Lodi/Trecker/', 'sex': 'F', 'birth': '1930-05-26', 'death': '2014-08-19'},
        'I6': {'name': 'Marco/Summers/', 'sex': 'M', 'birth': '1969-11-15', 'death': 'Unknown'},
        'I7': {'name': 'Julia/Fredrickson/', 'sex': 'F', 'birth': '2000-06-20', 'death': '2023-09-22'},
        'I8': {'name': 'Alexa/Smith/', 'sex': 'F', 'birth': '2020-02-08', 'death': 'Unknown'},
        'I9': {'name': 'Franck/Shumaker/', 'sex': 'M', 'birth': '1976-02-16', 'death': 'Unknown'}, 
        'I10': {'name': 'Samantha/Holden/', 'sex': 'F', 'birth': '1980-07-17', 'death': 'Unknown'}, 
        'I11': {'name': 'Mary/Apples/', 'sex': 'F', 'birth': '1970-11-26', 'death': 'Unknown'},
        'I12': {'name': 'Andrew/Summers/', 'sex': 'M', 'birth': '1995-01-24', 'death': 'Unknown'},
        'I13': {'name': 'Fred/Goldsmith/', 'sex': 'M', 'birth': '1967-09-17', 'death': 'Unknown'}, 
        'I14': {'name': 'Fransica/Goldsmith/', 'sex': 'F', 'birth': '1990-02-04', 'death': 'Unknown'},
        'I15': {'name': 'Tyler/Frups/', 'sex': 'M', 'birth': '2004-02-02', 'death': 'Unknown'}, 
        'I16': {'name': 'Warren/Goldsmith/', 'sex': 'M', 'birth': '1990-02-04', 'death': 'Unknown'}}

        self.families =[{'ID': 'F1', 'Children': ['I8'], 'Married': '2019-03-03', 'Divorced': [], 'Husband ID': 'I1', 'Husband Name': 'Joeseph/Summers/', 'Wife ID': 'I7', 'Wife Name': 'Julia/Fredrickson/'}, 
        {'ID': 'F2', 'Children': ['I1'], 'Married': '1987-07-04', 'Divorced': [], 'Husband ID': 'I2', 'Husband Name': 'Unknown', 'Wife ID': 'I3', 'Wife Name': 'Joylene/Summers/'}, 
        {'ID': 'F3', 'Children': ['I3', 'I6'], 'Married': '1946-04-21', 'Divorced': [], 'Husband ID': 'I4', 'Husband Name': 'Unknown', 'Wife ID': 'I5', 'Wife Name': 'Lodi/Trecker/'},
        {'ID': 'F4', 'Children': ['I10'], 'Married': '1997-01-03', 'Divorced': [], 'Husband ID': 'I9', 'Husband Name': 'Franck/Shumaker/', 'Wife ID': 'I6', 'Wife Name': 'Marco/Summers/'}, 
        {'ID': 'F5', 'Children': ['I12'], 'Married': '1990-02-05', 'Divorced': '1996-08-13', 'Husband ID': 'I6', 'Husband Name': 'Marco/Summers/', 'Wife ID': 'I11', 'Wife Name': 'Mary/Apples/'}, 
        {'ID': 'F6', 'Children': [], 'Married': '2022-04-03', 'Divorced': [], 'Husband ID': 'I15', 'Husband Name': 'Tyler/Frups/', 'Wife ID': 'I10', 'Wife Name': 'Samantha/Holden/'}, 
        {'ID': 'F7', 'Children': ['I14', 'I16'], 'Married': '1998-05-04', 'Divorced': [], 'Husband ID': 'I13', 'Husband Name': 'Fred/Goldsmith/', 'Wife ID': 'I11', 'Wife Name': 'Mary/Apples/'}]

        self.families_with_duplicates=[{'ID': 'F1', 'Children': ['I8'], 'Married': '2019-03-03', 'Divorced': [], 'Husband ID': 'I1', 'Husband Name': 'Joeseph/Summers/', 'Wife ID': 'I7', 'Wife Name': 'Julia/Fredrickson/'}, 
        {'ID': 'F2', 'Children': ['I1'], 'Married': '1987-07-04', 'Divorced': [], 'Husband ID': 'I2', 'Husband Name': 'Unknown', 'Wife ID': 'I3', 'Wife Name': 'Joylene/Summers/'}, 
        {'ID': 'F3', 'Children': ['I3', 'I6'], 'Married': '1946-04-21', 'Divorced': [], 'Husband ID': 'I4', 'Husband Name': 'Unknown', 'Wife ID': 'I5', 'Wife Name': 'Lodi/Trecker/'},
        {'ID': 'F4', 'Children': ['I10'], 'Married': '1997-01-03', 'Divorced': [], 'Husband ID': 'I9', 'Husband Name': 'Franck/Shumaker/', 'Wife ID': 'I6', 'Wife Name': 'Marco/Summers/'}, 
        {'ID': 'F2', 'Children': ['I1'], 'Married': '1987-07-04', 'Divorced': [], 'Husband ID': 'I2', 'Husband Name': 'Unknown', 'Wife ID': 'I3', 'Wife Name': 'Joylene/Summers/'}, 
        {'ID': 'F3', 'Children': ['I3', 'I6'], 'Married': '1946-04-21', 'Divorced': [], 'Husband ID': 'I4', 'Husband Name': 'Unknown', 'Wife ID': 'I5', 'Wife Name': 'Lodi/Trecker/'},
        {'ID': 'F7', 'Children': ['I14', 'I16'], 'Married': '1998-05-04', 'Divorced': [], 'Husband ID': 'I13', 'Husband Name': 'Fred/Goldsmith/', 'Wife ID': 'I11', 'Wife Name': 'Mary/Apples/'}]

        self.individuals_with_duplicates = {'I1': {'name': 'Joeseph/Summers/', 'sex': 'M', 'birth': '1920-08-30', 'death': '2000-12-04'},
        'I3': {'name': 'Joylene/Summers/', 'sex': 'F', 'birth': '1960-03-02', 'death': 'Unknown'},
        'I5': {'name': 'Lodi/Trecker/', 'sex': 'F', 'birth': '1930-05-26', 'death': '2014-08-19'},
        'I6': {'name': 'Marco/Summers/', 'sex': 'M', 'birth': '1969-11-15', 'death': 'Unknown'},
        'I1': {'name': 'Joeseph/Summers/', 'sex': 'M', 'birth': '1920-08-30', 'death': '2000-12-04'},
        'I3': {'name': 'Joylene/Summers/', 'sex': 'F', 'birth': '1960-03-02', 'death': 'Unknown'},
        'I5': {'name': 'Lodi/Trecker/', 'sex': 'F', 'birth': '1930-05-26', 'death': '2014-08-19'},
        'I6': {'name': 'Marco/Summers/', 'sex': 'M', 'birth': '1969-11-15', 'death': 'Unknown'},'I11': {'name': 'Mary/Apples/', 'sex': 'F', 'birth': '1970-11-26', 'death': 'Unknown'},
        'I12': {'name': 'Andrew/Summers/', 'sex': 'M', 'birth': '1995-01-24', 'death': 'Unknown'},
        'I13': {'name': 'Fred/Goldsmith/', 'sex': 'M', 'birth': '1967-09-17', 'death': 'Unknown'}, 
        'I14': {'name': 'Fransica/Goldsmith/', 'sex': 'F', 'birth': '1990-02-04', 'death': 'Unknown'},
        'I15': {'name': 'Tyler/Frups/', 'sex': 'M', 'birth': '2004-02-02', 'death': 'Unknown'}, 
        'I16': {'name': 'Warren/Goldsmith/', 'sex': 'M', 'birth': '1990-02-04', 'death': 'Unknown'}}
    def test_no_duplicates(self):

        self.assertEqual(detect_duplicate_children(self.individuals, self.families), [])

    def test_duplicates_family(self):
        self.assertEqual(detect_duplicate_children(self.individuals, self.families_with_duplicates), ['I1', 'I3', 'I6'])

    def test_with_duplicates_family_and_individuals(self):
        self.assertEqual(detect_duplicate_children(self.individuals_with_duplicates, self.families_with_duplicates), ['I1', 'I3', 'I6'])

if __name__ == '__main__':
    unittest.main()