# -*- coding: utf-8 -*-

import re
import datetime

import tzabbr


class fuzzydate:
    """ holder class for a datetime which can have missing fields """
    def __init__(self, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None, tzname=None):
        self.year=year
        self.month=month
        self.day=day
        self.hour=hour
        self.minute=minute
        self.second=second
        self.microsecond=microsecond
        self.tzname=tzname



    def empty_date(self):
        return self.year is None and self.month is None and self.day is None

    def empty_time(self):
        return self.hour is None and self.minute is None and self.second is None and self.microsecond is None and self.tzname is None

    def empty(self):
        return self.empty_date() and self.empty_time()

    def date(self, filler=None):
        if filler is not None:
            fz = fuzzydate.merge(filler,self)
        else:
            fz = self

        assert fz.year is not None
        assert fz.month is not None
        assert fz.day is not None

        return datetime.date(fz.year, fz.month, fz.day)

    def time(self, filler=None):
        if filler is not None:
            fz = fuzzydate.merge(filler,self)
        else:
            fz = self
        # TODO: TIMEZONES?
        return datetime.time(fz.hour, fz.minute, fz.second, fz.microsecond)


    def datetime(self, filler=None):

        if filler is not None:
            fz = fuzzydate.merge(filler,self)
        else:
            fz = self

        dt = datetime.datetime.combine(fz.date(), fz.time())
        if fz.tzname is not None:
            # convert to utc
            delta = tzabbr.abbr_to_delta(fz.tzname)
            if delta is None:   # TODO: Think this through properly
                return None
            dt -= delta
        return dt


    def __repr__(self):
        return "fuzzydate(year=%s, month=%s, day=%s, hour=%s, minute=%s,second=%s, microsecond=%s, tzname=%s)" %(self.year,self.month,self.day, self.hour,self.minute, self.second, self.microsecond, self.tzname)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @classmethod
    def merge(cls, *args):
        """ merge fuzzydates together

        Later args overwrite earlier ones.
        """
        fd = fuzzydate()
        for a in args:
            fd.year = fd.year if a.year is None else a.year
            fd.month = fd.month if a.month is None else a.month
            fd.day = fd.day if a.day is None else a.day
            fd.hour = fd.hour if a.hour is None else a.hour
            fd.minute = fd.minute if a.minute is None else a.minute
            fd.second = fd.second if a.second is None else a.second
            fd.microsecond = fd.microsecond if a.microsecond is None else a.microsecond
            fd.tzname = fd.tzname if a.tzname is None else a.tzname
        return fd


# order is important(ish) - want to match as much of the string as we can
date_crackers = [

    #"Tuesday 16 December 2008"
    #"Tue 29 Jan 08"
    #"Monday, 22 October 2007"
    #"Tuesday, 21st January, 2003"
    r'(?P<dayname>\w{3,})[.,\s]+(?P<day>\d{1,2})(?:st|nd|rd|th)?\s+(?P<month>\w{3,})[.,\s]+(?P<year>(\d{4})|(\d{2}))',

    # "Friday    August    11, 2006"
    # "Tuesday October 14 2008"
    # "Thursday August 21 2008"
    #"Monday, May. 17, 2010"
    r'(?P<dayname>\w{3,})[.,\s]+(?P<month>\w{3,})[.,\s]+(?P<day>\d{1,2})(?:st|nd|rd|th)?[.,\s]+(?P<year>(\d{4})|(\d{2}))',

    # "9 Sep 2009", "09 Sep, 2009", "01 May 10"
    # "23rd November 2007", "22nd May 2008"
    r'(?P<day>\d{1,2})(?:st|nd|rd|th)?\s+(?P<month>\w{3,})[.,\s]+(?P<year>(\d{4})|(\d{2}))',
    # "Mar 3, 2007", "Jul 21, 08", "May 25 2010", "May 25th 2010", "February 10 2008"
    r'(?P<month>\w{3,})[.,\s]+(?P<day>\d{1,2})(?:st|nd|rd|th)?[.,\s]+(?P<year>(\d{4})|(\d{2}))',

    # "2010-04-02"
    r'(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})',
    # "2007/03/18"
    r'(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})',
    # "22/02/2008"
    # "22-02-2008"
    # "22.02.2008"
    r'(?P<day>\d{1,2})[/.-](?P<month>\d{1,2})[/.-](?P<year>\d{4})',
    # "09-Apr-2007", "09-Apr-07"
    r'(?P<day>\d{1,2})-(?P<month>\w{3,})-(?P<year>(\d{4})|(\d{2}))',


    # dd-mm-yy
    r'(?P<day>\d{1,2})-(?P<month>\d{1,2})-(?P<year>\d{2})',
    # dd/mm/yy
    r'(?P<day>\d{1,2})/(?P<month>\d{1,2})/(?P<year>\d{2})',
    # dd.mm.yy
    r'(?P<day>\d{1,2})[.](?P<month>\d{1,2})[.](?P<year>\d{2})',

    # TODO:
    # mm/dd/yy
    # dd.mm.yy
    # etc...
    # YYYYMMDD

    # TODO:
    # year/month only

    # "May/June 2011" (common for publications) - just use second month
    r'(?P<cruftmonth>\w{3,})/(?P<month>\w{3,})\s+(?P<year>\d{4})',

    # "May 2011"
    r'(?P<month>\w{3,})\s+(?P<year>\d{4})',
]

date_crackers = [re.compile(pat,re.UNICODE|re.IGNORECASE) for pat in date_crackers]

dayname_lookup = {
    'mon': 'mon', 'monday': 'mon',
    'tue': 'tue', 'tuesday': 'tue',
    'wed': 'wed', 'wednesday': 'wed',
    'thu': 'thu', 'thursday': 'thu',
    'fri': 'fri', 'friday': 'fri',
    'sat': 'sat', 'saturday': 'sat',
    'sun': 'sun', 'sunday': 'sun',
    # es
    'lunes': 'mon',
    'martes': 'tue',
    'miércoles': 'wed',
    'jueves': 'thu',
    'viernes': 'fri',
    'sábado': 'sat',
    'domingo': 'sun',
}


month_lookup = {
    '01': 1, '1':1, 'jan': 1, 'january': 1,
    '02': 2, '2':2, 'feb': 2, 'february': 2,
    '03': 3, '3':3, 'mar': 3, 'march': 3,
    '04': 4, '4':4, 'apr': 4, 'april': 4,
    '05': 5, '5':5, 'may': 5, 'may': 5,
    '06': 6, '6':6, 'jun': 6, 'june': 6,
    '07': 7, '7':7, 'jul': 7, 'july': 7,
    '08': 8, '8':8, 'aug': 8, 'august': 8,
    '09': 9, '9':9, 'sep': 9, 'september': 9,
    '10': 10, '10':10, 'oct': 10, 'october': 10,
    '11': 11, '11':11, 'nov': 11, 'november': 11,
    '12': 12, '12':12, 'dec': 12, 'december': 12,
    # es
    'enero': 1,
    'febrero': 2,
    'marzo': 3,
    'abril': 4,
    'mayo': 5,
    'junio': 6,
    'julio': 7,
    'agosto': 8,
    'septiembre': 9,
    'octubre': 10,
    'noviembre': 11,
    'diciembre': 12,
}


# "BST" ,"+02:00", "+02"
tz_pat = r'(?P<tz>Z|[A-Z]{2,10}|(([-+])(\d{2})((:?)(\d{2}))?))'
ampm_pat = r'(?:(?P<am>am)|(?P<pm>pm))'

time_crackers = [
    #4:48PM GMT
    r'(?P<hour>\d{1,2})[:.](?P<min>\d{2})(?:[:.](?P<sec>\d{2}))?\s*' + ampm_pat + r'\s*' + tz_pat,
    #3:34PM
    #10:42 am
    r'(?P<hour>\d{1,2})[:.](?P<min>\d{2})(?:[:.](?P<sec>\d{2}))?\s*' + ampm_pat,
    #13:21:36 GMT
    #15:29 GMT
    #12:35:44+00:00
    #00.01 BST
    r'(?P<hour>\d{1,2})[:.](?P<min>\d{2})(?:[:.](?P<sec>\d{2}))?\s*' + tz_pat,
    #12.33
    #14:21
    # TODO: BUG: this'll also pick up time from "30.25.2011"!
    r'(?P<hour>\d{1,2})[:.](?P<min>\d{2})(?:[:.](?P<sec>\d{2}))?\s*',

    # TODO: add support for microseconds?
]
time_crackers = [re.compile(pat,re.UNICODE|re.IGNORECASE) for pat in time_crackers]


def parse_date(s):
    for c in date_crackers:
        m = c.search(s)
        if not m:
            continue

        g = m.groupdict()

        year,month,day = (None,None,None)

        if 'year' in g:
            year = int(g['year'])
            if year < 100:
                year = year+2000

        if 'month' in g:
            month = month_lookup.get(g['month'].lower(),None)
            if month is None:
                continue    # not a valid month name (or number)

            # special case to handle "Jan/Feb 2010"...
            # we'll make sure the first month is valid, then ignore it
            if 'cruftmonth' in g:
                cruftmonth = month_lookup.get(g['month'].lower(),None)
                if cruftmonth is None:
                    continue    # not a valid month name (or number)

        if 'dayname' in g:
            dayname = dayname_lookup.get(g['dayname'].lower(),None)
            if dayname is None:
                continue

        if 'day' in g:
            day = int(g['day'])
            if day<1 or day>31:    # TODO: should take month into account
                continue

        if year is not None or month is not None or day is not None:
            return (fuzzydate(year,month,day),m.span())

    return (fuzzydate(),None)



def parse_time(s):
    for cracker in time_crackers:
        m = cracker.search(s)
        if not m:
            continue
        g = m.groupdict()

        hour,minute,second,microsecond,tzname = (None,None,None,None,None)

        if g.get('hour', None) is not None:
            hour = int(g['hour'])

            # convert to 24 hour time
            # if no am/pm, assume 24hr
            if g.get('pm',None) is not None and hour>=1 and hour <=11:
                hour = hour + 12
            if g.get('am',None) is not None and hour==12:
                hour = hour - 12

            if hour<0 or hour>23:
                continue

        if g.get('min', None) is not None:
            minute = int(g['min'])
            if minute<0 or minute>59:
                continue

        if g.get('sec', None) is not None:
            second = int(g['sec'])
            if second<0 or second>59:
                continue

        tzname = g.get('tz',None)
        if tzname is not None:
            if tzabbr.abbr_to_delta(tzname) is None:
                continue    # not a recognised TZ

        if hour is not None or min is not None or sec is not None:
            return (fuzzydate(hour=hour,minute=minute,second=second,microsecond=microsecond,tzname=tzname),m.span())

    return (fuzzydate(),None)


def parse_datetime(s):
    # TODO: include ',', 'T', 'at', 'on' between  date and time in the matched span...

    time,timespan = parse_time(s)
    if timespan:
        # just to make sure time doesn't get picked up again as date... (bad news as hour can look like year!)
        s = s[:timespan[0]] + s[timespan[1]:]

    date,datespan = parse_date(s)
#    if datespan:
#        # just to make sure date doesn't get picked up again as time...
#        s = s[:datespan[0]] + s[datespan[1]:]

    fd = fuzzydate.merge(date,time)
    return fd







