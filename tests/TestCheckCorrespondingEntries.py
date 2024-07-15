import unittest
from GedcomDataReader import check_corresponding_entries

class TestCheckCorrespondingEntries(unittest.TestCase):
    
    def test_many_issues(self):
        self.maxDiff = None 
        individuals = {
            '1': {'FAMS': ['1']},
            '2': {'FAMC': ['1']},
            '3': {'FAMS': ['1'], 'FAMC': ['1']}
        }
        families = {
            '1': {'HUSB': '2', 'WIFE': '3', 'CHIL': ['1', '2']}
        }
        errors = check_corresponding_entries(individuals, families)
        self.assertEqual(errors, ['Checking Corresponding Entries: ERROR:  Individual 1 is listed as a spouse in family 1 but is not recorded as HUSB or WIFE', 'Checking Corresponding Entries: ERROR:  Individual 3 is listed as a child in family 1 but is not recorded as CHIL', 'Checking Corresponding Entries: ERROR:  Husband 2 in family 1 does not list 1 in FAMS', 'Checking Corresponding Entries: ERROR: FAMILY: Child 1 in family 1 does not list 1 in FAMC'])

    def test_individual_with_non_existent_family(self):
        self.maxDiff = None 
        individuals = {
            '1': {'FAMS': ['2']}
        }
        families = {}
        errors = check_corresponding_entries(individuals, families)
        self.assertEqual(errors, ['Checking Corresponding Entries: ERROR: Individual 1 has a FAMS link to non-existent family 2'])

    def test_individual_not_listed_as_spouse(self):
        self.maxDiff = None 
        individuals = {
            '1': {'FAMS': ['1']},
            '2': {'FAMC': ['1']}
        }
        families = {
            '1': {'HUSB': '2', 'WIFE': '3'}
        }
        errors = check_corresponding_entries(individuals, families)
        self.assertEqual(errors, ['Checking Corresponding Entries: ERROR:  Individual 1 is listed as a spouse in family 1 but is not recorded as HUSB or WIFE', 'Checking Corresponding Entries: ERROR:  Individual 2 is listed as a child in family 1 but is not recorded as CHIL'])

    def test_individual_not_listed_as_child(self):
        self.maxDiff = None 
        individuals = {
            '1': {'FAMC': ['1']}
        }
        families = {
            '1': {'CHIL': ['2']}
        }
        errors = check_corresponding_entries(individuals, families)
        self.assertEqual(errors, ['Checking Corresponding Entries: ERROR:  Individual 1 is listed as a child in family 1 but is not recorded as CHIL', 'Checking Corresponding Entries: ERROR: FAMILY: Child 2 in family 1 does not list 1 in FAMC'])

    def test_husband_not_listed_in_family(self):
        self.maxDiff = None 
        individuals = {
            '1': {'FAMS': ['1']},
            '2': {'FAMC': ['1']}
        }
        families = {
            '1': {'HUSB': '3', 'WIFE': '2', 'CHIL': ['1']}
        }
        errors = check_corresponding_entries(individuals, families)
        self.assertEqual(errors, ['Checking Corresponding Entries: ERROR:  Individual 1 is listed as a spouse in family 1 but is not recorded as HUSB or WIFE', 'Checking Corresponding Entries: ERROR:  Individual 2 is listed as a child in family 1 but is not recorded as CHIL'])

    def test_wife_not_listed_in_family(self):
        self.maxDiff = None 
        individuals = {
            '1': {'FAMS': ['1']},
            '2': {'FAMC': ['1']}
        }
        families = {
            '1': {'HUSB': '2', 'WIFE': '3', 'CHIL': ['1']}
        }
        errors = check_corresponding_entries(individuals, families)
        self.assertEqual(errors, ['Checking Corresponding Entries: ERROR:  Individual 1 is listed as a spouse in family 1 but is not recorded as HUSB or WIFE', 'Checking Corresponding Entries: ERROR:  Individual 2 is listed as a child in family 1 but is not recorded as CHIL'])

    def test_child_not_listed_in_family(self):
        self.maxDiff = None 
        individuals = {
            '1': {'FAMC': ['1']}
        }
        families = {
            '1': {'CHIL': ['2']}
        }
        errors = check_corresponding_entries(individuals, families)
        print(errors)
        self.assertEqual(errors, ['Checking Corresponding Entries: ERROR:  Individual 1 is listed as a child in family 1 but is not recorded as CHIL', 'Checking Corresponding Entries: ERROR: FAMILY: Child 2 in family 1 does not list 1 in FAMC'])

if __name__ == '__main__':
    unittest.main()