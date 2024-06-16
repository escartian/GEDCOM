import re
from datetime import datetime, timedelta

# Function to parse GEDCOM file
def parse_gedcom(file_path):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None
    date_tag = None

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split(' ', 2)
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
                errors.append(f"ERROR: FAMILY: US11: Individual {ind_id} has overlapping marriages in families {ind_marriages[i][2]} and {ind_marriages[i + 1][2]}.")

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
                    errors.append(f"ERROR: FAMILY: US08: Child {child} born before marriage.")
                if divorce_date and birth_date and birth_date > divorce_date and birth_date <= divorce_date + timedelta(days=9*30):
                    errors.append(f"ERROR: FAMILY: US08: Child {child} born more than 9 months after divorce.")

        # Check constraint 2: Child should be born before death of mother and before 9 months after death of father
        wife_death_date = wife['DEAT']
        husband_death_date = husband['DEAT']
        for child in children:
            birth_date = child['BIRT']
            if birth_date:
                if wife_death_date and birth_date > wife_death_date:
                    errors.append(f"ERROR: FAMILY: US09: Child {child} born after death of mother.")
                if husband_death_date and birth_date > husband_death_date + timedelta(days=9*30):
                    errors.append(f"ERROR: FAMILY: US09: Child {child} born more than 9 months after death of father.")

        # Check constraint 3: Marriage should be at least 14 years after birth of both spouses
        husband_birth_date = husband['BIRT']
        wife_birth_date = wife['BIRT']
        if marriage_date and husband_birth_date and wife_birth_date:
            if years_difference(marriage_date, husband_birth_date) < 14:
                errors.append(f"ERROR: FAMILY: US10: Marriage of husband {fam['HUSB']} occurred before he was 14.")
            if years_difference(marriage_date, wife_birth_date) < 14:
                errors.append(f"ERROR: FAMILY: US10: Marriage of wife {fam['WIFE']} occurred before she was 14.")

        # Check constraint 5: Parents' ages at child's birth
        for child in children:
            birth_date = child['BIRT']
            if birth_date:
                if husband_birth_date and years_difference(birth_date, husband_birth_date) > 80:
                    errors.append(f"ERROR: FAMILY: US12: Father {fam['HUSB']} more than 80 years older than child {child}.")
                if wife_birth_date and years_difference(birth_date, wife_birth_date) > 60:
                    errors.append(f"ERROR: FAMILY: US12: Mother {fam['WIFE']} more than 60 years older than child {child}.")

    return errors

# Path to the GED file (update the path as necessary)
ged_file_path = "My-Family-23-May-2024-145749432_test.ged"

# Read individuals and families from GED file
individuals, families = parse_gedcom(ged_file_path)

# Check constraints
errors = check_constraints(individuals, families)

# Print errors
for error in errors:
    print(error)