"""
Template helper functions for the Flask application
"""


def na_if_none(value):
    """Return 'N/A' if value is None, otherwise return the value"""
    return value if value is not None else "N/A"


def format_number(value):
    """Format a number with commas for thousands"""
    if value is None:
        return "N/A"
    try:
        return f"{int(value):,}"
    except (ValueError, TypeError):
        return str(value)


def format_datetime(value):
    """Format a datetime object"""
    if value is None:
        return "N/A"
    try:
        return value.strftime("%Y-%m-%d %H:%M:%S")
    except AttributeError:
        return str(value)


def format_date(value):
    """Format a date object"""
    if value is None:
        return "N/A"
    try:
        return value.strftime("%Y-%m-%d")
    except AttributeError:
        return str(value)


def format_title(value, max_length=50):
    """Format a title, truncating if too long"""
    if value is None:
        return "N/A"
    if len(str(value)) > max_length:
        return str(value)[:max_length] + "..."
    return str(value)


def format_party(value):
    """Format party information"""
    if value is None or value == "":
        return "Independent"
    return str(value)


def format_support(value):
    """Format support/opposition information"""
    if value is None:
        return "N/A"
    try:
        vote_value = int(value)
        if vote_value == 1:
            return "Support"
        if vote_value == 2:
            return "Oppose"
        return "Abstain"
    except (ValueError, TypeError):
        return str(value)


def format_vote_type(value):
    """Format vote type information"""
    if value is None:
        return "N/A"
    try:
        vote_value = int(value)
        if vote_value == 1:
            return "Yea"
        if vote_value == 2:
            return "Nay"
        return "Present"
    except (ValueError, TypeError):
        return str(value)
