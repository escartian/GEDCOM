from datetime import datetime, timedelta

def parse_gedcom_data(gedcom_data):
    individuals = {}
    families = {}
    current_indi_id = None
    current_fam_id = None
    
    for line in gedcom_data:
        parts = line.split()
        level = int(parts[0])
        tag = parts[1]
        
        if level == 0:
            if tag == 'INDI':
                current_indi_id = parts[1][1:-1]  # Remove '@' symbols
                individuals[current_indi_id] = {'NAME': None, 'SEX': None}
            elif tag == 'FAM':
                current_fam_id = parts[1][1:-1]  # Remove '@' symbols
                families[current_fam_id] = {'HUSB': None, 'WIFE': None}
        elif level == 1:
            if tag == 'SEX' and current_indi_id:
                individuals[current_indi_id][tag] = parts[2]
            elif tag == 'HUSB' and current_fam_id:
                families[current_fam_id][tag] = parts[2][1:-1]  # Remove '@' symbols
            elif tag == 'WIFE' and current_fam_id:
                families[current_fam_id][tag] = parts[2][1:-1]  # Remove '@' symbols
    
    return individuals, families

class sprint3:

    def siblings_marrying(self, gedcom_data):
        individuals = {}
        families = {}
        current_id = None
        current_tag = None

        for line in gedcom_data:
            parts = line.strip().split()
            if not parts:
                continue

            if parts[0] == "0":
                if parts[1].startswith("@I"):
                    current_id = parts[1]
                    current_tag = "INDI"
                    individuals[current_id] = {'famc': None, 'fams': []}
                elif parts[1].startswith("@F"):
                    current_id = parts[1]
                    current_tag = "FAM"
                    families[current_id] = {'husb': None, 'wife': None, 'chil': []}
            elif parts[0] == "1":
                if current_tag == "INDI" and parts[1] == "FAMC":
                    individuals[current_id]['famc'] = parts[2]
                elif current_tag == "INDI" and parts[1] == "FAMS":
                    individuals[current_id]['fams'].append(parts[2])
                elif current_tag == "FAM" and parts[1] in ["HUSB", "WIFE"]:
                    families[current_id][parts[1].lower()] = parts[2]
                elif current_tag == "FAM" and parts[1] == "CHIL":
                    families[current_id]['chil'].append(parts[2])

        siblings = {}
        for fam_id, fam_data in families.items():
            for child in fam_data['chil']:
                if child not in siblings:
                    siblings[child] = set(fam_data['chil']) - {child}
                else:
                    siblings[child].update(set(fam_data['chil']) - {child})

        sibling_marriages = {}
        for indi_id, indi_data in individuals.items():
            if indi_data['fams']:
                for fam in indi_data['fams']:
                    spouse = families[fam]['husb'] if families[fam]['wife'] == indi_id else families[fam]['wife']
                    if spouse in siblings.get(indi_id, []):
                        sibling_marriages[fam] = (indi_id, spouse)

        return sibling_marriages
     
    
    def invalid_dates(self, gedcom_data):
        invalid_dates = {}

        # Function to check if a date string is valid
        def is_valid_date(date_str):
            try:
                datetime.strptime(date_str, '%d %b %Y')
                return True
            except ValueError:
                return False
        
        # Iterate through each line in GEDCOM data
        for line in gedcom_data:
            parts = line.split()
            if len(parts) >= 3 and parts[0] == '2' and parts[1] == 'DATE':
                date_str = ' '.join(parts[2:])
                if not is_valid_date(date_str):
                    # Extract the key for the invalid date
                    key = f"{parts[0]} {parts[1]} {parts[2]}"
                    invalid_dates[key] = date_str
        
        return invalid_dates

        
    def find_gender_violations(self, gedcom_data):
        gender_violations = []

        i = 0
        while i < len(gedcom_data):
            line = gedcom_data[i]
            parts = line.split()

            if len(parts) > 2:
                level = parts[0]
                tag = parts[1]
                pointer = parts[2]

                if level == "1" and tag == "SEX":
                    gender = parts[2]
                    if gender != "M" and gender != "F":
                        gender_violations.append(f"Invalid gender '{gender}' for individual with ID '{pointer}'.")

            i += 1

        return gender_violations