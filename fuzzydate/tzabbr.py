import csv
import os
import datetime
import re
from collections import defaultdict

# helpers to translate common timezone abbreviations (eg EST, NZDT) to
# UTC offsets.

# uses time zone abbreviations from wikipedia:
# http://en.wikipedia.org/wiki/List_of_time_zone_abbreviations
# scraped via:
# https://scraperwiki.com/scrapers/time_zone_abbreviations
#
# TODO: this might be a more complete source:
#  http://www.timeanddate.com/library/abbreviations/timezones/
#
# TODO: the abbreviations are not unique (eg there are three "AST"s)
# For now, I've added a priority column to the data to make one override
# the others.
# The better option would be to a country code hint param
# to abbr_to_offset(). eg a program parsing web pages could use
# the country code of the domain name as a hint.

def _load_timezones():
    tz_data = defaultdict(list)

    offset_pat = re.compile(r'UTC(?P<hour>[+-]\d{1,2})?(?::(?P<min>\d{1,2}))?',re.I)
    def parse_offset(s):
        m = offset_pat.match(s)
        hour = m.group('hour')
        hour = int(hour) if hour is not None else 0
        min = m.group('min')
        min = int(min) if min is not None else 0

        if hour < 0:
            return datetime.timedelta(minutes=(hour*60)-min)
        else:
            return datetime.timedelta(minutes=(hour*60)+min)


    here = os.path.dirname(os.path.abspath(__file__))
    r = csv.reader(open(os.path.join(here, 'timezones.csv'), "r"))
    for row in r:
        abbr,val,pri = row[0],row[1],int(row[3])
        offset = parse_offset(val)

        abbr = abbr.lower()
        l = tz_data[abbr]
        l.append((offset,pri))
        if len(l)>1:
            l = sorted(l, key=lambda x: x[1], reverse=True)   # keep sorted by pri
        tz_data[abbr] = l
    return tz_data


_tz_abbreviations = _load_timezones()


def abbr_to_delta(tz_abbr):
    """ given a timezone abbreviation, returns an offset-from-utc (as a timedelta)

    returns None if abbreviation is not recognised.
    """
    foo = _tz_abbreviations.get(tz_abbr.lower(),None)
    if foo is None:
        return None
    else:
        # TODO: should use country code here if available, to disambiguate
        return foo[0][0]   # offset of first one

