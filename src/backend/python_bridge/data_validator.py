import re

def validate_roll(value):
    """
    Purpose: Ensure roll is a positive integer string
    Returns: (True, int) or (False, error_message)
    """
    if not str(value).isdigit() or int(value) <= 0:
        return False, "Roll number must be a positive integer"
    return True, int(value)

def validate_name(value):
    """
    Purpose: Ensure name contains only letters, spaces, hyphens
    Returns: (True, str) or (False, error_message)
    """
    value = value.strip()
    if not value:
        return False, "Name cannot be empty"
    if not re.match(r"^[A-Za-z\s\-]+$", value):
        return False, "Name must contain only letters, spaces, or hyphens"
    return True, value

def validate_contact(value):
    """
    Purpose: Ensure contact is digits only, 7-15 chars
    Returns: (True, str) or (False, error_message)
    """
    value = value.strip()
    if not value.isdigit() or not (7 <= len(value) <= 15):
        return False, "Contact must be 7-15 digits"
    return True, value

def validate_mark(value, subject="Mark"):
    """
    Purpose: Ensure mark is integer 0-100
    Returns: (True, int) or (False, error_message)
    """
    try:
        v = int(value)
        if not (0 <= v <= 100):
            return False, f"{subject} must be between 0 and 100"
        return True, v
    except ValueError:
        return False, f"{subject} must be a whole number"

def validate_date(value):
    """
    Purpose: Ensure date is YYYY-MM-DD format
    Returns: (True, str) or (False, error_message)
    """
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return False, "Date must be in YYYY-MM-DD format"
    return True, value
