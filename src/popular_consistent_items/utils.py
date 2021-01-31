import datetime
from itertools import combinations

DATES = ['time']

CONVERTERS = {'tokens' : lambda x : frozenset(x.split())}

DEBUG = False
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


def map_to_original(result, index_item):
    return [frozenset(index_item[i] for i in fi) for fi in result]

def create_next_candidates(prev_candidates, k):
    tmp_next_candidates = {s for s1 in prev_candidates for s2 in prev_candidates
        if len(s:=s1.union(s2)) == k}

    if k == 2:
        return tmp_next_candidates

    next_candidates = [
        candidate for candidate in tmp_next_candidates
        if all( x in prev_candidates
            for x in map(frozenset, combinations(candidate, k - 1)))
    ]
    return next_candidates