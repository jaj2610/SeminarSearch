import re
from datetime import datetime

month_options = "|".join(['january', 'february', 'march', 'april', 'may',
                          'june', 'july', 'august', 'september', 'november',
                          'december', 'jan', 'feb', 'mar', 'apr', 'may', 'jun',
                          'jul', 'aug', 'sep', 'nov', 'dec'])
month_map = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
             'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}


def validate_month(month):
    """Return True if month is between 1 and 12.
        month should be an int"""
    return month >= 1 and month <= 12


def validate_day(day):
    """Return True if day is between 1 and 31.
        day should be an int"""
    return day >= 1 and day <= 31


def get_numerical_date(text):
    """Return the first (date,span) from text where:
        date looks like 4/5/2015 and variants
        span is the indices of the matched date in the text
        (None, None) returned if no dates found.
        (None, span) returned if non-date found in span"""

    m = re.match(
        r'.*?(' +  # Intro text
        r'(\d\d?)' +  # Month
        r'\s?[\/\-]\s?' +  # Separator 1
        r'(\d\d?)' +  # Day
        r'(\s?[\/\-]\s?)?' +  # Separator 2
        r'(\d\d(\d\d)?)?' +  # Year
        r')', text)
    # Group 1: Whole date
    # Group 2: Month String (04 or 4)
    # Group 3: Day String (05 or 5)
    # Group 4: Separator 2 (None or - or / )
    # Group 5: Year String (1992 or 92)
    # Group 6: Year String (92 or None)

    if m:
        month = int(m.group(2))
        if not validate_month(month):
            return(None, m.span())

        day = int(m.group(3))
        if not validate_day(day):
            return (None, m.span())

        year_fmt = 'Y'

        if not m.group(5):
            year = datetime.today().year
        else:
            if not m.group(6):
                year_fmt = 'y'
                
            year = m.group(5)

        return (datetime.strptime("{year}-{month}-{day}".format(year=year, month=month, day=day),
                                  "%{year_fmt}-%m-%d".format(year_fmt=year_fmt)), m.span())
    return (None, None)


def get_textual_date(text):
    """Return the first (date,span) from text where:
        date looks like April 5 1992 and variants
        span is the indices of the matched date in the text
        (None, None) returned if no dates found.
        (None, span) returned if non-date found in span"""

    m = re.match(
        r'.*?(' +  # Intro text
        r'({month_options})'.format(month_options=month_options) +  # Month
        r'\.?\s+' +  # Separator 1
        r'(\d\d?)(st|nd|rd|th)?' +  # Day
        r'(\,?\s+)?' +  # Separator 2
        r'(\d\d(\d\d)?)?' +  # Year
        r')', text, re.IGNORECASE)
    # Group 1: Whole date
    # Group 2: Month String (April or APR or apr)
    # Group 3: Day String (05 or 5)
    # Group 4: Trailing junk (th from 5th)
    # Group 5: Separator 2 (, and/or \s)
    # Group 6: Year String (1992 or 92)
    # Group 7: Year String (92 or None)

    if m:
        month_str = m.group(2).lower()
        month = month_map[month_str[:3]]

        if not validate_month(month):
            return (None, m.span())

        day = int(m.group(3))
        if not validate_day(day):
            return (None, m.span())

        year_fmt = 'Y'

        if not m.group(6):
            year = datetime.today().year
        else:
            if not m.group(7):
                year_fmt = 'y'

            year = m.group(6)

        return (datetime.strptime("{year}-{month}-{day}".format(year=year, month=month, day=day),
                                  "%{year_fmt}-%m-%d".format(year_fmt=year_fmt)), m.span())
    return (None, None)


def get_backwards_textual_date(text):
    """Return the first (date,span) from text where:
        date looks like 5th of April, 1992 and variants
        span is the indices of the matched date in the text
        (None, None) returned if no dates found.
        (None, span) returned if non-date found in span"""

    m = re.match(
        r'.*?(' +  # Intro text
        r'(\d\d?)(st|nd|rd|th)?' +  # Day
        r'\s+(of\s)?' +  # Separator 1
        r'({month_options})'.format(month_options=month_options) +  # Month
        r'(\.?\,?\s+)?' +  # Separator 2
        r'(\d\d(\d\d)?)?' +  # Year
        r')', text, re.IGNORECASE)

    # Group 1: Whole date
    # Group 2: Day String (05 or 5)
    # Group 3: Trailing junk (th from 5th)
    # Group 4: of (None or of)
    # Group 5: Month String (April or APR or apr)
    # Group 6: Separator 2 (., )
    # Group 7: Year String (1992 or 92)
    # Group 8: Year String (92 or None)
    if m:
        month_str = m.group(5).lower()
        month = month_map[month_str[:3]]

        if not validate_month(month):
            return (None, m.span())

        day = int(m.group(2))
        if not validate_day(day):
            return (None, m.span())

        year_fmt = 'Y'

        if not m.group(7):
            year = datetime.today().year
        else:
            if not m.group(8):
                year_fmt = 'y'
            year = m.group(7)

        return (datetime.strptime("{year}-{month}-{day}".format(year=year, month=month, day=day),
                                 "%{year_fmt}-%m-%d".format(year_fmt=year_fmt)), m.span())
    return (None, None)


def get_dates(text):
    """Gets all the dates in text"""
    
    dates = []
    # get_backwards_textual needs to come before get_textual
    for date_finder in [get_numerical_date, get_backwards_textual_date, get_textual_date]:
        while True:
            try:
                date, span = date_finder(text)
            except:
                break
            if span:
                text = text[:span[0]] + text[span[1]:]
            if date:
                dates.append(date)
            if not span and not date:
                break

    return dates


def test_get_dates():

    # Numerical
    assert(get_dates("04-05-1992") == [datetime(1992, 4, 5)])
    assert(get_dates("04/05/1992") == [datetime(1992, 4, 5)])
    assert(get_dates("04-05-92") == [datetime(1992, 4, 5)])
    assert(get_dates("04/05/92") == [datetime(1992, 4, 5)])
    assert(get_dates("4-05-1992") == [datetime(1992, 4, 5)])
    assert(get_dates("4-5-1992") == [datetime(1992, 4, 5)])
    assert(get_dates("04-5-1992") == [datetime(1992, 4, 5)])
    assert(get_dates("4-05-1992") == [datetime(1992, 4, 5)])
    assert(get_dates("4-5-92") == [datetime(1992, 4, 5)])
    assert(get_dates("04-5-92") == [datetime(1992, 4, 5)])
    assert(get_dates("4-05-92") == [datetime(1992, 4, 5)])
    assert(get_dates("When: 4-5-1992") == [datetime(1992, 4, 5)])
    assert(get_dates("She got a 04/10") == [datetime(datetime.today().year, 4, 10)])
    assert(get_dates("04-05-1992 and then 04-06-1992") ==
           [datetime(1992, 4, 5), datetime(1992, 4, 6)])
    assert(get_dates("13-05-1992 and then 04-06-1992") == [datetime(1992, 4, 6)])
    assert(get_dates("1-05-1992,04-06-1992") == [datetime(1992, 1, 5), datetime(1992, 4, 6)])

    # Textual
    assert(get_dates("April 5 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("APRIL 5 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("April 5, 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("Apr 5 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("APR 5 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("Apr. 5, 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("April 5 92") == [datetime(1992, 4, 5)])
    assert(get_dates("APRIL 5 92") == [datetime(1992, 4, 5)])
    assert(get_dates("April 5, 92") == [datetime(1992, 4, 5)])
    assert(get_dates("Apr 5 92") == [datetime(1992, 4, 5)])
    assert(get_dates("APR 5 92") == [datetime(1992, 4, 5)])
    assert(get_dates("Apr. 5, 92") == [datetime(1992, 4, 5)])
    assert(get_dates("April 5 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("April 5th 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("April 5th, 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("April 1st 1992") == [datetime(1992, 4, 1)])
    assert(get_dates("April 2nd 1992") == [datetime(1992, 4, 2)])
    assert(get_dates("April 3rd 1992") == [datetime(1992, 4, 3)])
    assert(get_dates("April 03 1992") == [datetime(1992, 4, 3)])
    assert(get_dates("April 3rd") == [datetime(datetime.today().year, 4, 3)])
    assert(get_dates("April 22th, 1992") == [datetime(1992, 4, 22)])

    # Backwards Textual
    assert(get_dates("5 April 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("15 April 1992") == [datetime(1992, 4, 15)])
    assert(get_dates("05 April 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("5th of April 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("5th of April, 1992") == [datetime(1992, 4, 5)])
    assert(get_dates("5th of April") == [datetime(datetime.today().year, 4, 5)])
    assert(get_dates("1st of April, 1992") == [datetime(1992, 4, 1)])
    assert(get_dates("2nd April 1992") == [datetime(1992, 4, 2)])
    assert(get_dates("3rd of April, 1992") == [datetime(1992, 4, 3)])
    assert(get_dates("22nd Apr., 1992") == [datetime(1992, 4, 22)])
    assert(get_dates("22nd Apr., 1992 and 5th of June, 2010") == [datetime(1992, 4, 22),datetime(2010,6,5)])
    assert(get_dates("The event will the the 23rd of April, 2991") == [datetime(2991, 4, 23)])
    assert(get_dates("When: 23rd of April, 2991") == [datetime(2991, 4, 23)])

    # Non-matches
    assert(get_dates("I had 23 things to do that day") == [])
    assert(get_dates("The 23rd annual volleyball match this april") == [])
    assert(get_dates("She got a 96/100") == [])
