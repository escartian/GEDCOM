from datetime import datetime, timedelta

# Function to check if date is within the next 30 days
def is_within_next_30_days(date):
    if not date:
        return False
    today = datetime.today()
    anniv_date = datetime.strptime(date, "%d %b %Y")
    this_year_anniv = anniv_date.replace(year=today.year)
    next_year_anniv = anniv_date.replace(year=today.year + 1)

    return (0 <= (this_year_anniv - today).days <= 30) or (0 <= (next_year_anniv - today).days <= 30)


class sprint4: 

    def check_gender_roles(self, gedcom_data):
        individuals = {}
        families = {}
        current_indi = None
        current_fam = None
        errors = []
        no_gender = []

        # Parse the GEDCOM data
        for line in gedcom_data:
            parts = line.strip().split()
            if len(parts) < 3:
                continue

            level = parts[0]
            tag = parts[1].upper()

            if level == "0":
                if "INDI" in parts[2]:
                    current_indi = parts[1]
                    individuals[current_indi] = {"SEX": None}
                elif "FAM" in parts[2]:
                    current_fam = parts[1]
                    families[current_fam] = {"HUSB": None, "WIFE": None}
            elif level == "1" and tag == "SEX" and current_indi:
                individuals[current_indi]["SEX"] = parts[2]
            elif level == "1" and tag == "HUSB" and current_fam:
                families[current_fam]["HUSB"] = parts[2]
            elif level == "1" and tag == "WIFE" and current_fam:
                families[current_fam]["WIFE"] = parts[2]

        # Check gender roles
        for fam_id, family in families.items():
            husb_id = family["HUSB"]
            wife_id = family["WIFE"]

            if husb_id:
                if husb_id not in individuals or individuals[husb_id]["SEX"] is None:
                    no_gender.append(f"Family {fam_id}: Husband {husb_id} gender not specified")
                elif individuals[husb_id]["SEX"] != "M":
                    errors.append(f"Family {fam_id}: Husband {husb_id} is not male")
            if wife_id:
                if wife_id not in individuals or individuals[wife_id]["SEX"] is None:
                    no_gender.append(f"Family {fam_id}: Wife {wife_id} gender not specified")
                elif individuals[wife_id]["SEX"] != "F":
                    errors.append(f"Family {fam_id}: Wife {wife_id} is not female")

        return errors


    def list_upcoming_anniversaries(self, gedcom_data):
        individuals = {}
        upcoming_anniversaries = []
    
        current_indi = None
        current_fam = None
        husb_id = None
        wife_id = None

        # Had a big issue with the parts parts = line.strip().split() line.
        # For some reason it wasn't working as expected for line liek "1 MARR," or "1 BIRT"
        # So I found some work arounds like the maxplit param that works for this function 
        for i, line in enumerate(gedcom_data):
            parts = line.strip().split(maxsplit=2)
            if len(parts) < 2:
                continue

            level = parts[0]
            tag = parts[1].upper()

            if level == "0":
                current_indi = None
                current_fam = None
                if len(parts) > 2 and parts[2] == "INDI":
                    current_indi = parts[1]
                    individuals[current_indi] = {"NAME": None, "DEAT": None}
                elif len(parts) > 2 and parts[2] == "FAM":
                    current_fam = parts[1]
                    husb_id = None
                    wife_id = None
            elif level == "1" and tag == "NAME" and current_indi:
                individuals[current_indi]["NAME"] = parts[2]
            elif level == "1" and tag == "DEAT" and current_indi:
                if i + 1 < len(gedcom_data):
                    next_line = gedcom_data[i + 1].strip().split(maxsplit=2)
                    if len(next_line) > 2 and next_line[1].upper() == "DATE":
                        individuals[current_indi]["DEAT"] = " ".join(next_line[2:])
            elif level == "1" and tag == "HUSB" and current_fam:
                husb_id = parts[2]
            elif level == "1" and tag == "WIFE" and current_fam:
                wife_id = parts[2]
            elif level == "1" and tag == "MARR" and current_fam:
                if i + 1 < len(gedcom_data):
                    next_line = gedcom_data[i + 1].strip().split(maxsplit=2)
                    if len(next_line) > 2 and next_line[1].upper() == "DATE":
                        marr_date = " ".join(next_line[2:])
                        # Check if the marriage date is within the next 30 days
                        if is_within_next_30_days(marr_date):
                            if husb_id in individuals and wife_id in individuals:
                                husb = individuals[husb_id]
                                wife = individuals[wife_id]
                                if not husb["DEAT"] and not wife["DEAT"]:
                                    upcoming_anniversaries.append(f"{husb['NAME']} and {wife['NAME']} have an anniversary on {marr_date}")

        return upcoming_anniversaries
            