from Constants import logger, verbouseLogger
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