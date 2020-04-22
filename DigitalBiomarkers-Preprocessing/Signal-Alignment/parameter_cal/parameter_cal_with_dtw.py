import pandas as pd
import math
import linecache
import numpy as np
from parameter_cal import cf
from parameter_cal.utils import get_k_accuracy_same, get_W, get_SS2, get_fact_align, get_reverse_dict, get_true_align, get_link_graph, load_data
from parameter_cal.utils import plot_warped_signals, cal_warped_signals
from dtw import dtw
from scipy.misc import *
import matplotlib.pyplot as plt


def norm(x, y):
    return math.fabs(x[1] - y[1])


y_list = load_data(True)
query, reference = cal_warped_signals(y_list)


# plot warped signal
xvals, yinterp = plot_warped_signals(reference, query)


# store the corresponding point pair
query.drop('shift', axis=1)
query.drop('t', axis=1)
query2 = pd.DataFrame(yinterp)
query2['aligned_index'] = 0
query2['t'] = query['t']
query2.columns = ['q', 'aligned_index', 't']
query2.loc[len(query2) - 1, 'aligned_index'] = len(query) - 1
for i in range(len(query2) - 1):
    for j in range(len(query['t2']) - 1):
        if query['t2'][j] <= query2['t'][i] < query['t2'][j + 1]:
            if abs(query2['q'][i] - query['q'][j]) < abs(query2['q'][i] - query['q'][j + 1]):
                query2.loc[i, 'aligned_index'] = j
            else:
                query2.loc[i, 'aligned_index'] = j + 1

d, cost_matrix, acc_cost_matrix, path = dtw(reference[['t', 'q']].values, query2[['t', 'q']].values, dist=norm)
get_link_graph(reference, query2, path, -3)
true_align_dict = get_true_align(query2)
fact_dict = get_fact_align(path)
reverse_dict = get_reverse_dict(path)
print("error rate of dtw is " + str(get_k_accuracy_same(true_align_dict, fact_dict, reference)))
print("W of dtw is " + str(get_W(path)))
print("SS2 of dtw is " + str(get_SS2(fact_dict, reverse_dict, 1)))