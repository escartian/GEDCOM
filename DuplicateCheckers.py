"""
Module for detecting duplicate individuals and families in GEDCOM files.
"""
from Constants import logger


def detect_duplicate_individuals(individuals):
    """
    Detects duplicate individuals in a dictionary of individuals.

    Parameters:
        individuals (dict):
            the keys are individual IDs
            The values are dictionaries containing details of each individual.

    Returns:
        list: A list of tuples, where each tuple contains
            name, birth date, first seen ID, and current ID
            of a duplicate individual,
            or an empty list if there are no duplicates
    """
    seen = {}  # Dictionary to map (name, birth_date) to individual_id
    duplicates = []
    print("Starting duplicate individuals detection")
    for individual_id, details in individuals.items():
        name = details.get('name')
        birth_date = details.get('birth')
        # Composite key for checking duplicates
        key = (name, birth_date)
        if key in seen:
            # Duplicate found, print and add details to the duplicates list
            duplicates.append((name, birth_date, seen[key], individual_id))
            if logger:
                print(f"Duplicate individual found: Name={name}, Birth Date={birth_date}")
                print(f"First occurrence ID: {seen[key]}")
                print(f"Current occurrence ID: {individual_id}\n")
        else:
            # Store the ID for this key for future checks
            seen[key] = individual_id

    print(duplicates)
    print("Duplicate individuals detection completed")
    return duplicates


def check_unique_ids(individuals, families):
    """
    A function to check for non-unique IDs within a list of individuals and families.

    Parameters:
        individuals (list): A list of individual IDs to check for duplicates.
        families (list): A list of family IDs to check for duplicates.

    Returns:
        non_unique_individual_ids (set): A set containing the non-unique individual IDs found.
        non_unique_family_ids (set): A set containing the non-unique family IDs found.
    """
    print("Checking for non-unique IDs...")
    # Initialize sets for storing non-unique IDs
    non_unique_individual_ids = set()
    non_unique_family_ids = set()
    unique_family_ids = set()
    unique_individual_ids = set()
    # Extract individual IDs and check for duplicates
    for individual in individuals:
        ind_stripped = individual.strip("'")
        id = ind_stripped.split()[0]
        # id = individual[0]
        print(individual)
        if logger:
            print(f"Checking individual ID: {id}")
        if individual[0] in unique_individual_ids:
            print("Non-unique individual ID found: ", id)
            non_unique_individual_ids.add(id)
        else:
            unique_individual_ids.add(id)
    # Extract family IDs and check for duplicates
    for family in families:
        if logger:
            print(f"Checking family ID: {family['ID']}")
        if family['ID'] in unique_family_ids:
            print(f"Non-unique family ID found: {family['ID']}")
            non_unique_family_ids.add(family['ID'])
        else:
            unique_family_ids.add(family['ID'])
    if logger:
        print("non_unique_individual_ids", non_unique_individual_ids)
        print("non_unique_family_ids", non_unique_family_ids)
        print("Non-unique IDs checked.")
    print("Checking for non-unique IDs completed")
    return non_unique_individual_ids, non_unique_family_ids


def detect_duplicate_families(individuals, families):
    """
    Detects duplicate families in a list of individuals and families.

    Parameters:
        individuals (dict):
            the keys are individual IDs
            the values are dictionaries containing the details of each individual.
        families (list):
            A list of dictionaries representing families
            where each dictionary contains the details of a family.

    Returns:
        list: A list of dictionaries representing duplicate families.
    """
    print("Starting duplicate families detection")

    # Initialize a dictionary to store unique combinations of spouses and marriage dates
    unique_families = {}
    duplicate_families = {}

    # Iterate through the list of families
    for family in families:
        if logger:
            print("Family = ", family)
        # Fetch husband and wife details from the individuals dataset
        husband_name = individuals.get(family['Husband ID'], {}).get('name', '')
        wife_name = individuals.get(family['Wife ID'], {}).get('name', '')
        if logger:
            print(f"Checking family: {husband_name},{wife_name},{family['Married']}")
        # Construct a key from spouse names and marriage date
        key = f"{husband_name},{wife_name},{family['Married']}"
        # Add the family to the dictionary, using the constructed key
        # If the key already exists, it means we've found a duplicate
        if key not in unique_families:
            unique_families[key] = family
        else:
            if logger:
                print(f"Duplicate family found: {key}")
            duplicate_families[key] = family

    # Convert the dictionary values back into a list of families
    filtered_families = list(duplicate_families.values())
    print("Duplicate familes are: ", filtered_families)
    print("Duplicate families detection completed")
    return filtered_families


def detect_duplicate_children(individuals, families):
    """
    Detects duplicate children in a list of families.

    Parameters:
        individuals (dict):
            the keys are individual IDs
            the values are dictionaries containing details of each individual.
        families (list): A list of dictionaries representing families
            where each dictionary contains the details of a family.

    Returns:
        list: A list of child IDs that are duplicates.
    """
    print("Starting duplicate children detection")
    # Initialize a dictionary to track seen children by name and birth date
    seen_children = {}
    duplicate_children = []

    # Process each family
    for family in families:
        for child_id in family['Children']:
            # Extract child name and birth date from the individuals dictionary
            child_info = individuals.get(child_id)
            if child_info:
                child_name = child_info.get('name')
                child_birthdate = child_info.get('birth')
                # Check if the combination
                # name and birth date has been seen before
                if (child_name, child_birthdate) in seen_children:
                    # This is a duplicate
                    duplicate_children.append(child_id)
                else:
                    # Mark this combination as seen
                    seen_children[(child_name, child_birthdate)] = True
    print("Duplicate children are: ", duplicate_children)
    print("Duplicate children detection completed")
    return duplicate_children
