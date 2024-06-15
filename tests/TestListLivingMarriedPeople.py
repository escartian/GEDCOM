import unittest
from Constants import logger
from ListLivingMarriedPeople import list_living_married_people

class TestListLivingMarriedPeople(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.individuals = [('I1', {'ID': 'I1', 'name': 'James/Smith/', 'sex': 'M', 'birth': '2000-12-30'}),
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


        self.families = [
            {'ID': 'F1', 'Children': ['I8'], 'Married': '2019-03-03', 'Divorced': [], 'Husband ID': 'I1', 'Husband Name': 'James/Smith/', 'Wife ID': 'I7', 'Wife Name': 'Julia/Fredrickson/'}, 
             {'ID': 'F2', 'Children': ['I1'], 'Married': '1987-07-04', 'Divorced': [], 'Husband ID': 'I2', 'Husband Name': 'John/Smith/', 'Wife ID': 'I3', 'Wife Name': 'Joylene/Summers/'}, 
             {'ID': 'F3', 'Children': ['I3', 'I6'], 'Married': '1946-04-21', 'Divorced': [], 'Husband ID': 'I4', 'Husband Name': 'Joeseph/Summers/', 'Wife ID': 'I5', 'Wife Name': 'Lodi/Trecker/'},
             {'ID': 'F4', 'Children': ['I10'], 'Married': '1997-01-03', 'Divorced': [], 'Husband ID': 'I9', 'Husband Name': 'Franck/Shumaker/', 'Wife ID': 'I6', 'Wife Name': 'Marco/Summers/'}, 
             {'ID': 'F5', 'Children': ['I12'], 'Married': '1990-02-05', 'Divorced': '1996-08-13', 'Husband ID': 'I6', 'Husband Name': 'Marco/Summers/', 'Wife ID': 'I11', 'Wife Name': 'Mary/Apples/'},
             {'ID': 'F6', 'Children': ['I14'], 'Married': '1998-05-04', 'Divorced': [], 'Husband ID': 'I13', 'Husband Name': 'Fred/Goldsmith/', 'Wife ID': 'I11', 'Wife Name': 'Mary/Apples/'}
            
        ]
    def test_full_list(self):
        expected_output = [
        {'ID': 'I1', 'Details': {'ID': 'I1', 'name': 'James/Smith/', 'sex': 'M', 'birth': '2000-12-30'}, 'Spouse_ID': 'I7'},
        {'ID': 'I7', 'Details': {'ID': 'I7', 'name': 'Julia/Fredrickson/', 'sex': 'F', 'birth': '2000-06-20'}, 'Spouse_ID': 'I1'},
        {'ID': 'I2', 'Details': {'ID': 'I2', 'name': 'John/Smith/', 'sex': 'M', 'birth': '1957-10-12'}, 'Spouse_ID': 'I3'},
        {'ID': 'I3', 'Details': {'ID': 'I3', 'name': 'Joylene/Summers/', 'sex': 'F', 'birth': '1960-03-02'}, 'Spouse_ID': 'I2'},
        {'ID': 'I9', 'Details': {'ID': 'I9', 'name': 'Franck/Shumaker/', 'sex': 'M', 'birth': '1976-02-16'}, 'Spouse_ID': 'I6'},
        {'ID': 'I6', 'Details': {'ID': 'I6', 'name': 'Marco/Summers/', 'sex': 'M', 'birth': '1969-11-15'}, 'Spouse_ID': 'I9'},
        {'ID': 'I13', 'Details': {'ID': 'I13', 'name': 'Fred/Goldsmith/', 'sex': 'M', 'birth': '1967-09-17'}, 'Spouse_ID': 'I11'},
        {'ID': 'I11', 'Details': {'ID': 'I11', 'name': 'Mary/Apples/', 'sex': 'F', 'birth': '1970-11-26'}, 'Spouse_ID': 'I13'}
        ]
        result = list_living_married_people(self.individuals, self.families)
        if logger:
            print("test_empty_list returned - ", result)
        self.assertEqual(result, expected_output)
    
    def test_empty_list(self):
        self.individuals = []
        self.families = []
        expected_output = []
        result = list_living_married_people(self.individuals, self.families)
        if logger:    
            print("test_empty_list returned - ", result)
        self.assertEqual(result, expected_output)

    def test_no_families(self):
        self.families = []
        expected_output = []
        result = list_living_married_people(self.individuals, self.families)
        if logger:    
            print("test_no_families returned - ", result)
        self.assertEqual(result, expected_output)

    def test_no_individuals(self):
        self.individuals = []
        expected_output = []
        if logger:    
            print("test_no_individuals families - ", self.families)
        result = list_living_married_people(self.individuals, self.families)
        if logger:    
            print("test_no_individuals returned - ", result)
        self.assertEqual(result, expected_output)

    def test_family_of_two(self):
        self.maxDiff = None
        self.individuals = [ ('I6', {'ID': 'I6', 'name': 'Marco/Summers/', 'sex': 'M', 'birth': '1969-11-15'}),
                             ('I9', {'ID': 'I9', 'name': 'Franck/Shumaker/', 'sex': 'M', 'birth': '1976-02-16'})           
                           ]
        expected_output = [{'ID': 'I9', 'Details': {'ID': 'I9', 'name': 'Franck/Shumaker/', 'sex': 'M', 'birth': '1976-02-16'}, 'Spouse_ID': 'I6'},
                            {'ID': 'I6', 'Details': {'ID': 'I6', 'name': 'Marco/Summers/', 'sex': 'M', 'birth': '1969-11-15'}, 'Spouse_ID': 'I9'}]
        result = list_living_married_people(self.individuals, self.families)
        if logger:    
            print("test_family_of_two returned - ", result)
        self.assertEqual(result, expected_output)
        
if __name__ == '__main__':
    unittest.main()
