import re, csv
from argparse import ArgumentParser
import time
import random
RE_DATETIME = re.compile(r"^\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d")
LOG_FILE = open("../../data/check.log", "w")

def log(s):
    LOG_FILE.write(s + "\n")

def c_str(e):
    return True

def c_datetime(e):
    return RE_DATETIME.match(e)

def c_int(e):
    try:
        _ = int(e)
        return True
    except ValueError:
        return False

def c_bool(e):
    return e == "True" or e == "False"

def c_list(e):
    return e.strip() == "" or type(eval(e)) == list

def main(dataset, output, p):
    rows = []
    with open(dataset) as f, open(output, 'w') as o:
        reader = csv.reader(f)
        writer = csv.writer(o, quoting = csv.QUOTE_NONNUMERIC)
        header = next(reader)
        writer.writerow(header)
        # types=[c_str, c_str, c_str, c_datetime, c_int, c_int, c_int, c_bool, 
        #     c_datetime, c_str, c_list, c_str, c_bool]
        for r in reader:
            # # ff = r.split(',')
            # for e, t in zip(r, types):
            #     # print(e, t)
            #     if not t(e):
            #         log("%s does not match type %s" % (e, t.__name__))
            #         log("Record:\n%s" % str(r))
            #         break
            if random.uniform(0, 1) < p:
                writer.writerow(r)
    


if __name__ == "__main__":
    dataset="../../data/cleaned_covid19_tweets.csv"

    ts = time.localtime(time.time())
    
    output = f"../../data/tmp_log/{ts.tm_year}{ts.tm_mon:02d}{ts.tm_mday:02d}_{ts.tm_hour:02d}{ts.tm_min:02d}{ts.tm_sec:02d}.log"
    ap = ArgumentParser()
    ap.add_argument("p", type=float, help="fraction of data you want to analyze")
    main(dataset, output, ap.parse_args().p)