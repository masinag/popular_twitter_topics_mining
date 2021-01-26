import regex as re
import datetime

DATES = ['time']

CONVERTERS = {'tokens' : lambda x : frozenset(x.split())}

DEBUG = True
# RE_DATETIME = re.compile(r"(?P<y>\d\d\d\d)-(?P<mo>\d\d)-(?P<d>\d\d) "+ \
#     r"(?P<h>\d\d):(?P<mi>\d\d):(?P<s>\d\d)")

# def get_datetime(fields):
#     ff = {key : int(value[0]) for key, value in fields.items()}
#     return datetime(ff['y'], ff['mo'], ff['d'], ff['h'], ff['mi'], ff['s'])

def log(msg):
    if DEBUG:
        print(msg)


def get_curr_timestamp():
    now = datetime.datetime.now()
    return f"{now.year:04d}{now.month:02d}{now.day:02d}_{now.hour:02d}{now.minute:02d}{now.second:02d}"
