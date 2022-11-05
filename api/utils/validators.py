import re


# validate date format with regular expression
def validate_date(date):
    if re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return True
    return False


# validate date format with regular expression to be like 2022-11-03T23:50:53Z
def validate_iso_date(date):
    if re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", date):
        return True
    return False
