from .utils import log, create_next_candidates, map_to_original

def get_support(itemset, transactions):
    counter = 0
    for items in transactions:
        if itemset.issubset(items):
            counter += 1
    return counter

def get_items(transactions):
    n_items = 0 # number of different items found
    items = set() # contains the items found
    for transaction in transactions:
        for item in transaction:
            c = frozenset((item, ))
            if c not in items:
                items.add(c)

    return items


def apriori(transactions, s):
    candidates = get_items(transactions)

    min_support = s * len(transactions)
    k = 1
    result = []
    while candidates:
        frequent_itemsets_k = set()
        for candidate in candidates:
            support = get_support(candidate, transactions)
            if support >= min_support:
                frequent_itemsets_k.add(candidate)
                if (len(candidate) > 1):
                    result.append(candidate)

        candidates = create_next_candidates(frequent_itemsets_k, k+1)
        k += 1
    
    return result