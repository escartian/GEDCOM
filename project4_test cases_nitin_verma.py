# Project 4, Test cases for User stories 8, 9, 10, 11 and 12 completed by Nitin Verma

import unittest
from io import StringIO
from datetime import datetime, timedelta

# Function to parse GEDCOM data from a string
def parse_gedcom_from_string(gedcom_data):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None
    date_tag = None

    lines = gedcom_data.strip().split('\n')
    for line in lines:
        parts = line.strip().split(' ', 2)
        if len(parts) < 2:
            continue
        
        level = parts[0]
        tag = parts[1]
        
        if level == '0':
            if tag.startswith('@I'):
                current_individual = tag
                individuals[current_individual] = {
                    'BIRT': None,
                    'DEAT': None,
                    'FAMS': [],
                    'FAMC': None
                }
            elif tag.startswith('@F'):
                current_family = tag
                families[current_family] = {
                    'HUSB': None,
                    'WIFE': None,
                    'CHIL': [],
                    'MARR': None,
                    'DIV': None
                }
            current_tag = None
        elif level == '1':
            current_tag = tag
            if current_tag in ['HUSB', 'WIFE', 'CHIL']:
                if current_tag == 'CHIL':
                    families[current_family][current_tag].append(parts[2])
                else:
                    families[current_family][current_tag] = parts[2]
            elif current_tag in ['BIRT', 'DEAT', 'MARR', 'DIV']:
                date_tag = current_tag
            else:
                current_tag = None
        elif level == '2' and tag == 'DATE' and current_tag:
            date_str = parts[2]
            date = datetime.strptime(date_str, "%d %b %Y")
            if current_individual and date_tag in ['BIRT', 'DEAT']:
                individuals[current_individual][date_tag] = date
            elif current_family and date_tag in ['MARR', 'DIV']:
                families[current_family][date_tag] = date

    return individuals, families

# Function to calculate age difference in years
def years_difference(date1, date2):
    return abs((date1 - date2).days) / 365.25

# Function to check constraints
def check_constraints(individuals, families):
    errors = []

    # Collect all marriages
    marriages = {}
    for fam_id, fam in families.items():
        marriage_date = fam['MARR']
        divorce_date = fam['DIV'] or datetime.max
        husband_id = fam['HUSB']
        wife_id = fam['WIFE']

        if marriage_date:
            if husband_id not in marriages:
                marriages[husband_id] = []
            marriages[husband_id].append((marriage_date, divorce_date, fam_id))

            if wife_id not in marriages:
                marriages[wife_id] = []
            marriages[wife_id].append((marriage_date, divorce_date, fam_id))

    # Check for overlapping marriages
    for ind_id, ind_marriages in marriages.items():
        ind_marriages.sort()
        for i in range(len(ind_marriages) - 1):
            if ind_marriages[i][1] > ind_marriages[i + 1][0]:
                errors.append(f"ERROR: FAMILY: Individual {ind_id} has overlapping marriages in families {ind_marriages[i][2]} and {ind_marriages[i + 1][2]}.")

    # Check other constraints
    for fam_id, fam in families.items():
        marriage_date = fam['MARR']
        divorce_date = fam['DIV']
        husband = individuals.get(fam['HUSB'])
        wife = individuals.get(fam['WIFE'])
        children = [individuals.get(child) for child in fam['CHIL']]

        # Check constraint 1: Children should be born after marriage of parents
        if marriage_date:
            for child in children:
                birth_date = child['BIRT']
                if birth_date and birth_date < marriage_date:
                    errors.append(f"ERROR: FAMILY: Child {child} born before marriage.")
                if divorce_date and birth_date and birth_date > divorce_date + timedelta(days=9*30):
                    errors.append(f"ERROR: FAMILY: Child {child} born more than 9 months after divorce.")

        # Check constraint 2: Child should be born before death of mother and before 9 months after death of father
        wife_death_date = wife['DEAT']
        husband_death_date = husband['DEAT']
        for child in children:
            birth_date = child['BIRT']
            if birth_date:
                if wife_death_date and birth_date > wife_death_date:
                    errors.append(f"ERROR: FAMILY: Child {child} born after death of mother.")
                if husband_death_date and birth_date > husband_death_date + timedelta(days=9*30):
                    errors.append(f"ERROR: FAMILY: Child {child} born more than 9 months after death of father.")

        # Check constraint 3: Marriage should be at least 14 years after birth of both spouses
        husband_birth_date = husband['BIRT']
        wife_birth_date = wife['BIRT']
        if marriage_date and husband_birth_date and wife_birth_date:
            if years_difference(marriage_date, husband_birth_date) < 14:
                errors.append(f"ERROR: FAMILY: Marriage of husband {fam['HUSB']} occurred before he was 14.")
            if years_difference(marriage_date, wife_birth_date) < 14:
                errors.append(f"ERROR: FAMILY: Marriage of wife {fam['WIFE']} occurred before she was 14.")

        # Check constraint 5: Parents' ages at child's birth
        for child in children:
            birth_date = child['BIRT']
            if birth_date:
                if husband_birth_date and years_difference(birth_date, husband_birth_date) > 80:
                    errors.append(f"ERROR: FAMILY: Father {fam['HUSB']} more than 80 years older than child {child}.")
                if wife_birth_date and years_difference(birth_date, wife_birth_date) > 60:
                    errors.append(f"ERROR: FAMILY: Mother {fam['WIFE']} more than 60 years older than child {child}.")

    return errors

class TestGedcomConstraints(unittest.TestCase):
    def test_child_before_marriage(self):
        gedcom_data = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 SEX M
        1 BIRT
        2 DATE 1 JAN 1980
        1 FAMS @F1@

        0 @I2@ INDI
        1 NAME Jane /Smith/
        1 SEX F
        1 BIRT
        2 DATE 1 JAN 1982
        1 FAMS @F1@

        0 @I3@ INDI
        1 NAME Child1 /Doe/
        1 SEX M
        1 BIRT
        2 DATE 1 JAN 1995
        1 FAMC @F1@

        0 @F1@ FAM
        1 HUSB @I1@
        1 WIFE @I2@
        1 CHIL @I3@
        1 MARR
        2 DATE 1 JAN 2000
        """
        individuals, families = parse_gedcom_from_string(gedcom_data)
        errors = check_constraints(individuals, families)
        self.assertIn("ERROR: FAMILY: Child {'BIRT': datetime.datetime(1995, 1, 1, 0, 0), 'DEAT': None, 'FAMS': [], 'FAMC': None} born before marriage.", errors)

    def test_child_after_divorce(self):
        gedcom_data = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 SEX M
        1 BIRT
        2 DATE 1 JAN 1980
        1 FAMS @F1@

        0 @I2@ INDI
        1 NAME Jane /Smith/
        1 SEX F
        1 BIRT
        2 DATE 1 JAN 1982
        1 FAMS @F1@

        0 @I3@ INDI
        1 NAME Child2 /Doe/
        1 SEX F
        1 BIRT
        2 DATE 1 OCT 2001
        1 FAMC @F1@

        0 @F1@ FAM
        1 HUSB @I1@
        1 WIFE @I2@
        1 CHIL @I3@
        1 MARR
        2 DATE 1 JAN 1999
        1 DIV
        2 DATE 1 JAN 2000
        """
        individuals, families = parse_gedcom_from_string(gedcom_data)
        errors = check_constraints(individuals, families)
        self.assertIn("ERROR: FAMILY: Child {'BIRT': datetime.datetime(2001, 10, 1, 0, 0), 'DEAT': None, 'FAMS': [], 'FAMC': None} born more than 9 months after divorce.", errors)

    def test_child_after_death_of_parents(self):
        gedcom_data = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 SEX M
        1 BIRT
        2 DATE 1 JAN 1980
        1 DEAT
        2 DATE 1 JAN 2020
        1 FAMS @F1@

        0 @I2@ INDI
        1 NAME Jane /Smith/
        1 SEX F
        1 BIRT
        2 DATE 1 JAN 1982
        1 DEAT
        2 DATE 1 JAN 2021
        1 FAMS @F1@

        0 @I3@ INDI
        1 NAME Child2 /Doe/
        1 SEX F
        1 BIRT
        2 DATE 1 OCT 2021
        1 FAMC @F1@

        0 @F1@ FAM
        1 HUSB @I1@
        1 WIFE @I2@
        1 CHIL @I3@
        1 MARR
        2 DATE 1 JAN 2000
        """
        individuals, families = parse_gedcom_from_string(gedcom_data)
        errors = check_constraints(individuals, families)
        self.assertIn("ERROR: FAMILY: Child {'BIRT': datetime.datetime(2021, 10, 1, 0, 0), 'DEAT': None, 'FAMS': [], 'FAMC': None} born after death of mother.", errors)
        self.assertIn("ERROR: FAMILY: Child {'BIRT': datetime.datetime(2021, 10, 1, 0, 0), 'DEAT': None, 'FAMS': [], 'FAMC': None} born more than 9 months after death of father.", errors)

    def test_marriage_before_14_years_old(self):
        gedcom_data = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 SEX M
        1 BIRT
        2 DATE 1 JAN 1980
        1 FAMS @F1@

        0 @I2@ INDI
        1 NAME Jane /Smith/
        1 SEX F
        1 BIRT
        2 DATE 1 JAN 1982
        1 FAMS @F1@

        0 @I3@ INDI
        1 NAME Child3 /Doe/
        1 SEX M
        1 BIRT
        2 DATE 1 JAN 2000
        1 FAMC @F1@

        0 @F1@ FAM
        1 HUSB @I1@
        1 WIFE @I2@
        1 CHIL @I3@
        1 MARR
        2 DATE 1 JAN 1993
        """
        individuals, families = parse_gedcom_from_string(gedcom_data)
        errors = check_constraints(individuals, families)
        self.assertIn("ERROR: FAMILY: Marriage of husband @I1@ occurred before he was 14.", errors)
        self.assertIn("ERROR: FAMILY: Marriage of wife @I2@ occurred before she was 14.", errors)

    def test_overlapping_marriages(self):
        gedcom_data = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 SEX M
        1 BIRT
        2 DATE 1 JAN 1980
        1 FAMS @F1@
        1 FAMS @F2@

        0 @I2@ INDI
        1 NAME Jane /Smith/
        1 SEX F
        1 BIRT
        2 DATE 1 JAN 1982
        1 FAMS @F1@

        0 @I3@ INDI
        1 NAME Spouse2 /Doe/
        1 SEX F
        1 BIRT
        2 DATE 1 JAN 1990
        1 FAMS @F2@

        0 @F1@ FAM
        1 HUSB @I1@
        1 WIFE @I2@
        1 MARR
        2 DATE 1 JAN 1999
        1 DIV
        2 DATE 1 JAN 2001

        0 @F2@ FAM
        1 HUSB @I1@
        1 WIFE @I3@
        1 MARR
        2 DATE 1 JAN 2000
        1 DIV
        2 DATE 1 JAN 2005
        """
        individuals, families = parse_gedcom_from_string(gedcom_data)
        errors = check_constraints(individuals, families)
        self.assertIn("ERROR: FAMILY: Individual @I1@ has overlapping marriages in families @F1@ and @F2@.", errors)

    def test_parents_too_old(self):
        gedcom_data = """
        0 @I1@ INDI
        1 NAME John /Doe/
        1 SEX M
        1 BIRT
        2 DATE 1 JAN 1900
        1 FAMS @F1@

        0 @I2@ INDI
        1 NAME Jane /Smith/
        1 SEX F
        1 BIRT
        2 DATE 1 JAN 1920
        1 FAMS @F1@

        0 @I3@ INDI
        1 NAME Child4 /Doe/
        1 SEX M
        1 BIRT
        2 DATE 1 JAN 2000
        1 FAMC @F1@

        0 @F1@ FAM
        1 HUSB @I1@
        1 WIFE @I2@
        1 CHIL @I3@
        1 MARR
        2 DATE 1 JAN 1990
        """
        individuals, families = parse_gedcom_from_string(gedcom_data)
        errors = check_constraints(individuals, families)
        self.assertIn("ERROR: FAMILY: Father @I1@ more than 80 years older than child {'BIRT': datetime.datetime(2000, 1, 1, 0, 0), 'DEAT': None, 'FAMS': [], 'FAMC': None}.", errors)
        self.assertIn("ERROR: FAMILY: Mother @I2@ more than 60 years older than child {'BIRT': datetime.datetime(2000, 1, 1, 0, 0), 'DEAT': None, 'FAMS': [], 'FAMC': None}.", errors)

if __name__ == "__main__":
    unittest.main()
