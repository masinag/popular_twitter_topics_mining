import pandas as pd

from .apriori_opt import apriori as apriori_opt
from .apriori_basic import apriori as apriori_basic

# from memory_profiler import profile
from .utils import log

def get_frequent_items_in_time(tweets, s, r, a, start=None, end=None, basic=False):
    if tweets.empty:
        return []
    if not start:
        start = pd.Timestamp(tweets.time.min().date())
    if not end:
        end = tweets.time.max()
    frequent_itemset_f = apriori_basic if basic else apriori_opt

    log("File read")

    topics_counter = {} # number of times a topic is frequent in a period of time

    time_periods = 0
    grouper = pd.Grouper(key = "time", 
        origin = start, freq=f"{a}s")
    for group, batch in tweets.groupby(grouper):
        if group >= end:
            break
        log(f"Period of {group}")
        frequent_items = frequent_itemset_f(batch.tokens, s)
        for i in frequent_items:
            topics_counter[i] = topics_counter.get(i, 0) + 1
        time_periods += 1

    min_support = r * time_periods
    return [(i) for i, o in topics_counter.items() if o >= min_support]

