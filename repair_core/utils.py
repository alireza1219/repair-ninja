"""
Repair Ninja Utilities.
"""
def priority(value: int):
    """Translates the priority value into a human-readable string.

    Args:
        value (int): Priority Value

    Raises:
        ValueError: Priority value is not between 0 and 10

    Returns:
        _type_: str
    """
    if not 0 <= value <= 10:
        raise ValueError("Priority value must be between 0 and 10")

    PRIORITY_DICT = {
        0: 'Highest',
        1: 'Very High',
        2: 'High',
        3: 'Above Average',
        4: 'Average',
        5: 'Below Average',
        6: 'Low',
        7: 'Very Low',
        8: 'Lowest',
        9: 'Extremely Low',
        10: 'Not Specified'
    }

    return PRIORITY_DICT[value]
