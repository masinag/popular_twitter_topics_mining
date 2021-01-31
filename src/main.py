import pandas as pd
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from popular_consistent_items.popular_consistent_items import get_frequent_items_in_time
from popular_consistent_items.utils import get_curr_timestamp, DATES, CONVERTERS

def format_set(s):
    return ' '.join(s)

def write_output(output, fi):
    with open(output, 'w') as f:
        # f.write(f"{pt}\n")
        # for (ii) in sorted(fi, key=lambda t : t[1], reverse = True):
        for (ii) in fi:
            # f.write(f"{format_set(ii)}, {oo}\n")
            f.write(f"{format_set(ii)}\n")

def main(args):
    output = f"{args.output_dir.rstrip('/')}/{args.s:.04f}#{args.r:.04f}#{args.a}#{get_curr_timestamp()}"
    data = pd.read_csv(f"{args.input}", usecols=["time", "tokens"], encoding="utf-8", \
         parse_dates=DATES, converters = CONVERTERS)

    fi = get_frequent_items_in_time(data, args.s, args.r, args.a, args.start, args.end, args.basic)

    write_output(output, fi)

if __name__ == "__main__":
    base = ((sys.argv[0][:sys.argv[0].rfind('/') + 1]).rstrip('/') or '.') + '/'

    ap = ArgumentParser("""Program to find consistent popular topics in tweets.
    """,
    formatter_class=ArgumentDefaultsHelpFormatter)
    ap.add_argument("--input",  
        help="path to the file in input (csv format with two columns 'time' and 'tokens')",
        type=str,
        default=f"{base}../data/cleaned_covid19_tweets.csv")
    ap.add_argument("--output_dir", 
        help="path to the output directory", 
        type=str,
        default=f"{base}../bin/results/")
    ap.add_argument("--s", 
        help="minimum support to consider a topic frequent in a period of time", 
        type=float, default=0.01)
    ap.add_argument("--r", 
        help="minimum support to consider a topic consistent among the periods of time", 
        type=float, default=0.1)
    ap.add_argument("--a", 
        help="amplitude of each period of time in seconds", 
        type=int, default= 24 * 60 * 60)
    ap.add_argument("--start", help="""
    start timestamp of the first period to consider.
    If not set, it will be set the midnight of the day of the oldest
    tweet in the dataset.
    """, type=pd.Timestamp, default=None)
    
    ap.add_argument("--end", help="""end timestamp of the last period to consider.
    If not set, it will be set the timestamp of the most recent tweet in the dataset.
    """, type=pd.Timestamp, default=None)
    
    ap.add_argument("--basic", help="use the basic apriori implementation", 
        action="store_true")



    main(ap.parse_args())
    
