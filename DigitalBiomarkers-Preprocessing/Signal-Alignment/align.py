import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from dtw import dtw
import math
from scipy.spatial.distance import euclidean
from scipy.spatial.distance import seuclidean

def get_link(x, y, path, vertical_mov, shift_time):
    # make use of the feature of continuous increasing
    for i in range(len(path[0])):
        head_num = path[0][i]
        tail_num = path[1][i]
        plt.plot((x[head_num][0], y[tail_num][0]), (x[head_num][1], y[tail_num][1]+vertical_mov), 'r')


# x = pd.DataFrame(np.array([[0,1], [1,2], [2,3], [3,7], [4,9], [5,9], [6,9], [7,9], [8,8], [9,1], [10,1], [11,1], [12,1], [13,5], [14,7], [15,9], [16,9], [17,2], [18,1], [19,1], [20,1],[21,1]]))
# y = pd.DataFrame(np.array([[0,1], [2,1], [4,9], [6,9], [8,5], [10,1], [12,1], [14,9], [16,9], [18,1], [20,1]]))

x = pd.DataFrame(np.array([[0,1], [1,1], [2,1], [3,1],[4,1.2],[5,1],[6,1.2],[7,1],[8,1]]))
y = pd.DataFrame(np.array([[0,1], [2,1.1], [4, 1], [6,1]]))

fig, ax = plt.subplots(figsize=(20, 10))
ax.scatter(x[0].values, x[1].values, c='k', marker='^')
ax.scatter(y[0].values, y[1].values, c='r', marker='o')
plt.show()
norm = lambda x, y: math.fabs(x[1]-y[1])

dist, cost_matrix, acc_cost_matrix, path = dtw(x.values, y.values, dist = norm)
print(dist)
vertical_mov=-15
fig, ax = plt.subplots(figsize=(20, 10))
get_link(x.values, y.values, path, vertical_mov, shift_time=0)
ax.scatter(x[0].values, x[1].values, c='k', marker='.', s = 100)
ax.scatter(y[0].values, y[1].values+vertical_mov, c='b', s=100)
plt.show()

plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
plt.plot(path[0], path[1], 'w')
plt.show()