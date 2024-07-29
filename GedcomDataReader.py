import re
from collections import defaultdict
from prettytable import PrettyTable
from ListLivingMarriedPeople import list_living_married_people
from DuplicateCheckers import *
from Lists import *
from Constants import *
from datetime import datetime, timedelta


def parse_date_helper(date):
    try:
        if len(date.split()) == 3:
            return datetime.strptime(date, "%d %b %Y").date()
        elif len(date.split()) == 2:
            return datetime.strptime(date, "%b %Y").date()
        elif len(date.split()) == 1:
            return datetime.strptime(date, "%Y").date()
    except ValueError:
        return None

def is_within_next_30_days(date):
    if not date:
        return False
    today = datetime.today()
    try:
        anniv_date = datetime.strptime(date, "%d %b %Y")
    except ValueError:
        return False
    this_year_anniv = anniv_date.replace(year=today.year)
    next_year_anniv = anniv_date.replace(year=today.year + 1)
    return (0 <= (this_year_anniv - today).days <= 30) or (0 <= (next_year_anniv - today).days <= 30)

def dates_before_current_date(gedcom_lines):
    current_date = datetime.now()
    events = ["BIRT", "MARR", "DIV", "DEAT"]
    invalid_dates = []

    # Iterate through gedcom lines
    for i, line in enumerate(gedcom_lines):
        parts = line.strip().split()
        if parts and parts[0] in ["1", "2"] and parts[1] in events:
            date_line = gedcom_lines[i + 1].strip()
            date_parts = date_line.split()
            if date_parts[0] == "2" and date_parts[1] == "DATE":
                event_date = parse_date_helper(" ".join(date_parts[2:]))
                if event_date and event_date > current_date:
                    invalid_dates.append((i + 1, line, date_line))

    return invalid_dates


def check_gender_roles(gedcom_data):
    individuals = {}
    families = {}
    current_indi = None
    current_fam = None
    errors = []
    no_gender = []

    # Parse the GEDCOM data
    for i, line in enumerate(gedcom_data):
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
                no_gender.append(f"Line {i + 1}: Family {fam_id}: Husband {husb_id} gender not specified")
            elif individuals[husb_id]["SEX"] != "M":
                errors.append(f"Line {i + 1}: Family {fam_id}: Husband {husb_id} is not male")
        if wife_id:
            if wife_id not in individuals or individuals[wife_id]["SEX"] is None:
                no_gender.append(f"Line {i + 1}: Family {fam_id}: Wife {wife_id} gender not specified")
            elif individuals[wife_id]["SEX"] != "F":
                errors.append(f"Line {i + 1}: Family {fam_id}: Wife {wife_id} is not female")

    return errors


def list_upcoming_anniversaries(gedcom_data):
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
                                upcoming_anniversaries.append(
                                    f"{husb['NAME']} and {wife['NAME']} have an anniversary on {marr_date}")

    return upcoming_anniversaries


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

    # print(individuals)

    results = {}
    for ind_id, (b_date, m_date) in individuals.items():
        results[ind_id] = b_date < m_date if b_date and m_date else None
    # print(results)
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

    # print(individuals)

    results = {}
    for ind_id, (b_date, m_date) in individuals.items():
        results[ind_id] = b_date < m_date if b_date and m_date else None
        print(results)

    return results


def divorce_before_marriage(gedcom_data):
    fams = {}
    current_fam_id = None
    marriage_date = None
    divorce_date = None
    # print(gedcom_data)

    for i, line in enumerate(gedcom_data):
        parts = line.strip().split()
        # print(parts)
        if parts:
            # print(parts[1])
            if (parts[0] == "0" and "@F" in parts[1]):
                # print("here")
                if (current_fam_id):
                    fams[current_fam_id] = (marriage_date, divorce_date)
                current_fam_id = parts[1]
                marriage_date = None
                divorce_date = None
            elif (parts[0] == "1"):
                if (parts[1] == "MARR"):
                    date_line = gedcom_data[i + 1].strip()
                    date_parts = date_line.split()
                    if (date_parts[0] == "2" and date_parts[1] == "DATE"):
                        marriage_date = parse_date_helper(" ".join(date_parts[2:]))
                elif (parts[1] == "DIV"):
                    date_line = gedcom_data[i + 1].strip()
                    date_parts = date_line.split()
                    if (date_parts[0] == "2" and date_parts[1] == "DATE"):
                        divorce_date = parse_date_helper(" ".join(date_parts[2:]))
                        # print("div: ", divorce_date)
    # print(current_fam_id)
    # print(marriage_date)
    # print(divorce_date)
    if (current_fam_id):
        fams[current_fam_id] = (marriage_date, divorce_date)

    results = {}
    # print(fams)
    for fam_id, (mar_date, div_date) in fams.items():
        if (mar_date and div_date):
            # print("m date", mar_date)
            # print(div_date)
            if (div_date < mar_date):
                results[fam_id] = (mar_date.strftime('%d %b %Y').upper(), div_date.strftime('%d %b %Y').upper())
            # if (div_date < mar_date):
            #    print(f"Divorce before marriage in fam {fam_id}")
            #    print(f"Marriage Date: {mar_date.strftime('%d %b %Y')}")
            #    print(f"Divorce Date: {div_date.strftime('%d %b %Y')}")
    # print(results)
    return results


def death_before_marriage(gedcom_data):
    fams = {}
    inds = {}
    current_fam_id = None
    marriage_date = None
    husband_id = None
    wife_id = None

    for i, line in enumerate(gedcom_data):
        parts = line.strip().split()
        if parts:
            if parts[0] == "0" and "@I" in parts[1]:
                current_ind_id = parts[1]
                death_date = None
                birth_date = None
                for j in range(i + 1, len(gedcom_data)):
                    sub_parts = gedcom_data[j].strip().split()
                    if sub_parts[0] == "0":
                        break
                    if sub_parts[0] == "1" and sub_parts[1] == "BIRT":
                        date_line = gedcom_data[j + 1].strip()
                        date_parts = date_line.split()
                        if date_parts[0] == "2" and date_parts[1] == "DATE":
                            birth_date = parse_date_helper(" ".join(date_parts[2:]))
                    if sub_parts[0] == "1" and sub_parts[1] == "DEAT":
                        date_line = gedcom_data[j + 1].strip()
                        date_parts = date_line.split()
                        if date_parts[0] == "2" and date_parts[1] == "DATE":
                            death_date = parse_date_helper(" ".join(date_parts[2:]))
                inds[current_ind_id] = (birth_date, death_date)
            elif parts[0] == "0" and "@F" in parts[1]:
                if current_fam_id:
                    fams[current_fam_id] = (marriage_date, husband_id, wife_id)
                current_fam_id = parts[1]
                marriage_date = None
                husband_id = None
                wife_id = None
            elif parts[0] == "1":
                if parts[1] == "HUSB":
                    husband_id = parts[2]
                elif parts[1] == "WIFE":
                    wife_id = parts[2]
                elif parts[1] == "MARR":
                    date_line = gedcom_data[i + 1].strip()
                    date_parts = date_line.split()
                    if date_parts[0] == "2" and date_parts[1] == "DATE":
                        marriage_date = parse_date_helper(" ".join(date_parts[2:]))

    if current_fam_id:
        fams[current_fam_id] = (marriage_date, husband_id, wife_id)

    results = {}
    for fam_id, (mar_date, husb_id, wife_id) in fams.items():
        if mar_date:
            husb_death_date = inds.get(husb_id, (None, None))[1]
            wife_death_date = inds.get(wife_id, (None, None))[1]
            if (husb_death_date and mar_date > husb_death_date) or (wife_death_date and mar_date > wife_death_date):
                results[fam_id] = (mar_date.strftime('%d %b %Y').upper(),
                                   husb_death_date.strftime('%d %b %Y').upper() if husb_death_date else None,
                                   wife_death_date.strftime('%d %b %Y').upper() if wife_death_date else None)
    return results


def divorce_before_death(gedcom_data):
    fams = {}
    inds = {}
    current_fam_id = None
    divorce_date = None
    husband_id = None
    wife_id = None

    for i, line in enumerate(gedcom_data):
        parts = line.strip().split()
        if parts:
            if parts[0] == "0" and "@I" in parts[1]:
                current_ind_id = parts[1]
                death_date = None
                birth_date = None
                for j in range(i + 1, len(gedcom_data)):
                    sub_parts = gedcom_data[j].strip().split()
                    if sub_parts[0] == "0":
                        break
                    if sub_parts[0] == "1" and sub_parts[1] == "BIRT":
                        date_line = gedcom_data[j + 1].strip()
                        date_parts = date_line.split()
                        if date_parts[0] == "2" and date_parts[1] == "DATE":
                            birth_date = parse_date_helper(" ".join(date_parts[2:]))
                    if sub_parts[0] == "1" and sub_parts[1] == "DEAT":
                        date_line = gedcom_data[j + 1].strip()
                        date_parts = date_line.split()
                        if date_parts[0] == "2" and date_parts[1] == "DATE":
                            death_date = parse_date_helper(" ".join(date_parts[2:]))
                inds[current_ind_id] = (birth_date, death_date)
            elif parts[0] == "0" and "@F" in parts[1]:
                if current_fam_id:
                    fams[current_fam_id] = (divorce_date, husband_id, wife_id)
                current_fam_id = parts[1]
                divorce_date = None
                husband_id = None
                wife_id = None
            elif parts[0] == "1":
                if parts[1] == "HUSB":
                    husband_id = parts[2]
                elif parts[1] == "WIFE":
                    wife_id = parts[2]
                elif parts[1] == "DIV":
                    date_line = gedcom_data[i + 1].strip()
                    date_parts = date_line.split()
                    if date_parts[0] == "2" and date_parts[1] == "DATE":
                        divorce_date = parse_date_helper(" ".join(date_parts[2:]))

    if current_fam_id:
        fams[current_fam_id] = (divorce_date, husband_id, wife_id)

    results = {}
    for fam_id, (div_date, husb_id, wife_id) in fams.items():
        # print(div_date)

        if div_date:
            husb_death_date = inds.get(husb_id, (None, None))[1]
            wife_death_date = inds.get(wife_id, (None, None))[1]
            # print(husb_death_date)
            # print(wife_death_date)
            if (husb_death_date and div_date > husb_death_date) or (wife_death_date and div_date > wife_death_date):
                # print("husb ddate: ", husb_death_date)
                results[fam_id] = (div_date.strftime('%d %b %Y').upper(),
                                   husb_death_date.strftime('%d %b %Y').upper() if husb_death_date else None,
                                   wife_death_date.strftime('%d %b %Y').upper() if wife_death_date else None)
    # results {divorce date, husb death date, wife death date}
    # print(results)
    return results


def over_150(gedcom_data):
    inds = {}
    over_150 = {}

    i = 0
    while i < len(gedcom_data):
        line = gedcom_data[i]
        parts = line.strip().split()
        if parts:
            if parts[0] == "0" and "@I" in parts[1]:
                current_id = parts[1]
            elif parts[0] == "1":
                if parts[1] == "BIRT":
                    i += 1
                    date_line = gedcom_data[i].strip()
                    date_parts = date_line.split()
                    if date_parts[0] == "2" and date_parts[1] == "DATE":
                        birth_date = parse_date_helper(" ".join(date_parts[2:]))
                        inds[current_id] = birth_date
                elif parts[1] == "DEAT":
                    i += 1
                    date_line = gedcom_data[i].strip()
                    date_parts = date_line.split()
                    if date_parts[0] == "2" and date_parts[1] == "DATE":
                        death_date = parse_date_helper(" ".join(date_parts[2:]))
                        if (death_date - inds[current_id]).days > 365 * 150:
                            over_150[current_id] = (
                                inds[current_id].strftime('%d %b %Y'),
                                death_date.strftime('%d %b %Y')
                            )
        i += 1
    # over_150 = {IND_ID: (birth date, death date)}
    return over_150


def siblings_marrying(gedcom_data):
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


def invalid_dates(gedcom_data):
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
        if tag == 'DATE' and is_valid == 'Y':
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
        # if len(tokens) < 2:
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
    # Collect all marriages
    marriages = {}
    for fam_id, fam in families.items():
        marriage_date = fam['MARR']
        divorce_date = fam['DIV'] or datetime.max
        husband_id = fam['HUSB']
        wife_id = fam['WIFE']
        fam_line = fam.get('LINE', 'unknown')

        if marriage_date:
            if husband_id not in marriages:
                marriages[husband_id] = []
            marriages[husband_id].append((marriage_date, divorce_date, fam_id, fam_line))

            if wife_id not in marriages:
                marriages[wife_id] = []
            marriages[wife_id].append((marriage_date, divorce_date, fam_id, fam_line))

    print("=====Checking for overlapping marriages=====")
    # Check for overlapping marriages
    for ind_id, ind_marriages in marriages.items():
        ind_marriages.sort()
        for i in range(len(ind_marriages) - 1):
            if ind_marriages[i][1] > ind_marriages[i + 1][0]:
                print(
                    f"ERROR: FAMILY: US11: Individual {ind_id} has overlapping marriages in families {ind_marriages[i][2]} (line {ind_marriages[i][3]}) and {ind_marriages[i + 1][2]} (line {ind_marriages[i + 1][3]}).")

    # Check other constraints
    for fam_id, fam in families.items():
        marriage_date = fam['MARR']
        divorce_date = fam['DIV']
        husband = individuals.get(fam['HUSB'])
        wife = individuals.get(fam['WIFE'])
        children = [individuals.get(child) for child in fam['CHIL']]
        fam_line = fam.get('LINE', 'unknown')

        print("=====Checking that Children should be born after marriage of parents=====")
        if marriage_date:
            for child in children:
                birth_date = child['BIRT']
                if birth_date and birth_date < marriage_date:
                    print(f"ERROR: FAMILY: US08: Child {child['ID']} born before marriage in family {fam_id} (line {fam_line}).")
                if divorce_date and birth_date and birth_date > divorce_date and birth_date <= divorce_date + timedelta(days=9 * 30):
                    print(f"ERROR: FAMILY: US08: Child {child['ID']} born more than 9 months after divorce in family {fam_id} (line {fam_line}).")

        print("=====Checking that Child should be born before death of mother and before 9 months after death of father=====")
        wife_death_date = wife['DEAT']
        husband_death_date = husband['DEAT']
        for child in children:
            birth_date = child['BIRT']
            if birth_date:
                if wife_death_date and birth_date > wife_death_date:
                    print(f"ERROR: FAMILY: US09: Child {child['ID']} born after death of mother in family {fam_id} (line {fam_line}).")
                if husband_death_date and birth_date > husband_death_date + timedelta(days=9 * 30):
                    print(f"ERROR: FAMILY: US09: Child {child['ID']} born more than 9 months after death of father in family {fam_id} (line {fam_line}).")

        print("=====Checking that Marriage should be at least 14 years after birth of both spouses=====")
        husband_birth_date = husband['BIRT']
        wife_birth_date = wife['BIRT']
        if marriage_date and husband_birth_date and wife_birth_date:
            if years_difference(marriage_date, husband_birth_date) < 14:
                print(f"ERROR: FAMILY: US10: Marriage of husband {fam['HUSB']} occurred before he was 14 in family {fam_id} (line {fam_line}).")
            if years_difference(marriage_date, wife_birth_date) < 14:
                print(f"ERROR: FAMILY: US10: Marriage of wife {fam['WIFE']} occurred before she was 14 in family {fam_id} (line {fam_line}).")

        print("=====Checking that Parents' ages at child's birth=====")
        for child in children:
            birth_date = child['BIRT']
            if birth_date:
                if husband_birth_date and years_difference(birth_date, husband_birth_date) > 80:
                    print(f"ERROR: FAMILY: US12: Father {fam['HUSB']} more than 80 years older than child {child['ID']} in family {fam_id} (line {fam_line}).")
                if wife_birth_date and years_difference(birth_date, wife_birth_date) > 60:
                    print(f"ERROR: FAMILY: US12: Mother {fam['WIFE']} more than 60 years older than child {child['ID']} in family {fam_id} (line {fam_line}).")

        if 'CHIL' in fam:
            children = fam['CHIL']
            birth_dates = [individuals[child]['BIRT'] for child in children]
            birth_dates.sort()
            print("=====Checking that Birth dates of siblings should be more than 8 months apart or less than 2 days apart=====")
            for i in range(len(birth_dates) - 1):
                diff = (birth_dates[i + 1] - birth_dates[i]).days
                if diff < 2 or diff > 243:
                    continue
                print(f"ERROR: FAMILY: US13: Siblings {children[i]} and {children[i + 1]} born too close together or too far apart: {diff} days apart in family {fam_id} (line {fam_line}).")

            print("=====Checking that No more than five siblings should be born at the same time=====")
            birth_date_counts = {}
            for date in birth_dates:
                if date not in birth_date_counts:
                    birth_date_counts[date] = 0
                birth_date_counts[date] += 1

            for date, count in birth_date_counts.items():
                if count > 5:
                    print(f"ERROR: FAMILY: US14: More than five siblings born at the same time on {date} in family {fam_id} (line {fam_line}).")

            print("=====Checking that There should be fewer than 15 siblings in a family=====")
            if len(children) >= 15:
                print(f"ERROR: FAMILY: US15: More than 14 siblings in family {fam_id} (line {fam_line}).")

        print("=====Checking that All male members of a family should have the same last name=====")
        male_last_names = set()
        for child_id in fam.get('CHIL', []):
            child = individuals[child_id]
            if child.get('SEX') is None:
                print(f"ERROR: FAMILY: US16: Child {child_id} in family {fam_id} does not have a gender (line {fam_line}).")
                continue
            if child['SEX'] == 'M':
                last_name = child['NAME'].split('/')[-1].strip()
                male_last_names.add(last_name)
        if len(male_last_names) > 1:
            print(f"ERROR: FAMILY: US16: Males in family {fam_id} do not have the same last name: {male_last_names} (line {fam_line}).")

        print("=====Checking that Parents should not marry any of their descendants=====")
        husband_id = fam.get('HUSB')
        wife_id = fam.get('WIFE')
        descendants = set()

        def get_descendants(ind_id, families, individuals):
            nonlocal descendants
            for fam_id in individuals[ind_id]['FAMS']:
                for child_id in families[fam_id]['CHIL']:
                    descendants.add(child_id)
                    get_descendants(child_id, families, individuals)

        if husband_id:
            get_descendants(husband_id, families, individuals)
        if wife_id:
            get_descendants(wife_id, families, individuals)

        if husband_id in descendants or wife_id in descendants:
            print(f"ERROR: FAMILY: US17: Parent married to a descendant in family {fam_id} (line {fam_line}).")


def parse_gedcom(file_path):
    individuals = {}
    families = {}
    current_individual = None
    current_family = None
    date_tag = None

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
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
                        'FAMC': None,
                        'LINE': i + 1  # Store line number
                    }
                elif tag.startswith('@F'):
                    current_family = tag
                    families[current_family] = {
                        'HUSB': None,
                        'WIFE': None,
                        'CHIL': [],
                        'MARR': None,
                        'DIV': None,
                        'LINE': i + 1  # Store line number
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


def list_recent_births(individuals):
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Birth Date"]
    today = datetime.today()
    for ind_id, ind in individuals.items():
        if ind['BIRT'] and (today - ind['BIRT']).days <= 30:
            table.add_row([ind_id, ind.get('NAME', 'N/A'), ind['BIRT'].strftime("%d %b %Y")])
    print("Recent Births:")
    print(table)


def list_recent_deaths(individuals):
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Death Date"]
    today = datetime.today()
    for ind_id, ind in individuals.items():
        if ind['DEAT'] and (today - ind['DEAT']).days <= 30:
            table.add_row([ind_id, ind.get('NAME', 'N/A'), ind['DEAT'].strftime("%d %b %Y")])
    print("Recent Deaths:")
    print(table)


def list_recent_survivors(individuals, families):
    table = PrettyTable()
    table.field_names = ["Deceased ID", "Deceased Name", "Survivor ID", "Survivor Name"]
    today = datetime.today()
    for ind_id, ind in individuals.items():
        if ind['DEAT'] and (today - ind['DEAT']).days <= 30:
            # List living spouses
            for fam_id in ind['FAMS']:
                family = families[fam_id]
                spouse_id = family['HUSB'] if family['HUSB'] != ind_id else family['WIFE']
                if individuals[spouse_id]['DEAT'] is None:
                    table.add_row(
                        [ind_id, ind.get('NAME', 'N/A'), spouse_id, individuals[spouse_id].get('NAME', 'N/A')])
            # List living children
            if ind['FAMC']:
                for fam_id in ind['FAMC']:
                    family = families[fam_id]
                    for child_id in family['CHIL']:
                        if individuals[child_id]['DEAT'] is None:
                            table.add_row(
                                [ind_id, ind.get('NAME', 'N/A'), child_id, individuals[child_id].get('NAME', 'N/A')])
    print("Recent Survivors of Deceased:")
    print(table)


def list_upcoming_birthdays(individuals):
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Birthday"]
    today = datetime.today()
    for ind_id, ind in individuals.items():
        if ind['BIRT'] and ind['DEAT'] is None:
            birth_date_this_year = ind['BIRT'].replace(year=today.year)
            if 0 <= (birth_date_this_year - today).days <= 30:
                table.add_row([ind_id, ind.get('NAME', 'N/A'), ind['BIRT'].strftime("%d %b %Y")])
    print("Upcoming Birthdays:")
    print(table)


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
            individual_table.add_row([individual_id, data.get('name', ''), data.get('sex', ''), birth_date, age, alive,
                                      data.get('death', '')])

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

        families_dict = {family['ID']: family for family in families}

        # Create family table
        family_table = PrettyTable()
        family_table.field_names = ["Family ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID",
                                    "Wife Name", "Children"]
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

            family_table.add_row(
                [family_id, married_status, divorced_status, husband_id, husband_name, wife_id, wife_name, children])

        # Print individual data
        print("\nIndividuals:")
        print(individual_table)

        # Print family data
        print("\nFamilies:")
        print(family_table)

        # User Story 22
        if perform_check_unique_ids:
            check_unique_ids(individuals, families)
        # User Story 23
        if perform_detect_duplicate_infividuals:
            detect_duplicate_individuals(individuals_dict)
        # User Story 24
        if perform_detect_duplicate_families:
            detect_duplicate_families(individuals_dict, families)
        # User Story 25
        if perform_detect_duplicate_children:
            detect_duplicate_children(individuals_dict, families)

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
        print("====== Divorce b4 Marriage ======")
        try:
            print(divorce_before_marriage([line.strip() for line in lines]))
        except:
            print("error")
        print("====== Death b4 Marraige ======")
        try:
            print(death_before_marriage([line.strip() for line in lines]))
        except:
            print("error")
        print("====== Divorce b4 death ======")
        try:
            print(divorce_before_death([line.strip() for line in lines]))
        except:
            print("error")
        print("====== Age over 150 ======")
        try:
            print(over_150([line.strip() for line in lines]))
        except:
            print("error")
        print("====== siblings married ======")
        try:
            print(siblings_marrying([line.strip() for line in lines]))
        except:
            print("error")
        print("====== invalid Dates ======")
        try:
            print(invalid_dates([line.strip() for line in lines]))
        except:
            print("error")
        print("====== Gender Roles ======")
        try:
            print(check_gender_roles([line.strip() for line in lines]))
        except:
            print("error")
        print("====== Upcoming Anniversaries ======")
        try:
            print(list_upcoming_anniversaries([line.strip() for line in lines]))
        except:
            print("Invalid dates have rendered the upcoming anniversaries function useless, refactoring required")

        # User Story 29
        if perform_list_living_married_people:
            list_living_married_people(individuals, families)
        # User Story 30
        if perform_list_deceased_individuals:
            list_deceased_individuals(individuals)
        # User Story 31
        if perform_list_living_single_people:
            list_living_single_people(individuals, families)
        # User Story 32
        if perform_list_multiple_births:
            list_multiple_births(individuals, families)
        # User Story 33
        if perform_list_orphans:
            list_orphans(individuals_dict, families)

        # User Story 08 - Birth before marriage of parents	Children should be born after marriage of parents (and not more than 9 months after their divorce)

        # User Story 09 - Birth before death of parents	Child should be born before death of mother and before 9 months after death of father

        # User Story 10 - Marriage after 14	Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old)

        # User Story 11 - No bigamy	Marriage should not occur during marriage to another spouse

        # User Story 12 - Parents not too old	Mother should be less than 60 years older than her children and father should be less than 80 years older than his children

        # User Story 13 - Siblings spacing	Birth dates of siblings should be more than 8 months apart or less than 2 days apart (twins may be born one day apart, e.g. 11:59 PM and 12:02 AM the following calendar day)

        # User Story 14 - Multiple births <= 5	No more than five siblings should be born at the same time

        # User Story 15 - Fewer than 15 siblings	There should be fewer than 15 siblings in a family

        # User Story 16 - Male last names	All male members of a family should have the same last name

        # User Story 17 - No marriages to descendants	Parents should not marry any of their descendants

        if perform_Corresponding_entries:

            errors = check_corresponding_entries(individuals_dict, families_dict)
            if errors:
                print("\n".join(errors))

        # reprinting the individuals table since it already included the ages
        if perform_include_individual_ages:
            print("Individuals table data already included the age")
            include_individual_ages(individuals)

        # print(type(individuals_dict), individuals_dict)
        # print(type(families_dict), families_dict)
        if perform_order_siblings_by_age:
            ordered_siblings = order_siblings_by_age(individuals_dict, families_dict)
            print(ordered_siblings)
            print("Ordering siblings by age Complete")
        if perform_list_large_age_differences:
            list_large_age_differences(individuals_dict, families_dict)

        individuals_t, families_t = parse_gedcom(gedcom_file_path)
        check_constraints(individuals_t, families_t)
        # User Story 35 - List Recent Births - List all people in a GEDCOM file who were born in the last 30 days
        list_recent_births(individuals_t)
        # User Story 36 - List Recent Deaths - List all people in a GEDCOM file who died in the last 30 days
        list_recent_deaths(individuals_t)
        # User Story 37 - List Recent Survivors - List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days
        list_recent_survivors(individuals_t, families_t)
        # User Story 38 - List Upcoming Birthdays - List all living people in a GEDCOM file whose birthdays occur in the next 30 days
        list_upcoming_birthdays(individuals_t)

        print("========================================\nProgram Ended Successfully")

    except FileNotFoundError:
        print(f"File '{gedcom_file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def check_corresponding_entries(individuals, families):
    """
    Check the corresponding entries between individuals and families to identify any errors.

    Parameters:
    individuals (dict): A dictionary containing information about individuals.
    families (dict): A dictionary containing information about families.

    Returns:
    list: A list of errors found during the check.
    """

    print("checking corresponding entries")
    errors = []

    # Ensure individuals and families are dictionaries
    if not isinstance(individuals, dict) or not isinstance(families, dict):
        raise TypeError("Both individuals and families must be dictionaries.")

    # Check individuals' FAMS and FAMC against families' HUSB, WIFE, and CHIL
    for ind_id, ind_data in individuals.items():
        fams = ind_data.get('FAMS', [])
        famc = ind_data.get('FAMC', [])
        for fam_id in fams:
            if fam_id not in families:
                errors.append(
                    f"Checking Corresponding Entries: ERROR: Individual {ind_id} has a FAMS link to non-existent family {fam_id}")
                continue
            fam = families.get(fam_id, {})
            if ind_id not in [fam.get('HUSB', ''), fam.get('WIFE', '')]:
                errors.append(
                    f"Checking Corresponding Entries: ERROR:  Individual {ind_id} is listed as a spouse in family {fam_id} but is not recorded as HUSB or WIFE")
        for fam_id in famc:
            if fam_id not in families:
                errors.append(
                    f"Checking Corresponding Entries: ERROR:  Individual {ind_id} has a FAMC link to non-existent family {fam_id}")
                continue
            fam = families.get(fam_id, {})
            if ind_id not in fam.get('CHIL', []):
                errors.append(
                    f"Checking Corresponding Entries: ERROR:  Individual {ind_id} is listed as a child in family {fam_id} but is not recorded as CHIL")

    # Check families' HUSB, WIFE, and CHIL against individuals' FAMS and FAMC
    for fam_id, fam_data in families.items():
        husb_id = fam_data.get('HUSB', '')
        wife_id = fam_data.get('WIFE', '')
        if husb_id and husb_id not in individuals:
            continue  # Skip if husband or wife is not in individuals dict
        if wife_id and wife_id not in individuals:
            continue
        if husb_id and fam_id not in individuals.get(husb_id, {}).get('FAMS', []):
            errors.append(
                f"Checking Corresponding Entries: ERROR:  Husband {husb_id} in family {fam_id} does not list {fam_id} in FAMS")
        if wife_id and fam_id not in individuals.get(wife_id, {}).get('FAMS', []):
            errors.append(
                f"Checking Corresponding Entries: ERROR:  Wife {wife_id} in family {fam_id} does not list {fam_id} in FAMS")
        for child_id in fam_data.get('CHIL', []):
            if child_id not in individuals or fam_id not in individuals.get(child_id, {}).get('FAMC', []):
                errors.append(
                    f"Checking Corresponding Entries: ERROR: FAMILY: Child {child_id} in family {fam_id} does not list {fam_id} in FAMC")

    print("checking corresponding entries Complete")
    return errors


def include_individual_ages(individuals):
    """
    Prints individuals' data along with their ages.

    :param individuals
    """
    individual_table = PrettyTable()
    individual_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death"]

    for individual_id, data in individuals:
        birth_date = data.get('birth', '')
        if not birth_date.strip():
            birth_date = "N/A"

        age = calculate_age(birth_date) if birth_date else "N/A"
        alive = "Yes" if not data.get('death', '') else "No"
        individual_table.add_row(
            [individual_id, data.get('name', ''), data.get('sex', ''), birth_date, age, alive, data.get('death', '')])

    print(individual_table)


def order_siblings_by_age(individuals, families):
    print("Ordering siblings by age")
    siblings_ordered_by_age = {}

    for family_id, family_data in families.items():
        # print("Family id is " + family_id)
        # print("Family data is " + str(family_data))
        siblings = family_data.get('Children', [])

        siblings_details = [individuals.get(sibling_id) for sibling_id in siblings]

        # print("Siblings details are " + str(siblings_details))
        siblings_with_birth_dates = [s for s in siblings_details if s and 'birth' in s]

        # print ("Siblings with birth dates are " + str(siblings_with_birth_dates))
        sorted_siblings = sorted(siblings_with_birth_dates, key=lambda s: calculate_age(s['birth']), reverse=True)

        # print("Sorted siblings are " + str(sorted_siblings))

        # Store the sorted siblings data directly
        siblings_ordered_by_age[family_id] = sorted_siblings
    print("Siblings ordered by age")
    return siblings_ordered_by_age


def calculate_target_age(birth_date, target_date):
    """
    Calculate the age of an individual at a specific target date.

    :param birth_date: The birth date of the individual as a datetime.datetime object.
    :param target_date: The target date (e.g., marriage date) as a datetime.datetime object.
    :return: The age of the individual at the target date.
    """
    # print("Birth date is " + str(birth_date))
    # print("Target date is " + str(target_date))
    age = target_date.year - birth_date.year - (
                (target_date.month, target_date.day) < (birth_date.month, birth_date.day))
    return age


def list_large_age_differences(individuals, families):
    """
    Lists all couples who were married when the older spouse was more than twice as old as the younger spouse.

    :param individuals: A dictionary where keys are individual IDs and values are dictionaries containing individual data.
    :param families: A dictionary where keys are family IDs and values are dictionaries containing family data.
    :return: A list of tuples, where each tuple contains the IDs of a couple that meets the criteria.
    """
    print("Listing large age differences")
    large_age_difference_couples = []

    for family_id, family_data in families.items():
        husband_id = family_data['Husband ID']
        # print("Husband id is " + husband_id)
        wife_id = family_data['Wife ID']
        # print("Wife id is " + wife_id)
        husband_birth_date = datetime.strptime(individuals[husband_id]['birth'], "%Y-%m-%d")
        # print("Husband birth date is " + str(husband_birth_date))
        wife_birth_date = datetime.strptime(individuals[wife_id]['birth'], "%Y-%m-%d")
        # print("Wife birth date is " + str(wife_birth_date))
        # print("Married is " + str(family_data['Married']))
        if not family_data['Married']:
            print(
                "list_large_age_differences: Skipping family " + family_id + " because there is no married date available to calculate age difference")
            continue
        marriage_date = datetime.strptime(family_data['Married'], "%Y-%m-%d")
        # print("Marriage date is " + str(marriage_date))

        husband_age_at_marriage = calculate_target_age(husband_birth_date, marriage_date)
        wife_age_at_marriage = calculate_target_age(wife_birth_date, marriage_date)

        # Check if the older spouse is more than twice as old as the younger spouse at the time of marriage
        if abs(husband_age_at_marriage - wife_age_at_marriage) > 2 * wife_age_at_marriage:
            large_age_difference_couples.append((husband_id, wife_id))
    print(large_age_difference_couples)
    print("Large age difference complete")
    return large_age_difference_couples


if __name__ == "__main__":
    main()
