import datetime
import re

def is_valid_integer(input_string):
    """
    Validate if the input string is a valid integer.
    
    Args:
        input_string (str): The string to validate
    
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r"^-?\d+$"
    return bool(re.match(pattern, input_string))

def is_valid_string(input_string):
    """
    Validate if the input string contains only letters, numbers, spaces, hyphens, and apostrophes.
    
    Args:
        input_string (str): The string to validate
    
    Returns:
        bool: True if valid, False otherwise
    """

    pattern = r"^[A-Za-z0-9\s\-\']+$"
    return bool(re.match(pattern, input_string))

def is_valid_date(date_string, format="%Y-%m-%d"):
    """
    Validate if the input string is a valid date in the specified format.
    Default format is YYYY-MM-DD (e.g., 2025-09-09).
    
    Args:
        date_string (str): The date string to validate
        format (str): The expected date format (default: %Y-%m-%d)
    
    Returns:
        bool: True if valid, False otherwise
    """
    # Check if the string matches the expected format using regex
    if format == "%Y-%m-%d":
        pattern = r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$'
        if not re.match(pattern, date_string):
            return False
    
    # Try to parse the date
    try:
        datetime.datetime.strptime(date_string, format)
        return True
    except ValueError:
        return False
