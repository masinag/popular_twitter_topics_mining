import sys
import time
from argparse import ArgumentParser
from popular_consistent_items.popular_consistent_items import get_frequent_items_in_time
from popular_consistent_items.utils import get_curr_timestamp, DATES, CONVERTERS
import pandas as pd
import timeit


def write_output(output, times):
    with open(output, 'a+') as f:
        # for (ii) in sorted(fi, key=lambda t : t[1], reverse = True):
        for (t1, t2) in times:
            # f.write(f"{format_set(ii)}, {oo}\n")
            f.write(f"{t1} {t2}\n")

def main(args):
    oo = f"{args.output_dir.rstrip('/')}/{args.s:.04f}#{args.r:.04f}#{args.a}#{get_curr_timestamp()}"
    dd = pd.read_csv(f"{args.input}", usecols=["time", "tokens"], encoding="utf-8", \
         parse_dates=DATES, converters = CONVERTERS)
    tt = []
    for _ in range(args.tests):
        print(_)
        bb = dd.sample(n = int(args.data_size * len(dd)))
        t1 = timeit.Timer(stmt="get_frequent_items_in_time(bb, args.s, args.r, args.a, basic=False)", globals=locals(),
            setup="from popular_consistent_items.popular_consistent_items import get_frequent_items_in_time")
        t2 = timeit.Timer(stmt="get_frequent_items_in_time(bb, args.s, args.r, args.a, basic=True)",  globals=locals(),
            setup="from popular_consistent_items.popular_consistent_items import get_frequent_items_in_time")
        tt.append((t1.timeit(number=1), t2.timeit(number=1)))

    write_output(f"{args.output_dir.rstrip('/')}/{int(args.data_size * len(dd))}", tt)

if __name__ == '__main__':
    base = ((sys.argv[0][:sys.argv[0].rfind('/') + 1]).rstrip('/') or '.') + '/'
    ap = ArgumentParser()

    ap.add_argument("--input",  
    help="path to the file in input (csv format with two columns 'time' and 'tokens')",
    type=str, default=f"{base}../data/cleaned_covid19_tweets.csv")
    ap.add_argument("--output_dir", 
        help="path to the output directory", 
        type=str,
        default=f"{base}../bin/execution_times/")
    ap.add_argument("--s", 
        help="minimum support to consider a topic frequent in a period of time", 
        type=float, default=0.01)
    ap.add_argument("--r", 
        help="minimum support to consider a topic consistent among the periods of time", 
        type=float, default=0.1)
    ap.add_argument("--a", 
        help="amplitude of each period of time in seconds", 
        type=int, default= 24 * 60 * 60)
    ap.add_argument("--tests", type=int, default=20, help="Number of tests to perform")
    ap.add_argument("--data_size", required=True, type=float, help="Fraction of data to sample")

    main(ap.parse_args())