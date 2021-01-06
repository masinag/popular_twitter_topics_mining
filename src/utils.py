import regex as re
import datetime

DATES = ['time']

CONVERTERS = {'tokens' : lambda x : x.split()}

def get_curr_timestamp():
    now = datetime.datetime.now()
    return f"{now.year:04d}{now.month:02d}{now.day:02d}_{now.hour:02d}{now.minute:02d}{now.second:02d}"
