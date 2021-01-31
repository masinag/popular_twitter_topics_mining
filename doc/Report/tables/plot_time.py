import os, sys
import matplotlib

import matplotlib.pyplot as plt
RESULTS_DIR = '../../../bin/execution_times/'
TABLES_DIR = './'

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'font.size' : 18,
    'text.usetex': True,
    'pgf.rcfonts': False,
})




def read_times(filename):
    sum_s = 0
    sum_b = 0
    n = 0
    with open(filename) as f:
        for r in f:
            s, b = map(float, r.split())
            sum_s += s
            sum_b += b 
            n += 1

    return sum_s/n, sum_b/n

def plot_times(sizes, solution, baseline):

    plt.title("Execution time with different input sizes")

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Input size (number of tweets)')

    color = 'darkslategrey'
    ax1.set_ylabel('Basic A-Priori time (s)', color=color)
    ax1.plot(sizes, baseline, color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'midnightblue'
    ax2.set_ylabel('Efficient A-Priori time (s)', color=color)  # we already handled the x-label with ax1
    ax2.set_ylim([0, 5.9])
    ax2.plot(sizes, solution, color=color, marker='X')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(f"{TABLES_DIR}times.pgf")
    # plt.plot(sizes, solution)
    # plt.plot(sizes, baseline)
            

if __name__ == '__main__':
    base = ((sys.argv[0][:sys.argv[0].rfind('/') + 1]).rstrip('/') or '.') + '/'
    TABLES_DIR = f"{base}{TABLES_DIR}"


    sizes = []
    solution = []
    baseline = []
    for filename in sorted(os.listdir(f'{base}{RESULTS_DIR}'), key = int):
        sizes.append(int(filename))
        s, b = read_times(f"{base}{RESULTS_DIR}{filename}")
        solution.append(s)
        baseline.append(b)
    plot_times(sizes, solution, baseline)        
