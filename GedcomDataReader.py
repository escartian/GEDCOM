import re
from collections import defaultdict
from prettytable import PrettyTable
from ListLivingMarriedPeople import list_living_married_people
from Lists import *
from Constants import *
from datetime import datetime, timedelta

def dates_before_current_date(gedcom_lines):
    current_date = datetime.now()
    events = ["BIRT", "MARR", "DIV", "DEAT"]
    invalid_dates = []

    #iterate through gedcom lines
    for i, line in enumerate(gedcom_lines):
        parts = line.strip().split()
        #checking that the event is in the events array
        if (parts and parts[0] in ["1", "2"] and parts[1] in events):
            date_line = gedcom_lines[i + 1].strip()
            date_parts = date_line.split()
            if (date_parts[0] == "2" and date_parts[1] == "DATE"):
                try:
                    event_date = datetime.strptime(" ".join(date_parts[2:]), "%d %b %Y")
                    # if event date is after current data 
                    if (event_date > current_date):
                        invalid_dates.append((line, date_line))
                except ValueError:
                    continue

    #print (invalid_dates)
    return invalid_dates

def birth_before_marriage(gedcom_lines):
    individuals = {}
    current_id = None
    birth_date = None
    marriage_date = None


    for i, line in enumerate(gedcom_lines):
        parts = line.strip().split()
        if parts:
            if parts[0] == "0" and "@I" in parts[1]:
                if current_id and birth_date and marriage_date:
                    individuals[current_id] = (birth_date, marriage_date)

                current_id = parts[1]
                birth_date = None
                marriage_date = None
            elif parts[0] == "1":
                if parts[1] == "BIRT":
                    date_line = gedcom_lines[i + 1].strip()
                    date_parts = date_line.split()
                    if date_parts[0] == "2" and date_parts[1] == "DATE":
                        try:
                            birth_date = datetime.strptime(" ".join(date_parts[2:]), "%d %b %Y")
                        except ValueError:
                            birth_date = None
                elif parts[1] == "MARR":
                    date_line = gedcom_lines[i + 1].strip()
                    date_parts = date_line.split()
                    if date_parts[0] == "2" and date_parts[1] == "DATE":
                        try:
                            marriage_date = datetime.strptime(" ".join(date_parts[2:]), "%d %b %Y")
                        except ValueError:
                            marriage_date = None

    # Add the last individual's dates
    if current_id and birth_date and marriage_date:
        individuals[current_id] = (birth_date, marriage_date)

    #print(individuals)

    results = {}
    for ind_id, (b_date, m_date) in individuals.items():
        results[ind_id] = b_date < m_date if b_date and m_date else None
    #print(results)
    return results

def birth_before_death(gedcom_lines):
    individuals = {}
    current_id = None
    birth_date = None
    death_date = None

    for i, line in enumerate(gedcom_lines):
        parts = line.strip().split()
        if parts:
            if parts[0] == "0" and "@I" in parts[1]:
                if current_id and birth_date and death_date:
                    individuals[current_id] = (birth_date, death_date)

                current_id = parts[1]
                birth_date = None
                death_date = None
            elif parts[0] == "1":
                if parts[1] == "BIRT":
                    date_line = gedcom_lines[i + 1].strip()
                    date_parts = date_line.split()
                    if date_parts[0] == "2" and date_parts[1] == "DATE":
                        try:
                            birth_date = datetime.strptime(" ".join(date_parts[2:]), "%d %b %Y")
                        except ValueError:
                            birth_date = None
                elif parts[1] == "DEAT":
                    date_line = gedcom_lines[i + 1].strip()
                    date_parts = date_line.split()
                    if date_parts[0] == "2" and date_parts[1] == "DATE":
                        try:
                            death_date = datetime.strptime(" ".join(date_parts[2:]), "%d %b %Y")
                        except ValueError:
                            death_date = None

    # Add the last individual's dates
    if current_id and birth_date and death_date:
        individuals[current_id] = (birth_date, death_date)

    #print(individuals)

    results = {}
    for ind_id, (b_date, m_date) in individuals.items():
        results[ind_id] = b_date < m_date if b_date and m_date else None
        print(results)
    
    return results

def process_gedcom_line(line):
    tokens = line.split()
    if verbouseLogger:
        print("process_gedcom_line:line was split into tokens")
    level, tag, *arguments = tokens
    if verbouseLogger:
        print("process_gedcom_line: tokens are: ", tokens)
        print("process_gedcom_line: level: ", level, "tag: ", tag, "arguments: ", arguments)    
    is_indi_or_fam = False
    # Check if the tag is valid
    is_valid = 'Y' if tag in valid_tags else 'N'

    # Additional check for unsupported tags
    if (level == '1' and tag == 'DATE') or (level == '2' and tag == 'NAME'):
        is_valid = 'N'
        if verbouseLogger:
            print("process_gedcom_line: INVALID DATE or NAME detected")
        
    if any(arg in {'INDI', 'FAM'} for arg in arguments):
        is_valid = 'Y'
        is_indi_or_fam = True 
        if verbouseLogger:
            print("process_gedcom_line: INDI/FAM flipping tag and arguments")
        # Flip tag and arguments if the argument is 'INDI' or 'FAM'
        if arguments and arguments[0] in {'INDI', 'FAM'}:
            *arguments, tag = tag, *arguments
        # tag = arguments.pop(0)  # Remove 'INDI' or 'FAM' from arguments and assign to tag

    # Extract the data from the arguments (as it's a list)
    if verbouseLogger:
        print("process_gedcom_line: Arguments before removing leading and trailing @ symbol: ", arguments)
    if arguments and arguments[0].startswith("@") and arguments[-1].endswith("@"):
        arguments = arguments[0][1:-1]  # Remove the "@" symbols
        if verbouseLogger:
            print("process_gedcom_line: Arguments after removing leading and trailing @ symbol: ", arguments)

    # Construct the output strings
    if is_indi_or_fam:
        if verbouseLogger:
            print("process_gedcom_line: Processing output for an INDI or FAM")
        id_part = arguments
        processed_line = f"{level}|{tag}|{id_part}"
    else:
        if tag == 'DATE' and is_valid=='Y':
            if verbouseLogger:
                print("process_gedcom_line: Processing output for a DATE")
            processed_line = f"{level}|{tag}|{parse_date(' '.join(arguments))}"
        else:
            processed_line = f"{level}|{tag}|{''.join(arguments).strip()}"
    if verbouseLogger:
        print("process_gedcom_line: returning ", processed_line, is_valid)

    # Return the processed line and is_valid flag
    return processed_line, is_valid

def calculate_age(birth_date):
    today = datetime.today()
    birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def parse_date(date_string):
    """
    Parse a date string from GEDCOM format (e.g., "2 DATE 2 MAR 1960") and return a formatted date string.
    """
    if verbouseLogger:
        print("parse_date DATE: " + date_string)
    # Example date_string: "2 DATE 2 MAR 1960"
    # Splitting by space gives: ['2', 'DATE', '2', 'MAR', '1960']
    parts = date_string.split()
    if verbouseLogger:
        print("parse_date DATE PARTS: " + str(parts))
    # The year is in the last part of the split string
    year = int(parts[-1])
    
    # The day and month are in the second and third parts
    day = int(parts[0])
    month = parts[1].upper()  # Convert to uppercase
    
    # Mapping month abbreviations to numbers
    month_to_number = {
        "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4,
        "MAY": 5, "JUN": 6, "JUL": 7, "AUG": 8,
        "SEP": 9, "OCT": 10, "NOV": 11, "DEC": 12
    }
    
    # Validate and convert month
    if month not in month_to_number:
        raise ValueError("parse_date Invalid month in date string")
    month_number = month_to_number[month]
    
    # Return formatted date string
    return f"{year}-{month_number:02d}-{day:02d}"
def create_family_from_lines(data, individuals_dict):
    families = []
    current_family = None
    expecting_marriage_date = False
    expecting_divorce_date = False
    
    for line in data:
        tokens = line.split('|')
        #if len(tokens) < 2:
        #    continue
        
        level = tokens[0]
        tag = tokens[1]
        value = " ".join(tokens[2:])
        
        if logger:
            print("create_family_from_lines: level: " + level + " tag: " + tag + " value: " + value)

        if tag == "FAM":
            if current_family:
                families.append(current_family)
            current_family = {
                'ID': value,
                'Children': [],
                'Married': [],  # Initialize with empty string
                'Divorced': []  # Initialize with empty string
            }
        elif tag == "HUSB":
            current_family['Husband ID'] = value
            current_family['Husband Name'] = individuals_dict.get(value, {}).get('name', 'Unknown')
        elif tag == "WIFE":
            current_family['Wife ID'] = value
            current_family['Wife Name'] = individuals_dict.get(value, {}).get('name', 'Unknown')
        elif tag == "CHIL":
            # Append child ID to the Children list
            current_family['Children'].append(value)
        elif tag == "MARR":
            expecting_marriage_date = True
            continue  # Skip to next iteration to capture the date
        elif tag == "DIV":
            expecting_divorce_date = True
            continue  # Skip to next iteration to capture the date
        elif tag == "DATE":
            if expecting_marriage_date:
                current_family['Married'] = value
                if verbouseLogger:
                    print("Married date value is now:", current_family['Married'])
                expecting_marriage_date = False
            elif expecting_divorce_date:
                current_family['Divorced'] = value
                expecting_divorce_date = False
        else:
            # Reset flags if neither marriage nor divorce date is expected
            expecting_marriage_date = False
            expecting_divorce_date = False
    
    if current_family:
        families.append(current_family)
    
    return families
def create_individual_from_lines(lines):
    individuals = {}
    current_indi_id = None
    current_data = {}
    capturing_birthday = False
    capturing_death = False
    if logger:
        print("Starting individuals processing")

    for line in lines:
        tokens = line.split('|')
        level, tag, *arguments = tokens

        if level == '0' and tag == 'INDI':
            if logger:
                print("Starting new individual record")
            if current_indi_id is not None:
                individuals[current_indi_id] = current_data.copy()
            current_indi_id = arguments[0]
            current_data = {'ID': current_indi_id}
            continue

        if level == '1' and tag == 'NAME':
            current_data['name'] = ' '.join(arguments)
            continue

        if level == '1' and tag == 'SEX':
            current_data['sex'] = arguments[0]
            continue

        if level == '0' and current_indi_id is not None:
            individuals[current_indi_id] = current_data.copy()
            current_indi_id = None
            current_data = {}

        if tag == 'BIRT':
            capturing_birthday = True
            continue

        if capturing_birthday and tag == 'DATE':
            current_data['birth'] = ' '.join(arguments)
            capturing_birthday = False
            continue

        if tag == 'DEAT':
            capturing_death = True
            continue

        if capturing_death and tag == 'DATE':
            current_data['death'] = ' '.join(arguments)
            capturing_death = False
            continue

    if current_indi_id is not None:
        individuals[current_indi_id] = current_data

    return individuals.items()  # Return a tuple of (individual ID, individual data)

# Function to calculate age difference in years
def years_difference(date1, date2):
    return abs((date1 - date2).days) / 365.25
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
    print("=====Checking for overlapping marriages=====")
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
        print("=====Checking that Children should be born after marriage of parents=====")
        # Check constraint 1: Children should be born after marriage of parents
        if marriage_date:
            for child in children:
                birth_date = child['BIRT']
                if birth_date and birth_date < marriage_date:
                    errors.append(f"ERROR: FAMILY: US08: Child {child} born before marriage.")
                if divorce_date and birth_date and birth_date > divorce_date and birth_date <= divorce_date + timedelta(days=9*30):
                    errors.append(f"ERROR: FAMILY: US08: Child {child} born more than 9 months after divorce.")
        print("=====Checking that Child should be born before death of mother and before 9 months after death of father=====")
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
        print("=====Checking that Marriage should be at least 14 years after birth of both spouses=====")
        # Check constraint 3: Marriage should be at least 14 years after birth of both spouses
        husband_birth_date = husband['BIRT']
        wife_birth_date = wife['BIRT']
        if marriage_date and husband_birth_date and wife_birth_date:
            if years_difference(marriage_date, husband_birth_date) < 14:
                errors.append(f"ERROR: FAMILY: US10: Marriage of husband {fam['HUSB']} occurred before he was 14.")
            if years_difference(marriage_date, wife_birth_date) < 14:
                errors.append(f"ERROR: FAMILY: US10: Marriage of wife {fam['WIFE']} occurred before she was 14.")
        print("=====Checking that Parents' ages at child's birth=====")
        # Check constraint 5: Parents' ages at child's birth
        for child in children:
            birth_date = child['BIRT']
            if birth_date:
                if husband_birth_date and years_difference(birth_date, husband_birth_date) > 80:
                    errors.append(f"ERROR: FAMILY: US12: Father {fam['HUSB']} more than 80 years older than child {child}.")
                if wife_birth_date and years_difference(birth_date, wife_birth_date) > 60:
                    errors.append(f"ERROR: FAMILY: US12: Mother {fam['WIFE']} more than 60 years older than child {child}.")

    return errors


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
def main():
    print("Program Starting...")

    if logger:
        print("Starting application")
    try:
        if logger:
            print("Reading GEDCOM file: " + gedcom_file_path)
        with open(gedcom_file_path, "r") as gedcom_file:
            lines = gedcom_file.readlines()  # Read all lines into memory
        
        if logger:
            print("Processing GEDCOM lines...")
        valid_lines = []
        for line in lines:
            processed_line, is_valid = process_gedcom_line(line)
            if is_valid == 'Y':
                if verbouseLogger:
                    print("Appending valid line: " + line)
                valid_lines.append(processed_line)
        if logger:
            print("Invalid lines removed: " + str(len(lines) - len(valid_lines)))
            print("Valid lines remaining: " + str(len(valid_lines)))
            print("Total lines processed: " + str(len(lines)))
        if verbouseLogger:
            for line in valid_lines:
                print(line)
            print("END OF VALID LINES")
        # Now, proceed with processing only valid lines
        individuals = create_individual_from_lines(valid_lines)
        if logger:    
            print("Found " + str(len(individuals)) + " Individuals Processed")
        
        # Create individual table
        individual_table = PrettyTable()
        individual_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]
        if logger:
            for individual in individuals:
                print(individual)
        # Create individual table 
        if logger:
            print("Creating Individual Table")
        individual_table = PrettyTable()
        individual_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]

        for individual_id, data in individuals:
            birth_date = data.get('birth', '')
            if not birth_date.strip():
                birth_date = "N/A"

            age = calculate_age(birth_date) if birth_date else "N/A"
            alive = "Yes" if not data.get('death', '') else "No"
            individual_table.add_row([individual_id, data.get('name', ''), data.get('sex', ''), birth_date, age, alive, data.get('death', '')])

        # Create a custom lookup dictionary for individuals
        individuals_dict = {}
        families_dict = {}
        for indiv_tuple in individuals:
            individual_id = indiv_tuple[0]
            individual_details = indiv_tuple[1]
            individual_name = individual_details.get('name', 'Unknown')
            individual_sex = individual_details.get('sex', 'Unknown')
            individual_birth = individual_details.get('birth', 'Unknown')
            individual_death = individual_details.get('death', 'Unknown')
            
            individuals_dict[individual_id] = {
                'name': individual_name,
                'sex': individual_sex,
                'birth': individual_birth,
                'death': individual_death,
            }

            if logger:
                print("Processed:", indiv_tuple)

        families = create_family_from_lines(valid_lines, individuals_dict)
        if logger:
            print("Found " + str(len(families)) + " Families Processed")


        # Create family table
        family_table = PrettyTable()
        family_table.field_names = ["Family ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
        for data in families:
            family_id = data.get('ID')
            husband_id = data.get('Husband ID')
            husband_name = individuals_dict.get(husband_id, {}).get('name', 'Unknown')
            
            wife_id = data.get('Wife ID')
            wife_name = individuals_dict.get(wife_id, {}).get('name', 'Unknown')
            
            children_ids = data.get('Children', [])
            children_names = [individuals_dict.get(child_id, {}).get('name', 'Unknown') for child_id in children_ids]
            children = ', '.join(children_names) if children_names else 'N/A'
            
            married_value = data.get('Married')
            married_status = 'N/A' if married_value == [] else married_value

            divorced_value = data.get('Divorced')
            divorced_status = 'N/A' if divorced_value == [] else divorced_value
            
            family_table.add_row([family_id, married_status, divorced_status, husband_id, husband_name, wife_id, wife_name, children])

        # Print individual data
        print("\nIndividuals:")
        print(individual_table)

        # Print family data
        print("\nFamilies:")
        print(family_table)

        print("====== Dates after current Date ======")
        try:
            print(dates_before_current_date([line.strip() for line in lines]))
        except:
            print("error")
        print("====== Birth b4 Marriage ====== (true means yes)")
        try:
            print(birth_before_marriage([line.strip() for line in lines]))
        except:
            print("error")
        print("====== Birth b4 Death =======(true means yes)")
        try:
            print(birth_before_death([line.strip() for line in lines]))
        except:
            print("error")

        #User Story 29
        if perform_list_living_married_people:
            list_living_married_people(individuals, families)
        #User Story 30
        if perform_list_deceased_individuals:
            list_deceased_individuals(individuals)

        #User Story 31
        if perform_list_living_single_people:
            list_living_single_people(individuals, families)

        #User Story 32
        if perform_list_multiple_births:
            list_multiple_births(individuals, families)

        #User Story 33
        if perform_list_orphans:
            list_orphans(individuals_dict, families)

        #User Story 08 - Birth before marriage of parents	Children should be born after marriage of parents (and not more than 9 months after their divorce)

        #User Story 09 - Birth before death of parents	Child should be born before death of mother and before 9 months after death of father

        #User Story 10 - Marriage after 14	Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)

        #User Story 11 - No bigamy	Marriage should not occur during marriage to another spouse

        #User Story 12 - Parents not too old	Mother should be less than 60 years older than her children and father should be less than 80 years older than his children
        individuals_t, families_t = parse_gedcom(gedcom_file_path)
        errors = check_constraints(individuals_t, families_t)

        # Print errors
        for error in errors:
            print(error)
        print("========================================\nProgram Ended Successfully")

    except FileNotFoundError:
        print(f"File '{gedcom_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()