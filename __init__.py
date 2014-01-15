# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import pytz
from functools import wraps
from time import time
from decimal import Decimal
import decimal
from decimal import InvalidOperation
import random
import string
import re
from urlparse import urlparse
from django.core.validators import email_re

#-----libs for write_pdf
#import cgi
#import StringIO
#from django.template.loader import get_template
#from xhtml2pdf import pisa


def get_hour_from_datetime(datetime_input):
    hour_datetime = datetime(year=datetime_input.year,
                             month=datetime_input.month,
                             day=datetime_input.day,
                             hour=datetime_input.hour,
                             tzinfo=datetime_input.tzinfo)

    return hour_datetime


def get_week_start_datetime_end_datetime_tuple(
        year,
        month,
        week
):
    """gets the first and the last day of a given number of week of month

    :param year: integer 4 digits
    :param month: integer 1 or 2 digits
    :param week: integer 1 or 2 digits
    :return: tuple of the first and the last day datetime objects

    >>> get_week_start_datetime_end_datetime_tuple(2013, 01, 01)
    datetime.datetime(2012, 12, 31, 0, 0), datetime.datetime(2013, 1, 7, 0, 0)
    >>> get_week_start_datetime_end_datetime_tuple(2013, 03, 01)
    datetime.datetime(2013, 02, 25, 0, 0), datetime.datetime(2013, 1, 4, 0, 0)

    """
    first_day_of_month = datetime(year=year, month=month, day=1)
    first_day_of_first_week = first_day_of_month - timedelta(
        days=first_day_of_month.weekday())
    week_delta = timedelta(weeks=1)
    week_number = 1
    first_day_of_week = first_day_of_first_week
    while (first_day_of_week + week_delta).year <= year and\
          (first_day_of_week + week_delta).month <= month and\
          week_number < week:

        week_number += 1
        first_day_of_week += week_delta

    week_start = first_day_of_week.replace(hour=0,
                                           minute=0,
                                           second=0)

    week_end = week_start + week_delta
    return week_start, week_end


def get_week_of_month_from_datetime(datetime_variable):
    """Get the week number of the month for a datetime

    :param datetime_variable: the date
    :returns: the week number (int)
    """
    first_day_of_month = datetime(year=datetime_variable.year,
        month=datetime_variable.month, day=1)
    first_day_first_week = first_day_of_month - timedelta(
        days=first_day_of_month.weekday())
    week_delta = timedelta(weeks = 1)
    datetime_next = first_day_first_week + week_delta
    week_number = 1
    while datetime_next <= datetime_variable:
        week_number += 1
        datetime_next += week_delta

    return week_number


#noinspection PyUnusedLocal
def random_string_generator(size=6,
                            chars=string.ascii_uppercase + string.digits):
    """Random String Generator

    :param size: longitud de la cadena (default 6)
    :param chars: caracteres de entre los que generara la cadena
                  (default [A-Z0-9])
    :return: generated random string
    >>> random_string_generator()
    'G5G74W'
    >>> random_string_generator(3, "6793YUIO")
    'Y3U'

    """
    return ''.join(random.choice(chars) for x in range(size))


#def write_pdf(template_src, context_dict):
#    """
#    genera un pdf, recibe la ruta del template y el context para el template
#    """
#    template = get_template(template_src)
#    context = contexto(context_dict)
#    html  = template.render(context)
#    result = StringIO.StringIO()
#    pdf = pisa.pisaDocument(StringIO.StringIO(
#        html.encode("ISO-8859-1")), result)
#    if not pdf.err:
#        return HttpResponse(result.getvalue(), mimetype='application/pdf')
#    return HttpResponse(
#        "Los Gremlin's se comieron tu PDF! %s" % cgi.escape(html))

def validate_url(url):
    """Checks if a url is valid

    :param url: string object, the url to validate
    :return: boolean, True if valid, False if not
    >>> validate_url("http://google.com")
    True
    >>> validate_url("asieselabarrote")
    False

    """
    o = urlparse(url)
    if o.netloc != '':
        return True
    else:
        return False


def validate_username(strng):
    """Checks for a valid username (alphanumeric with underscores/hypens/dots)

    :param strng: string object, the string to validate
    :return: boolean, True if valid, False if not
    >>> validate_string("http://google.com")
    False
    >>> validate_string("así.es_el-abarrote01")
    True
    """
    if not isinstance(strng, str) and not isinstance(strng, unicode):
        return False
    if isinstance(strng, str):
        strng = unicode(strng.decode("utf-8"))
    pattern = re.compile(r'[^\w\s\-\._"]', re.UNICODE)

    string_arr = strng.split(" ")
    for i in string_arr:
        if i == "" or pattern.search(i):
            return False
    return True


def validate_string(strng):
    """Checks for non word chars in a unicode string

    :param strng: string object, the string to validate
    :return: boolean, True if valid, False if not
    >>> validate_string("http://google.com")
    False
    >>> validate_string("así es el abarrote")
    True

    """
    if not isinstance(strng, str) and not isinstance(strng, unicode):
        return False
    if isinstance(strng, str):
        strng = unicode(strng.decode("utf-8"))
    pattern = re.compile(r'[^\w\s\-\'\."]', re.UNICODE)
    string_arr = strng.split(" ")
    for i in string_arr:
        if i == "" or pattern.search(i):
            return False
    return True


def unique_from_array(array):
    """takes an array and removes duplicates

    :param array: array object, the array to evaluate
    :returns: an array with unique values

    >>> unique_from_array([1, 23, 32, 1, 23, 44, 2, 1])
    [1, 23, 32, 44, 2]
    >>> unique_from_array(["uno", "dos", "uno", 2, 1])
    ["uno", "dos", 2, 1]

    """
    u = []
    for x in array:
        if x not in u:
            if x != '':
                u.append(x)

    return u


def get_post_data(post):
    """cleans the post dictionary data, turns the strings into str(),
    and the numbers into long or float

    :param post: dictionary
    :return: a dict with the same keys

    """
    datos_post = {}
    for postdata in post:
        dato = post[str(postdata)].strip()

        try:
            dato = Decimal(dato)
        except InvalidOperation:
            datos_post[str(postdata)] = post[str(postdata)]
        else:
            #si es un numero entero
            if dato%1 == 0:
                datos_post[str(postdata)] = long(dato)
            else:
                #si tiene decimales
                datos_post[str(postdata)] = float(dato)
    return datos_post


def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money( or number ) formatted string.

    :param places:  required number of places after the decimal point
    :param curr:    optional currency symbol before the sign (may be blank)
    :param sep:     optional grouping separator (comma, period, space, or blank)
    :param dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    :param pos:     optional sign for positive numbers: '+', space or blank
    :param neg:     optional sign for negative numbers: '-', '(', space or blank
    :param trailneg:optional trailing minus indicator:  '-', ')', space or blank
    :return: formatted string

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<0.02>'

    """
    q = Decimal(10) ** -places      # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    result = []
    digits = map(str, digits)
    build, next_ = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        build(next_() if digits else '0')
    build(dp)
    if not digits:
        build('0')
    i = 0
    while digits:
        build(next_())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    build(neg if sign else pos)
    return ''.join(reversed(result))


def is_number(number):
    """ check if a string is number

    :param number: string to evaluate
    :return: false if not numeric, else returns digit(long or float)

    >>> is_number("233.33")
    233.33
    >>> is_number("233")
    233L
    >>> is_number("foobar")
    False

    """
    try:
        dato = Decimal(number)
    except decimal.InvalidOperation:
        return False
    else:
        #si es un numero entero
        if dato % 1 == 0:
            dato = long(dato)
        else:
            #si tiene decimales
            dato = float(dato)
        return dato


def is_valid_email(email):
    """ check if a string is a valid email address
    django dependant

    :param email: - the string to evaluate
    :return: boolean, True if valid, False if not

    >>> is_valid_email("hector@wime.com.mx")
    True
    >>> is_valid_email("foobar")
    False
    """
    return True if email_re.match(email) else False


def scale_dimensions(width, height, longest_side):
    """ Calculates image ratio given a longest side
    returns a tupple with ajusted width, height

    :param width:  integer, the current width of the image
    :param height:  integer, the current height of the image
    :param longest_side:   the longest side of the resized image
    :return: resized width, height

    >>> scale_dimensions(680, 480, 340)
    340, 240
    >>> scale_dimensions(480, 680, 340)
    240, 340

    """
    if width > height:
        if width > longest_side:
            ratio = longest_side*1./width
            return int(width*ratio), int(height*ratio)
    elif height > longest_side:
        ratio = longest_side*1./height
        return int(width*ratio), int(height*ratio)
    return width, height


def convert_to_utc(time_v, tz):
    """ Convert a time in a tz timezone to a utc time

    :param time_v: time object in utc time
    :param tz: the timezone to convert the time to utc
    :return: adjusted time, offset hours
    """

    now_dt = datetime.utcnow()
    #get a date object
    date_dt = now_dt.date()
    #combine the current date object with our given time object
    dt = datetime.combine(date_dt, time_v)
    #get an timezone object for the source timezone
    src_tz = pytz.timezone(str(tz))
    #stamp the source datetime object with the src timezone
    src_dt = src_tz.localize(dt)
    #get the offset from utc to given timezone
    offset = str(int(src_dt.strftime("%z"))).rstrip('0')
    #convert the source datetime object to
    utc_dt = src_dt.astimezone(pytz.utc)
    #return the converted time and the offset in integer format
    return utc_dt.time(), int(offset)


def convert_from_utc(time_v, tz):
    """ Convert a utc time to a tz timezone time

    :param time_v: time object in utc time
    :param tz: the timezone to convert the time to
    :return: adjusted time
    """
    now_dt = datetime.now()
    date = now_dt.date()
    dt = datetime.combine(date, time_v)
    dest = pytz.timezone(str(tz))
    dt = dt.replace(tzinfo=pytz.utc)
    dest_dt = dt.astimezone(dest)
    return dest_dt.time()


def timed(f):
    """Measures the time(seconds) a f function takes to return a result

    :param f: function
    :return: the result of the function
    """

    @wraps(f)
    def wrapper(*args, **kwds):
        start = time()
        result = f(*args, **kwds)
        elapsed = time() - start
        print "%s took %d seconds to finish" % (f.__name__, elapsed)
        return result
    return wrapper
