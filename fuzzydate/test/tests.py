from fuzzydate import parse_datetime, parse_date, parse_time, fuzzydate
import unittest
import datetime


class Tests(unittest.TestCase):

    examples_from_the_wild = [
        # timestring, expected result in UTC
        ("2010-04-02T12:35:44+00:00", (2010,4,2,12,35,44)),#(iso8601, bbc blogs)
        ("2008-03-10 13:21:36 GMT", (2008,3,10, 13,21,36)),  #(technorati api)
        ("9 Sep 2009 12.33", (2009,9,9,12,33,0)), #(heraldscotland blogs)
        ("May 25 2010 3:34PM", (2010,5,25,15,34,0)), #(thetimes.co.uk)
        ("Thursday August 21 2008 10:42 am", (2008,8,21,10,42,0)), #(guardian blogs in their new cms)
        ('Tuesday October 14 2008 00.01 BST', (2008,10,13,23,1,0)), #(Guardian blogs in their new cms)
        ('Tuesday 16 December 2008 16.23 GMT', (2008,12,16,16,23,0)), #(Guardian blogs in their new cms)
        ("3:19pm on Tue 29 Jan 08", (2008,1,29,15,19,0)), #(herald blogs)
        ("2007/03/18 10:59:02", (2007,3,18,10,59,2)),
        ("Mar 3, 2007 12:00 AM", (2007,3,3,0,0,0)),
        ("Jul 21, 08 10:00 AM", (2008,7,21,10,0,0)), #(mirror blogs)
        ("09-Apr-2007 00:00", (2007,4,9,0,0,0)), #(times, sundaytimes)
        ("4:48PM GMT 22/02/2008", (2008,2,22,16,48,0)), #(telegraph html articles)
        ("09-Apr-07 00:00", (2007,4,9,0,0,0)), #(scotsman)
        ("Friday    August    11, 2006", (2006,8,11,0,0,0)), #(express, guardian/observer)
        ("26 May 2007, 02:10:36 BST", (2007,5,26,1,10,36)), #(newsoftheworld)
        ("2:43pm BST 16/04/2007", (2007,4,16,13,43,0)), #(telegraph, after munging)
        ("20:12pm 23rd November 2007", (2007,11,23,20,12,0)), #(dailymail)
#TODO        ("2:42 PM on 22nd May 2008", (2008,5,22,14,42,0)), #(dailymail)
        ("February 10 2008 22:05", (2008,2,10,22,5,0)), #(ft)
#        ("22 Oct 2007, #(weird non-ascii characters) at(weird non-ascii characters)11:23", (2007,10,22,11,23,0)), #(telegraph blogs OLD!)
        ('Feb 2, 2009 at 17:01:09', (2009,2,2,17,1,9)), #(telegraph blogs)
        ("18 Oct 07, 04:50 PM", (2007,10,18,16,50,0)), #(BBC blogs)
        ("02 August 2007  1:21 PM", (2007,8,2,13,21,0)), #(Daily Mail blogs)
        ('October 22, 2007  5:31 PM', (2007,10,22,17,31,0)), #(old Guardian blogs, ft blogs)
        ('October 15, 2007', (2007,10,15,0,0,0)), #(Times blogs)
        ('February 12 2008', (2008,2,12,0,0,0)), #(Herald)
        ('Monday, 22 October 2007', (2007,10,22,0,0,0)), #(Independent blogs, Sun (page date))
        ('22 October 2007', (2007,10,22,0,0,0)), #(Sky News blogs)
        ('11 Dec 2007', (2007,12,11,0,0,0)), #(Sun (article date))
        ('12 February 2008', (2008,2,12,0,0,0)), #(scotsman)
        ('03/09/2007', (2007,9,3,0,0,0)), #(Sky News blogs, mirror)
        ('Tuesday, 21 January, 2003, 15:29 GMT', (2003,1,21,15,29,0)), #(historical bbcnews)
        ('2003/01/21 15:29:49', (2003,1,21,15,29,49)), #(historical bbcnews (meta tag))
        ('2010-07-01', (2010,7,1,0,0,0)),
        ('2010/07/01', (2010,7,1,0,0,0)),
        ('Feb 20th, 2000', (2000,2,20,0,0,0)),
        ('May 2008', (2008,5,1,0,0,0)),
        ('Monday, May. 17, 2010', (2010,5,17,0,0,0)),   # (time.com)
        ('Thu Aug 25 10:46:55 BST 2011', (2011,8,25,9,46,55)), # (www.yorkshireeveningpost.co.uk)

        #
        ('September, 26th 2011 by Christo Hall', (2011,9,26,0,0,0)),    # (www.thenewwolf.co.uk)
        ('Monday 30 July 2012 08.38 BST', (2012,7,30, 7,38,0)),     # (guardian.co.uk)

        # TODO: NZT isn't a real timezone...
    #    ("Thursday April 7, 2011 8:56 PM NZT", (2011,4,7,8,56,00)),    # nz herald

        # some that should fail!
#        ('50.50', None),
#        ('13:01pm', None),
#        ('01:62pm', None),
        # TODO: should reject these: (but day is just ignored)
#        ('32nd dec 2010', None),
    ]

    # these should fail
    bad_examples = [
        '50.50',        # should just be ignored

        # should raise range exceptions
        '13:01pm',
        '01:62pm',
    ]

    def setUp(self):
        pass

    def testExamplesFromWild(self):
        filler = fuzzydate(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

        for foo in self.examples_from_the_wild:
            fuzzy = parse_datetime(foo[0])
            got = fuzzy.datetime(filler)
            if foo[1] is not None:
                expected = datetime.datetime(*foo[1])
            else:
                expected = None

            self.assertEqual(got,expected, "'%s': expected '%s', got '%s')" % (foo[0],expected,got))


    def testSpans(self):
        got,span = parse_date('blah blah blah wibble foo, may 25th, 2011 some more crap here')
        self.assertEqual(span,(27,41))
 
        got,span = parse_date('wibble 25-01-2011 pibble')
        self.assertEqual(span,(7,17))

    def testEq(self):
        b1 = fuzzydate()
        b2 = fuzzydate()
        a1 = fuzzydate(2001,1,1, 1,1,1, 0, None)
        a2 = fuzzydate(2001,1,1, 1,1,1, 0, None)
        self.assertTrue(b1==b2)
        self.assertTrue(a1==a2)
        self.assertFalse(a1==b1)


    def testMerge(self):
        blank = fuzzydate()
        a = fuzzydate(2001,1,1, 1,1,1, 0, None)
        b = fuzzydate(2002,2,2, 2,2,2, 0, None)

        self.assertTrue(fuzzydate.merge(blank,a) == a)
        self.assertTrue(fuzzydate.merge(a,blank) == a)
        self.assertTrue(fuzzydate.merge(a,b) == b)


 
if __name__ == "__main__":
    unittest.main()
 

