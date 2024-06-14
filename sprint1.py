from datetime import datetime
import re

class sprint1:
    def dates_before_current_date(self, gedcom_lines):
        current_date = datetime.now()
        events = ["BIRT", "MARR", "DIV", "DEAT"]
        invalid_dates = []

        for i, line in enumerate(gedcom_lines):
            parts = line.strip().split()
            if parts and parts[0] in ["1", "2"] and parts[1] in events:
                date_line = gedcom_lines[i + 1].strip()
                date_parts = date_line.split()
                if date_parts[0] == "2" and date_parts[1] == "DATE":
                    try:
                        event_date = datetime.strptime(" ".join(date_parts[2:]), "%d %b %Y")
                        if event_date > current_date:
                            invalid_dates.append((line, date_line))
                    except ValueError:
                        continue
        return invalid_dates