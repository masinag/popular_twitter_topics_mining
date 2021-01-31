"""
Adapted from https://github.com/ymoch/apyori
"""
from itertools import islice
from .utils import create_next_candidates, map_to_original, log

def get_items(transactions):
    n_items = 0 # number of different items found
    index_transactions = [] # ith entry is the set of transactions in which ith element appears
    item_index = {} # maps items to indexes
    index_item = [] # ith entry is the item corresponding to ith index
    for i, transaction in enumerate(transactions):
        for item in transaction:
            j = item_index.get(item, -1)
            if j == -1:
                j = n_items
                n_items += 1 
                item_index[item] = j
                index_item.append(item)
                index_transactions.append(set())

            index_transactions[j].add(i)

    items = [frozenset((i,)) for i in range(n_items)]

    return items, index_transactions, index_item

def get_support(itemset, index_transactions):
    # get iterator on the transaction of each item in the itemset
    tt = map(lambda x : index_transactions[x], itemset)
    # get the size of their intersections
    return len(set.intersection(next(tt), *tt) if tt else set())


def apriori(transactions, s):
    candidates, index_transactions, index_item = get_items(transactions)
    # print(len(transactions))
    min_support = s * len(transactions)
    k = 1
    result = []
    while candidates:
        # log(f"{k}, {len(candidates)}")
        frequent_itemsets_k = set()
        for candidate in candidates:
            support = get_support(candidate, index_transactions)
            if support >= min_support:
                frequent_itemsets_k.add(candidate)
                if (len(candidate) > 1):
                    result.append(candidate)

        candidates = create_next_candidates(frequent_itemsets_k, k+1)
        k += 1
    # print(result)
    return map_to_original(result, index_item)
