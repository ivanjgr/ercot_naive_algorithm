from datetime import datetime, date

def get_texas_season(input_date=None):
    """
    Determine the season for a date in Texas, accounting for its unique climate.

    Args:
        input_date (datetime or date, optional): The date to determine the season for.
                                                 Defaults to today's date if not provided.

    Returns:
        str: The season specific to Texas
    """
    # Use today's date if no date is provided
    if input_date is None:
        input_date = date.today()

    # Ensure we're working with a date object
    if isinstance(input_date, datetime):
        input_date = input_date.date()

    month = input_date.month

    # Texas-specific seasonal definitions
    texas_seasons = {
        # Early Winter (cooler, but not deep winter)
        (11, 12, 1): 'Early Winter',

        # Winter (January-February)
        (2,): 'Winter',

        # Early Spring (March-April, unpredictable weather)
        (3, 4): 'Early Spring',

        # Late Spring (May, getting hot)
        (5,): 'Late Spring',

        # Summer (June-August, intense heat)
        (6, 7, 8): 'Summer',

        # Late Summer/Early Fall (September, still very hot)
        (9,): 'Late Summer',

        # Fall (October-early November, pleasant)
        (10, 11): 'Fall'
    }

    # Find the matching season
    for season_months, season_name in texas_seasons.items():
        if month in season_months:
            return season_name

    # Fallback (though this should never happen with the current mapping)
    return 'Unknown'

# Example usage
if __name__ == "__main__":
    # Test dates across different Texas seasons
    test_dates = [
        date(2024, 1, 15),    # Early Winter
        date(2024, 2, 15),    # Winter
        date(2024, 3, 20),    # Early Spring
        date(2024, 4, 15),    # Early Spring
        date(2024, 5, 15),    # Late Spring
        date(2024, 7, 4),     # Summer
        date(2024, 9, 1),     # Late Summer
        date(2024, 10, 31),   # Fall
        date(2024, 11, 15)    # Early Winter
    ]

    for test_date in test_dates:
        print(f"{test_date}: {get_texas_season(test_date)}")