import itertools
import functools
import operator

from .utils import log

# @profile
def apriori(data, s):
    log(f"Looking for items appearing more than {s:.03f} times out of {data.shape[0]}")
    # get frequent singletons
    curr_occ = {}
    for tokens in data:
        for token in tokens:
            curr_occ[token] = curr_occ.get(token, 0) + 1
    frequencies = [{(token, ) for token, occ in curr_occ.items() if occ >= s}]
    # log(f"Got {len(frequencies[-1])} frequent itemsets if size 1: {'' if len(frequencies[-1]) > 10 else frequencies[-1]}")
    log(f"Got {len(frequencies[-1])} frequent itemsets if size 1")
    curr_occ.clear()

    # get bigger itemsets
    n = 2 # itemsets size
    while len(frequencies[-1]) > 1:
        # get frequent itemsets of size n
        for _, tokens in data.iteritems():
            for subset in itertools.combinations(tokens, n):
                # count if it was already counted or \
                #   each of its subset of n-1 items was frequent
                if subset in curr_occ or  \
                    all(x in frequencies[-1] for x in itertools.combinations(subset, n-1)):
                    curr_occ[subset] = curr_occ.get(subset, 0) + 1
        frequencies.append({token for token, occ in curr_occ.items() if occ >= s})
        log(f"Got {len(frequencies[-1])} frequent itemsets if size {n}")
        n += 1
        curr_occ.clear()
    return functools.reduce(operator.iconcat, frequencies, [])