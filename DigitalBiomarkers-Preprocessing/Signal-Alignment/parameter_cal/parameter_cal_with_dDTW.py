import pandas as pd
import math
import numpy as np
from parameter_cal import cf
from dtw import dtw
from scipy.misc import *
from parameter_cal.utils import get_k_accuracy_same, get_W, get_fact_align, get_SS2, get_reverse_dict, get_true_align, get_link_graph
from parameter_cal.utils import plot_warped_signals, load_data, cal_warped_signals
import matplotlib.pyplot as plt


def slope_col(query):
    # calculate the slope of query
    query_last = len(query) - 1
    query['slope'] = 0
    query.loc[1, 'slope'] = ((query.loc[1, 'q'] - query.loc[0, 'q']) + ((query.loc[2 , 'q'] - query.loc[1, 'q']) / 2)) / 2
    query.loc[0, 'slope'] = query.loc[1, 'slope']
    for i in range(2, query_last - 1):
        query.loc[i , 'slope'] = ((query.loc[i, 'q'] - query.loc[i-1, 'q']) + ((query.loc[i+1, 'q'] - query.loc[i, 'q']) / 2)) / 2
        query.loc[query_last - 1, 'slope'] = ((query.loc[query_last - 1, 'q'] - query.loc[query_last - 2, 'q']) + ((query.loc[query_last, 'q'] - query.loc[query_last - 1, 'q']) / 2)) / 2
        query.loc[query_last, 'slope'] = query.loc[query_last - 1, 'slope']


def norm(x, y):
    return math.fabs(x[1] - y[1])


def gaussian_bump(x, a=1):
    return math.exp(1 / (pow((x / a), 2) - 1))


# when x = 0, sigmoid's derivative value is 1/4a
def sigmoid0(x):
    return (4 * cf.warp_width) / (1 + math.exp(-x / cf.warp_width))


sigmoid = np.vectorize(sigmoid0)

y_list = load_data('data/Beef_TRAIN', 1)
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


slope_col(query2)
slope_col(reference)
d, cost_matrix, acc_cost_matrix, path = dtw(reference[['t', 'slope']].values, query2[['t', 'slope']].values, dist=norm)
get_link_graph(reference, query2, path, -3)
true_align_dict = get_true_align(query2)
fact_dict = get_fact_align(path)
reverse_dict = get_reverse_dict(path)
print("error rate of dtw is " + str(get_k_accuracy_same(true_align_dict, fact_dict, reference)))
print("W of ddtw is " + str(get_W(path)))
print("SS2 of ddtw is " + str(get_SS2(fact_dict, reverse_dict, 1)))
