import re

# число, похожее на год
YEAR_RE = "(1\d|20)\d{2}"
# год в именованной группе
YEAR_GROUP_RE = "(?P<year>{})".format(YEAR_RE)

# тире, минусы, предлоги
DASHES = "([—–−-]|до|по|и)"

# диапазон годов: год, тире/предлог, еще один год
YEAR_RANGE_RE = re.compile(
    "(\D|^){}(\s*{}\s*)+{}(\D|$)".format(YEAR_GROUP_RE, DASHES, YEAR_RE)
)
# год с "г"
G_YEAR_RE = re.compile("(\D|^){}\s*г".format(YEAR_GROUP_RE), re.IGNORECASE)
# просто отдельный год
SIMPLE_YEAR_RE = re.compile("(\D|^){}(\D|$)".format(YEAR_GROUP_RE))


def year(text):
    # сначала найдем диапазоны - на случай "1991-1993 гг."
    # (по условию в этом случае должен использоваться первый год)
    range_match = YEAR_RANGE_RE.search(text)
    if range_match is not None:
        return (True, range_match.groupdict().get("year", None))
    # затем годы с "г"
    g_match = G_YEAR_RE.search(text)
    if g_match is not None:
        return (True, g_match.groupdict().get("year", None))
    # если ничего не нашли, то просто отдельные годы
    match = SIMPLE_YEAR_RE.search(text)
    if match is not None:
        return (False, match.groupdict().get("year", None))
    return (False, None)
