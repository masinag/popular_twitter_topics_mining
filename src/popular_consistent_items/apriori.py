import itertools
import functools
import operator
import math

from .utils import log

def insert_sorted_tuple(t, singleton):
    for i, e in enumerate(t):
        if e >= singleton:
            break
    return t[:i] + t + t[i:]

# @profile
def apriori(data, s):
    log(f"Looking for items appearing more than {s:.03f} times out of {data.shape[0]}")
    # get frequent singletons
    curr_occ = {}
    for tokens in data:
        for token in map(lambda x : frozenset((x, )), tokens):
            curr_occ[token] = curr_occ.get(token, 0) + 1
    frequencies = [{token for token, occ in curr_occ.items() if occ >= s}]
    # log(f"Got {len(frequencies[-1])} frequent itemsets if size 1: {'' if len(frequencies[-1]) > 10 else frequencies[-1]}")
    log(f"Got {len(frequencies[-1])} frequent itemsets if size 1")

    # get bigger itemsets
    n = 2 # itemsets size
    while len(frequencies[-1]) > 1:
        curr_occ.clear()
        # get frequent itemsets of size n
        for _, tokens in data.iteritems():
            for subset in map(frozenset, itertools.combinations(tokens, n)):
                assert(len(subset) == n)
                # count if it was already counted or \
                #   each of its subset of n-1 items was frequent
                if subset in curr_occ or  \
                    all(x in frequencies[-1] for x in map(frozenset, itertools.combinations(subset, n-1))):
                    curr_occ[subset] = curr_occ.get(subset, 0) + 1
        frequencies.append({token for token, occ in curr_occ.items() if occ >= s})
        assert(all(len(x)==n for x in frequencies[-1]))
        log(f"Got {len(frequencies[-1])} frequent itemsets if size {n}")
        n += 1
    
    curr_occ.clear()
    return functools.reduce(operator.iconcat, frequencies, [])

def combine(ss1, ss2, tokens, n):
    return set(filter(lambda x : x.issubset(tokens), (s \
        for s1 in ss1 for s2 in ss2 if len(s:=s1 | s2) == n)))

def extend_subsets(subsets, singletons, tokens, n):
    n_all_comb = math.comb(len(tokens), n)
    n_combine_subsets = len(subsets)**2
    n_add_singleton = len(subsets)*len(singletons)
    best = min(n_all_comb, n_combine_subsets, n_add_singleton)
    
    if best == n_all_comb:
        return map(frozenset, itertools.combinations(tokens, n))
    elif best == n_combine_subsets:
        return combine(subsets, subsets, tokens, n)
    else:
        return combine(subsets, singletons, tokens, n)


def apriori_opt(data, s):
    log(f"Looking for items appearing more than {s:.03f} times out of {data.shape[0]}")
    # get frequent singletons
    curr_occ = {}
    for tokens in data:
        for token in map(lambda x : frozenset((x, )), tokens):
            curr_occ[token] = curr_occ.get(token, 0) + 1
    frequencies = [{token for token, occ in curr_occ.items() if occ >= s}]

    # For each entry of data, find the frequent singletons it contains
    frequent_singletons = [[fs for fs in frequencies[-1] if fs.issubset(tokens)] 
        for tokens in data]

    log(f"Got {len(frequencies[-1])} frequent itemsets of size 1")

    # get bigger itemsets
    n = 2 # itemsets size
    # contains frequent itemsets found in the last pass for each entry
    # frequent_subsets = [frequent_singletons[i].copy() for i in range(len(data))]
    
    not_count = set()
    frequent_subsets = []
    while len(frequencies[-1]) > 1:
        # get frequent itemsets of size n
        curr_occ.clear()
        not_count.clear()

        for i, tokens in enumerate(data):
            frequent_subsets.clear()
            for fs in frequencies[-1]:
                if fs.issubset(tokens):
                    frequent_subsets.append(fs)
            for subset in extend_subsets(frequent_subsets, frequent_singletons[i], tokens, n):
                if (subset in curr_occ) or (subset not in not_count and  \
                    all(x in frequencies[-1] for x in map(frozenset, itertools.combinations(subset, n-1)))):
                    curr_occ[subset] = curr_occ.get(subset, 0) + 1
                else:
                    not_count.add(subset)
        frequencies.append({token for token, occ in curr_occ.items() if occ >= s})

        log(f"Got {len(frequencies[-1])} frequent itemsets if size {n}")
        n += 1
        
    return functools.reduce(operator.iconcat, frequencies, [])