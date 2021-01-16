from matplotlib import pyplot as plt
import numpy as np
ld = {}

with open("../../data/tmp_tf_idfs.dict") as f:
    ld = eval(f.read())

flat = []
for d in ld:
    flat.extend(d.values()) 

flat.sort(reverse = True)
print(f"Max:{np.max(flat)}\nMin:{np.min(flat)}\nAvg:{np.mean(flat)}")

plt.plot(range(len(flat)), flat)
plt.show()

