import pandas as pd
import regex as re
from .apriori import apriori, apriori_opt
from memory_profiler import profile
# from collections import deque
# import matplotlib.pyplot as plt
from .utils import DATES, CONVERTERS, get_curr_timestamp, log
# CHUNK_SIZE = 10000 # rows read per time
TIME_RANGE = 43200 # seconds, to count frequency (43200 sec = 12 hours)

def count(data, itemset):
    count = 0
    for tokens in data:
        if itemset.issubset(tokens):
            count += 1
    # print(itemset, count)
    return count

# @profile
def get_frequent_items_in_time(dataset, s, a, start, end, frequent_itemset_f=apriori_opt):
    data = pd.read_csv(dataset, usecols=["time", "tokens"], encoding="utf-8", \
         parse_dates=DATES, converters = CONVERTERS).sort_values(by="time")
    if data.empty:
        return {}, 0
    if not start:
        start = pd.Timestamp(data.iloc[0].time.date())
    if not end:
        end = data.iloc[-1].time
    log("File read")

    base_date = None
    periods_frequent = {} # number of times a token is frequent in a period of time

    time_periods = 0
    
    grouper = pd.Grouper(key = "time", 
        origin = start, freq=f"{a}s")
    for group, batch in data.groupby(grouper):
        if group >= end:
            break
        log(f"Period of {group}")
        frequent_items = frequent_itemset_f(batch.tokens, s*len(batch))
        assert(len(frequent_items) == len(set(frequent_items)))
        for i in frequent_items:
            # if (count(batch.tokens, i) < s*len(batch)):
            #     print(i)

            # assert(count(batch.tokens, i) >= s*len(batch))
            periods_frequent[i] = periods_frequent.get(i, 0) + 1
        time_periods += 1
    # log(f"{time_periods} anayzed, looking for topics in >= {p * time_periods} periods")

    return periods_frequent, time_periods
    # if frequencies:
    #     ll.append(frequencies)
    # print(ll)
    # lines = pd.DataFrame(ll)
    # print(lines)
    # print(lines.shape)
    # print(lines.columns)
    # lines.plot()
    # plt.show()


         

