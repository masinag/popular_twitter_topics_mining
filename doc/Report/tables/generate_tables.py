import os, sys

DEFAULT_VALUES = {'s':'0.0100', 'r':'0.1000', 'a':f'{24*60*60}', 'baseline': f'{38*24*60*60}'}
VAR_POS = {'s':0, 'r':1, 'a':2}
RESULTS_DIR = '../../../bin/results/'
TABLES_DIR = './'
MAX_ENTRIES = 30


HEADER = r'''
\begin{table}
    \centering
    \caption{%s}
    \label{tab:%s}
    \begin{tabular}{>{\raggedright}p{0.22\textwidth}>{\raggedright}p{%f\textwidth}p{%f\textwidth}p{%f\textwidth}p{%f\textwidth}}
        \toprule
            Itemset
'''

FOOTER = r'''
    \bottomrule
    \end{tabular}
    %s
\end{table}

'''

def format_header(var, h):
    if var == 'a':
        sec = int(h)
        h = sec // 3600
        d = sec // (24*3600)
        if d == 0:
            # return fr"${h}$ hour{'s'*min(1, h-1)}"
            return fr"${h}$ h"
        else:
            # return fr"${d}$ day{'s'*min(1, d-1)}"
            return fr"${d}$ d"
    elif var == 's':
        return fr"${h[3]}.{h[4:]}$\small\%"
    elif var == 'r':
        return fr"${h[2:4].lstrip('0')}.{h[4:5]}$\small\%"
    return h

def generate_vary_table(var, var_files):
    var_files.sort(key=lambda fn : float(fn[fn.rfind('/')+1:].split('#')[VAR_POS[var]]), reverse=True)

    itemsets = {}
    headers = []
    for i, filename in enumerate(var_files):
        headers.append(filename[filename.rfind('/')+1:].split('#')[VAR_POS[var]])
        with open(filename) as f:
            for r in f:
                # itemset, frequence = r.split(', ')
                itemset_key = frozenset(r.split())
                
                if itemset_key not in itemsets:
                    itemsets[itemset_key] = []
                while len(itemsets[itemset_key]) < i:
                    itemsets[itemset_key].append(False)
                itemsets[itemset_key].append(True)
    print(headers)
    # write header
    with open(f'{TABLES_DIR}varying_{var}.tex', 'w') as f:
        f.write(HEADER % (f'Popular consistent topics identified, varying ${var}$', var, 0.038, 0.038, 0.038, 0.038))
        for h in headers:
            f.write(fr'& {format_header(var, h)}  ')
        f.write(r''' \\          
        \midrule
        ''')

        # for itemset, presence in itemsets.items():
        #     print()
        
        count = 0
        print(var, len(itemsets))
        for itemset, presence in sorted(itemsets.items(), key = lambda x : (-sum(x[1]), sorted(x[0]))):
            s = ' '.join(sorted(itemset))
            if len(s) >= 30:
                if (sum(presence) > 1):
                    print(itemset, presence)
                assert(sum(presence) == 1)
                continue
            count += 1
            while(len(presence) < len(headers)):
                presence.append(False)
            f.write(f'{s} ')
            for p in presence:
                if p:
                    f.write(r'& \checkC{} ')
                else:
                    f.write(r'&        {} ')
            f.write(r'''\\
                ''')
            if count == MAX_ENTRIES:
                break

        if not (len(itemsets) < MAX_ENTRIES or count >= MAX_ENTRIES):
            print("AAAAAA", len(itemsets), count)
        # assert(len(itemsets) < 50 or count >= 50) 
        comment = r'''
        \begin{flushleft}
        The table shows the topics identified by the algorithm with different values 
        of $%s$. A cell is grey if the topic in the row has been identified by setting the parameter
        value corresponding to the column. %s 
    \end{flushleft}
        ''' % (var, '' if count < MAX_ENTRIES else 'Here we show the first %d rows out of %d.' % (count, len(itemsets)))
        f.write(FOOTER % comment)


def generate_baseline_table(var_files):
    itemsets = {}
    headers = []
    for i, (method, filename) in enumerate(sorted(var_files.items(), reverse=True)):
        headers.append(method)
        with open(filename) as f:
            for r in f:
                # itemset, frequence = r.split(', ')
                itemset_key = frozenset(r.split())
                # if len(itemset_key) > 3:
                #     continue
                # if min(map(len, itemset_key)) <= 3:
                #     continue
                if itemset_key not in itemsets:
                    itemsets[itemset_key] = []
                while len(itemsets[itemset_key]) < i:
                    itemsets[itemset_key].append(False)
                itemsets[itemset_key].append(True)
    # write header
    print(f'{TABLES_DIR}baseline.tex')
    with open(f'{TABLES_DIR}baseline.tex', 'w') as f:
        f.write(HEADER % (f'Comparison with baseline method', 'bl', 0.12, 0.12, 0.12, 0.12))

        for h in headers:
            f.write(fr'& {h}  ')
        f.write(r''' \\          
        \midrule
        ''')

        # for itemset, presence in itemsets.items():
        #     print()
        

        count = 0
        for itemset, presence in sorted(itemsets.items(), key = lambda x : (-sum(x[1]), sorted(x[0]))):
            s = ' '.join(sorted(itemset))
            if len(s) >= 30:
                if (sum(presence) > 1):
                    print(itemset, presence)
                assert(sum(presence) == 1)
                continue
            count += 1
            while(len(presence) < len(headers)):
                presence.append(False)
            f.write(f'{s} ')
            for p in presence:
                if p:
                    f.write(r'& \checkC{} ')
                else:
                    f.write(r'&        {} ')
            f.write(r'''\\
                ''')
            if count == MAX_ENTRIES:
                break

        if not (len(itemsets) < MAX_ENTRIES or count >= MAX_ENTRIES):
            print("AAAAAA", len(itemsets), count)
        # print('\n'.join(map(str, itemsets.items())))
        comment = r'''
        \begin{flushleft}
            The table shows the topics identified by the solution proposed compared 
            with the ones found by the baseline method. 
            A cell is grey if the topic in the row has been identified by the method corresponding to the column. %s 
        \end{flushleft}
        ''' % ('' if count < MAX_ENTRIES else 'Here we show the first %d rows out of %d.' % (count, len(itemsets)))
        f.write(FOOTER % comment) 

            

if __name__ == '__main__':
    base = ((sys.argv[0][:sys.argv[0].rfind('/') + 1]).rstrip('/') or '.') + '/'
    RESULTS_DIR = f"{base}{RESULTS_DIR}"
    for var in DEFAULT_VALUES:
        if var != 'baseline':
            var_files = []
            for filename in os.listdir(f'{base}{RESULTS_DIR}'):
                ff = filename.split('#')
                val = {v: ff[i] for v, i in VAR_POS.items()}
                other_default = True
                for k, v in val.items():
                    if k != var and v != DEFAULT_VALUES[k] or (k == 'a' and v == DEFAULT_VALUES['baseline']):
                        other_default = False
                if other_default:
                    var_files.append(f'{base}{RESULTS_DIR}{filename}')

            generate_vary_table(var, var_files)
        else:
            var_files = {}
            for filename in os.listdir(f'{base}{RESULTS_DIR}'):
                ff = filename.split('#')
                val = {v: ff[i] for v, i in VAR_POS.items()}
                if val['s'] == '0.0100' and all(v == DEFAULT_VALUES[k] for k, v in val.items() if k != 's'):
                    var_files['Solution proposed'] = (f'{base}{RESULTS_DIR}{filename}')
                elif val['a'] == DEFAULT_VALUES['baseline']:
                    var_files['Baseline method'] = (f'{base}{RESULTS_DIR}{filename}')

            generate_baseline_table(var_files)

