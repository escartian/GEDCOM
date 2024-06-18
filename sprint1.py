from datetime import datetime
import re

class sprint1:
    def dates_before_current_date(self, gedcom_lines):
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

        print (invalid_dates)
        return invalid_dates
        
    def birth_before_marriage(self, gedcom_lines):
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
            print(results)
        

    def birth_before_death(self, gedcom_lines):
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