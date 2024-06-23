from datetime import datetime
import re

def parse_date_helper(date):
        try:
            return datetime.strptime(date, "%d %b %Y").date()
        except ValueError:
            return None
        
class sprint2:
    
    def divorce_before_marriage(self, gedcom_data):
        fams = {} 
        current_fam_id = None
        marriage_date = None
        divorce_date = None
        #print(gedcom_data)

        for i, line in enumerate(gedcom_data):
            parts = line.strip().split()
            #print(parts)
            if parts: 
                #print(parts[1])
                if (parts[0] == "0" and "@F" in parts[1]):
                    #print("here")
                    if (current_fam_id):
                        fams[current_fam_id] = (marriage_date, divorce_date)
                    current_fam_id = parts[1]
                    marriage_date = None
                    divorce_date = None
                elif (parts[0] == "1"):
                    if (parts[1] == "MARR"):
                        date_line = gedcom_data[i+1].strip()
                        date_parts = date_line.split()
                        if (date_parts[0] == "2" and date_parts[1] == "DATE"):
                            marriage_date = parse_date_helper(" ".join(date_parts[2:]))
                    elif (parts[1] == "DIV"):
                        date_line = gedcom_data[i+1].strip()
                        date_parts = date_line.split()
                        if(date_parts[0] == "2" and date_parts[1] == "DATE"):
                            divorce_date = parse_date_helper(" ".join(date_parts[2:]))
                            #print("div: ", divorce_date)
        #print(current_fam_id)
        #print(marriage_date)
        #print(divorce_date)
        if (current_fam_id):
            fams[current_fam_id] = (marriage_date, divorce_date)
            
        results = {} 
        #print(fams)
        for fam_id, (mar_date, div_date) in fams.items():
            if (mar_date and div_date):
                #print("m date", mar_date)
                #print(div_date)
                if(div_date < mar_date):
                    results[fam_id] = (mar_date.strftime('%d %b %Y').upper(), div_date.strftime('%d %b %Y').upper())
                #if (div_date < mar_date):
                #    print(f"Divorce before marriage in fam {fam_id}")
                #    print(f"Marriage Date: {mar_date.strftime('%d %b %Y')}")
                #    print(f"Divorce Date: {div_date.strftime('%d %b %Y')}")
        #print(results)
        return results 
    
    def death_before_marriage(self, gedcom_data):
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

    def divorce_before_death(self, gedcom_data):
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
            #print(div_date)
            
            if div_date:
                husb_death_date = inds.get(husb_id, (None, None))[1]
                wife_death_date = inds.get(wife_id, (None, None))[1]
                #print(husb_death_date)
                #print(wife_death_date)
                if (husb_death_date and div_date > husb_death_date) or (wife_death_date and div_date > wife_death_date):
                    #print("husb ddate: ", husb_death_date)
                    results[fam_id] = (div_date.strftime('%d %b %Y').upper(),
                                        husb_death_date.strftime('%d %b %Y').upper() if husb_death_date else None,
                                        wife_death_date.strftime('%d %b %Y').upper() if wife_death_date else None)
        #results {divorce date, husb death date, wife death date}
        #print(results)
        return results
    
    def over_150(self, gedcom_data):
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