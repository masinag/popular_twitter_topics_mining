import pandas as pd
import regex as re
from datetime import datetime
import itertools
import functools
import operator
from memory_profiler import profile
# from collections import deque
# import matplotlib.pyplot as plt
from utils import DATES, CONVERTERS
# CHUNK_SIZE = 10000 # rows read per time
TIME_RANGE = 43200 # seconds, to count frequency (43200 sec = 12 hours)
DEBUG = True
# RE_DATETIME = re.compile(r"(?P<y>\d\d\d\d)-(?P<mo>\d\d)-(?P<d>\d\d) "+ \
#     r"(?P<h>\d\d):(?P<mi>\d\d):(?P<s>\d\d)")

# def get_datetime(fields):
#     ff = {key : int(value[0]) for key, value in fields.items()}
#     return datetime(ff['y'], ff['mo'], ff['d'], ff['h'], ff['mi'], ff['s'])

def log(msg):
    if DEBUG:
        print(msg)

def time_diff(datetime1, datetime2):
    # match1 = RE_DATETIME.match(datetime1)
    # match2 = RE_DATETIME.match(datetime2)
    
    # if not match1 or not match2:
    #     raise ValueError
    # fields1 = match1.capturesdict()
    # fields2 = match2.capturesdict()
    # d1 = get_datetime(fields1)
    # d2 = get_datetime(fields2)
    return (datetime2 - datetime1).total_seconds()

def get_day_half(date):
    return pd.Timestamp(date.year, date.month, date.day, 
        0 if date.hour < 12 else 12, 0, 0)
    
# def find_items(dataset):
#     chunks = pd.read_csv(dataset, usecols=["tokens"], encoding="utf8", chunksize=CHUNK_SIZE)
#     s = dict()
#     l = 0
#     max_b = 0
#     for chunk in chunks:
#         for row in chunk.iterrows():
#             l += 1
#             r = row[1]
#             tokens = eval(r.tokens)
#             for t in tokens:
#                 s[t] = s.get(t, 0) + 1
#             max_b = max(max_b, len(tokens))
#     print("Max tokens: %d" % max_b)
#     mf = max(s.values())
#     mm = {k : v for k, v in s.items() if v == mf}
#     print("Max freq: %s" % str(mm))
#     return {t for t, f in s.items() if f >= MIN_FREQ}, l

# @profile
def get_frequent_items(data, s):
    m = len(data)
    log(f"Looking for items appearing more than {s * m} times out of {data.shape[0]}")
    # get frequent singletons
    curr_occ = {}
    for _, tokens in data.iteritems():
        for token in tokens:
            curr_occ[token] = curr_occ.get(token, 0) + 1
    frequencies = [{(token, ) for token, occ in curr_occ.items() if occ >= s * m}]
    log(f"Got {len(frequencies[-1])} frequent itemsets if size 1: {'' if len(frequencies[-1]) > 10 else frequencies[-1]}")
    curr_occ.clear()

    # get bigger itemsets
    n = 2 # itemsets size
    while len(frequencies[-1]) > 1:
        # get frequent itemsets of size n
        for _, tokens in data.iteritems():
            for subset in itertools.combinations(tokens, n):
                if subset in curr_occ or  \
                    all(x in frequencies[-1] for x in itertools.combinations(subset, n-1)):
                    curr_occ[subset] = curr_occ.get(subset, 0) + 1
        frequencies.append({token for token, occ in curr_occ.items() if occ >= s * m})
        log(f"Got {len(frequencies[-1])} frequent itemsets if size {n}: {'' if len(frequencies[-1]) > 10 else frequencies[-1]}")
        n += 1
        curr_occ.clear()
    return functools.reduce(operator.iconcat, frequencies, [])

# @profile
def get_frequent_items_in_time(dataset, s_f, p_f):
    data = pd.read_csv(dataset, usecols=["date", "tokens"], encoding="utf-8", \
         parse_dates=DATES, converters = CONVERTERS)
    
    log("File read")
    data["date_group"] = data.date.apply(get_day_half)
    # f_items, length = find_items(dataset)
    # print("items: %d, rows: %d" % (len(f_items), length))
    # print(f_items)
    # lines = pd.DataFrame.from_dict()
    # i = 0
    base_date = None
    periods_frequent = {} # number of times a token is frequent in a period of time
    # batch = []
    time_periods = 0
    # for _, r in data.iterrows():
        
    #     if not base_date:
    #         base_date = r.date   
    #     if time_diff(base_date, r.date) <= TIME_RANGE:
    #         batch.append(r.tokens)
    #     else:
    #         log(f"Period from {base_date} to {r.date}")
    #         frequent_items = get_frequent_items(batch, s)
    #         for i in frequent_items:
    #             periods_frequent[i] = periods_frequent.get(i, 0) + 1
    #         time_periods += 1
    #         base_date = r.date
    #         batch.clear()
    for group, batch in data.groupby(by = "date_group"):
        time_periods += 1
        log(f"Period of {group}")
        frequent_items = get_frequent_items(batch.tokens, s)
        for i in frequent_items:
            periods_frequent[i] = periods_frequent.get(i, 0) + 1
        time_periods += 1
    log(f"{time_periods} anayzed, looking for topics in >= {p * time_periods} periods")
    return [i for i, f in periods_frequent.items() if f >= p * time_periods]
    # if frequencies:
    #     ll.append(frequencies)
    # print(ll)
    # lines = pd.DataFrame(ll)
    # print(lines)
    # print(lines.shape)
    # print(lines.columns)
    # lines.plot()
    # plt.show()


if __name__ == "__main__":
    dataset="data/tweets_clean.csv"
    s = 0.02 # percent of tweets per period of time
    p = 0.04 # percent of periods of time considered
    print(sorted(get_frequent_items_in_time(dataset, s, p), key = lambda x : len(x)))