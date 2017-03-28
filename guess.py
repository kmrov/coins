import re

# a year-like number
YEAR_RE = "(1\d|20)\d{2}"
# a year-like number in named group
YEAR_GROUP_RE = "(?P<year>{})".format(YEAR_RE)

# dashes etc.
DASHES = "([—–−-]|до|по|и)"

# year range: year, then dash, then another year
YEAR_RANGE_RE = re.compile(
    "(\D|^){}(\s*{}\s*)+{}(\D|$)".format(YEAR_GROUP_RE, DASHES, YEAR_RE)
)
# year with "г"
G_YEAR_RE = re.compile("(\D|^){}\s*г".format(YEAR_GROUP_RE), re.IGNORECASE)
# just a year inside other text
SIMPLE_YEAR_RE = re.compile("(\D|^){}(\D|$)".format(YEAR_GROUP_RE))


def get_year(match):
    try:
        y = int(match.groupdict().get("year", None))
        if 1000 < y < 2018:
            return y
        else:
            return None
    except ValueError:
        return None


def year(text):
    match = SIMPLE_YEAR_RE.search(text)
    if match is not None:
        s_year = get_year(match)
        if s_year is not None:
            return s_year
    return None


def year_fuzzy(text):
    # first we search for ranges: by task we should
    # use the first year in this case
    range_match = YEAR_RANGE_RE.search(text)
    if range_match is not None:
        range_year = get_year(range_match)
        if range_year is not None:
            return (True, range_year)
    # then years with "г"
    g_match = G_YEAR_RE.search(text)
    if g_match is not None:
        g_year = get_year(g_match)
        if g_year is not None:
            return (True, g_year)
    # finally, just year-like numbers
    match = SIMPLE_YEAR_RE.search(text)
    if match is not None:
        s_year = get_year(match)
        if s_year is not None:
            return (False, s_year)
    return (False, None)
