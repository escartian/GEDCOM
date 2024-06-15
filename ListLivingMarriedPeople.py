from Constants import logger, verbouseLogger

def list_living_married_people(individuals, families):
    """
    List all living, married individuals in the GEDCOM file.

    :param individuals: A dictionary of individuals parsed from the GEDCOM file.
    :param families: A list of family dictionaries parsed from the GEDCOM file.
    :return: A list of tuples containing the ID and details of each living, married individual.
    """
    living_married_individuals = []

    # Iterate over each family
    for family in families:
        husband_id = family.get('Husband ID')
        wife_id = family.get('Wife ID')
        husband_data = None
        wife_data = None
        divorced = family.get('Divorced')

        if divorced:
            continue
        if logger:
            print("list_living_married_people - Husband ID:", husband_id, "Wife ID:", wife_id)
        # Check if both husband and wife IDs exist in the individuals dictionary
        for individual_id, individual_data in individuals:
            if individual_id == husband_id:
                husband_data = individual_data
                if verbouseLogger:
                    print("list_living_married_people - Husband Data: " , husband_data)
                
            if individual_id == wife_id:
                wife_data = individual_data
                if verbouseLogger:
                    print("list_living_married_people - Wife Data: " , wife_data)

            if husband_data and wife_data:
                husband_alive = 'death' not in husband_data or not husband_data['death']
                wife_alive = 'death' not in wife_data or not wife_data['death']

                if husband_alive and wife_alive:
                    if logger:    
                        print("list_living_married_people - Both Alive")
                    living_married_individuals.append({
                        'ID': husband_id,
                        'Details': husband_data,
                        'Spouse_ID': wife_id
                    })
                    living_married_individuals.append({
                        'ID': wife_id,
                        'Details': wife_data,
                        'Spouse_ID': husband_id
                    })
                    #reset the data to avoid double entries
                    husband_data = None
                    wife_data = None
    if logger:
        print(living_married_individuals)
    return living_married_individuals