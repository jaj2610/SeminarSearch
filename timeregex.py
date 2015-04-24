import re
from datetime import datetime


def validate_hour(hour):
    return hour >= 0 and hour <= 23


def validate_minute(minute):
    return minute >= 0 and minute <= 59


def get_time(text):
    """Get first time from text, and return index of that time"""
    m = re.match(r'.*?(' +
                 r'(\d\d?)' +  # Hour
                 r'\:\.?\s?' +  # Separator
                 r'(\d\d)' +  # Minutes
                 r'(\s?[ap]\s?\.?m\s?\.?)?' +  # am or pm
                 r')', text, re.IGNORECASE)

    # Group 1: Whole Time Expression
    # Group 2: Hour
    # Group 3: Minutes
    # Group 4: pm or am or
    if m:
        hour = int(m.group(2))
        if not validate_hour(hour):
            return (None, m.span())

        minute = int(m.group(3))
        if not validate_minute(minute):
            return (None, m.span())

        if m.group(4):
            ampm = m.group(4).lower()
            if "p" in ampm:
                if hour < 12:
                    hour += 12

        return (datetime(1900,1,1,hour,minute), m.span())
    return (None, None)


def get_times(text):

    times = []

    while True:
        time, span = get_time(text)
        if span:
            text = text[:span[0]] + text[span[1]:]
        if time:
            times.append(time)
        if not span and not time:
            return times


def test_get_times():
    assert(get_times('12:00 pm') == [datetime(1900, 1, 1, 12, 0)])
    assert(get_times('4:00 P.M') == [datetime(1900, 1, 1, 16, 0)])
    assert(get_times('8:15 am') == [datetime(1900, 1, 1, 8, 15)])
    assert(get_times('Something at 11:15am') == [datetime(1900, 1, 1, 11, 15)])
    assert(get_times('Somethings at 11:15am and 12:36pm') ==
           [datetime(1900, 1, 1, 11, 15), datetime(1900, 1, 1, 12, 36)])
    assert(get_times('Something on 12/13/14 - 7:45am') == [datetime(1900, 1, 1, 7, 45)])
    assert(get_times('Something on 12/13/14 @ 7:45pm') == [datetime(1900, 1, 1, 19, 45)])

    assert(get_times('Nothing to see here') == [])
