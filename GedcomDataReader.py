from collections import defaultdict
from datetime import datetime
from prettytable import PrettyTable
from ListLivingMarriedPeople import list_living_married_people
from Constants import *

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

def list_deceased_individuals(individuals):
    """
    Lists all deceased individuals along with their details.

    :param individuals: A dictionary view object of individuals extracted from the GEDCOM file.
    :return: None (prints the details of deceased individuals), or a list of deceased individuals' details.
    """
    print("\n=====Listing Deceased Individuals=====")
    deceased_individuals = []
    for individual_id, data in individuals:
        death_date = data.get('death')
        if death_date:
            # If verbose logging is enabled, print detailed information about the deceased individual
            if logger:
                print(f"Deceased Individual: ID={individual_id}, Name={data.get('name', 'Unknown')}, Sex={data.get('sex', 'Unknown')}, "
                      f"Birthday={data.get('birth', 'N/A')}, Death Date={death_date}")
            deceased_individuals.append({
                'ID': individual_id,
                'Name': data.get('name', 'Unknown'),
                'Sex': data.get('sex', 'Unknown'),
                'Birthday': data.get('birth', 'N/A'),
                'Death Date': death_date
            })
    
    # If there are no deceased individuals, inform the user
    if not deceased_individuals:
        print("No deceased individuals found.")
    else:

        for entry in deceased_individuals:
            print(entry)

        return deceased_individuals

def list_living_single_people(individuals, families):
    """
    Lists all living individuals who are considered single based on the absence of a marital relationship and the presence of a death date.

    :param individuals: A dictionary of individuals parsed from the GEDCOM file.
    :param families: A list of family dictionaries parsed from the GEDCOM file.
    :return: Prints the details of living single individuals.
    """
    print("\n=====Listing Single Living Individuals=====")
    single_individuals = []
    # Create sets of husband and wife IDs for quick lookup
    husband_ids = set(family.get('Husband ID') for family in families if family.get('Husband ID'))
    wife_ids = set(family.get('Wife ID') for family in families if family.get('Wife ID'))

    for individual_id, data in individuals:
        # Check if the individual is alive by verifying the absence of a death date
        if 'death' not in data or data['death'] == 'N/A':
            # Check if the individual is not part of any family as a husband or wife
            if individual_id not in husband_ids and individual_id not in wife_ids:
                single_individuals.append({
                    'ID': individual_id,
                    'Name': data.get('name', 'Unknown'),
                    'Sex': data.get('sex', 'Unknown'),
                    'Birthday': data.get('birth', 'N/A'),
                })
 
     # If there are no single individuals, inform the user
    if not single_individuals:
         print("No single individuals found.")
    else:
         # Optionally, print a header for better readability
         for entry in single_individuals:
             print(entry)
 
    return single_individuals
def list_multiple_births(individuals, families):
    """
    Identifies and lists instances of multiple births within the same family, adjusted to work with individuals as dict_items, prints the details, and returns the results.
    
    :param individuals: A dict_items object of individuals parsed from the GEDCOM file.
    :param families: A list of family dictionaries parsed from the GEDCOM file.
    :return: A list of dictionaries, each representing a family with multiple births and details of the children involved.
    """
    print("\n=====Listing Multiple Births=====")
    multiple_births = []  # List to accumulate families with multiple births for returning

    for family in families:
        children_dates = {}
        for child_id in family.get('Children', []):
            # Iterate through individuals to find the matching child_id and extract the birth date
            for individual_id, data in individuals:
                if individual_id == child_id:
                    birth_date = data.get('birth')
                    if birth_date:
                        if birth_date in children_dates:
                            children_dates[birth_date].append(child_id)
                        else:
                            children_dates[birth_date] = [child_id]
                    break  # Found the child, no need to continue searching
        
        for birth_date, child_ids in children_dates.items():
            if len(child_ids) > 1:
                # Print details as before
                print(f"Multiple Births Found: Family ID: {family.get('ID', 'Unknown')}")
                for child_id in child_ids:
                    # Find the child's name by iterating through individuals again
                    for individual_id, data in individuals:
                        if individual_id == child_id:
                            child_name = data.get('name', 'Unknown')
                            print(f"- Child ID: {child_id}, Name: {child_name}")
                            break  # Found the child, no need to continue searching
                
                # Accumulate details for return
                family_details = {
                    'Family ID': family.get('ID', 'Unknown'),
                    'Birth Date': birth_date,
                    'Children': [{'ID': child_id, 'Name': data.get('name', 'Unknown')} for individual_id, data in individuals if individual_id in child_ids]
                }
                multiple_births.append(family_details)
                if logger:
                    print(family_details)  #  the accumulated details for this family
                
    if not multiple_births:
        print("No instances of multiple births found.")
    else:
        if len(multiple_births) == 1:
            print("Found 1 instance of multiple births.")
        else:
            print(f"Found {len(multiple_births)} instances of multiple births.")
    
    return multiple_births

from datetime import datetime

def list_orphans(individuals, families):
    """
    Identifies and lists orphans within the families, considering age and parent's death information.

    :param individuals: A dictionary of individuals parsed from the GEDCOM file.
    :param families: A list of family dictionaries parsed from the GEDCOM file.
    :return: A list of dictionaries, each representing an orphan and their details.
    """
    print("\n=====Listing Orphans=====")
    orphans = []  # List to accumulate orphan details for returning

    today = datetime.today().year

    for family in families:
        husband_id = family.get('Husband ID')
        wife_id = family.get('Wife ID')
        children = family.get('Children', [])

        # Fetch husband and wife information from the individuals dictionary
        husband_info = individuals.get(husband_id, {})
        wife_info = individuals.get(wife_id, {})

        # Now you can safely access the 'death' key from husband_info and wife_info
        husband_deceased = husband_info.get('death') is not None
        wife_deceased = wife_info.get('death') is not None

        if husband_deceased and wife_deceased:
            for child_id in children:
                child_info = individuals.get(child_id, {})
                if child_info:
                    birth_year = int(child_info.get('birth').split('-')[0])
                    if (today - birth_year) < 18:  # Use current_year here
                        orphan_details = {
                            'Family ID': family.get('ID', 'Unknown'),
                            'Child ID': child_id,
                            'Name': child_info.get('name', 'Unknown'),
                            'Birth Year': birth_year
                        }
                        orphans.append(orphan_details)
                        if logger: 
                            print(f"Orphan: Family ID: {orphan_details['Family ID']}, Child ID: {orphan_details['Child ID']}, Name: {orphan_details['Name']}, Birth Year: {orphan_details['Birth Year']}")
                    else:
                        if logger:
                            print(f"Orphan Found: Child {child_id} is too old to be an orphan.")
    for orphan in orphans:
        print(orphan)

    if not orphans:
        print("No orphans found.")
    else:
        if len(orphans) == 1:
            print("Found 1 orphan.")
        else:
            print(f"Found {len(orphans)} instances of orphans.")

    return orphans

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
            print("List Multiple Births")
            list_multiple_births(individuals, families)

        #User Story 33
        if perform_list_orphans:
            list_orphans(individuals_dict, families)

        print("========================================\nProgram Ended Successfully")

    except FileNotFoundError:
        print(f"File '{gedcom_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
