import pandas as pd
import sys
from argparse import ArgumentParser
from popular_consistent_items.popular_consistent_items import get_frequent_items_in_time
from popular_consistent_items.utils import get_curr_timestamp
import tracemalloc
def format_set(s):
    return ' '.join(s)

def write_output(output, fi, pt):
    with open(output, 'w') as f:
        f.write(f"{pt}\n")
        for ii, oo in sorted(fi.items(), key=lambda t : t[1], reverse = True):
            if oo > 1 and len(ii) > 1:
                f.write(f"{format_set(ii)}, {oo}\n")

def main(base, args):
    output = f"{base}{args.output_dir.rstrip('/')}/{args.s:.04f}#{get_curr_timestamp()}"
    # tracemalloc.start()
    # usage = resource.getrusage(resource.RUSAGE_SELF)
    fi, pt = get_frequent_items_in_time(f"{base}{args.input}", args.s, args.a, args.start, args.end)
    # current, peak = tracemalloc.get_traced_memory()
    # print(f"Current memory usage is {current / 10**6}MB; Peak was {peak / 10**6}MB")
    # tracemalloc.stop()
    write_output(output, fi, pt)

if __name__ == "__main__":

    ap = ArgumentParser()
    ap.add_argument("--input", 
        help="path to the file in input (csv format)",
        type=str,
        default="../data/cleaned_covid19_tweets.csv")
    ap.add_argument("--output_dir", 
        help="path to the output directory", 
        type=str,
        default=f"../bin/results/")
    ap.add_argument("--s", 
        help="fraction of buckets to consider an itemset popular", 
        type=float, default=0.01)
    ap.add_argument("--r", 
        help="fraction of periods to consider an itemset consistent", 
        type=float, default=0.01)
    ap.add_argument("--a", 
        help="duration of each period in seconds", 
        type=int, default= 24 * 60 * 60)
    ap.add_argument("--start", help="start of the first period to consider", 
        type=pd.Timestamp, default=None)
    ap.add_argument("--end", help="end of the first period to consider", 
        type=pd.Timestamp, default=None)

    base = ((sys.argv[0][:sys.argv[0].rfind('/') + 1]).rstrip('/') or '.') + '/'

    main(base, ap.parse_args())
    
