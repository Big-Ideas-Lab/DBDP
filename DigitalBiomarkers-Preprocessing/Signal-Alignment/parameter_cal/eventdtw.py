import pandas as pd
import math
import linecache
import numpy as np
from parameter_cal import cf
from dtw import dtw
from scipy.misc import *
from parameter_cal.utils import get_k_accuracy_same, get_W, get_fact_align, get_reverse_dict, get_SS2, calculate_event, get_link_graph, get_true_align
from parameter_cal.utils import load_data, plot_warped_signals, cal_warped_signals


def norm(x, y):
    #return math.fabs(x[1] - y[1])
    return math.fabs(x[1] - y[1])+math.fabs(x[2] - y[2])+math.fabs(x[3] - y[3])


y_list = load_data('data/Beef_TRAIN')
query, reference = cal_warped_signals(y_list)

reference['upslope'] = 0
reference['downslope'] = 0

# plot warped signal
xvals, yinterp = plot_warped_signals(reference, query)


# calculate the corresponding point pair
query.drop('shift', axis=1)
query.drop('t', axis=1)
query2 = pd.DataFrame(yinterp)
query2['aligned_index'] = 0
query2['t'] = query['t']
query2.columns = ['q', 'aligned_index', 't']
query2['upslope'] = 0
query2['downslope'] = 0
query2.loc[len(query2) - 1, 'aligned_index'] = len(query) - 1
for i in range(len(query2) - 1):
    for j in range(len(query['t2']) - 1):
        if query['t2'][j] <= query2['t'][i] < query['t2'][j + 1]:
            if abs(query2['q'][i] - query['q'][j]) < abs(query2['q'][i] - query['q'][j + 1]):
                query2.loc[i, 'aligned_index'] = j
            else:
                query2.loc[i, 'aligned_index'] = j + 1

refer_peak_indexes = np.array([211])
query_peak_indexes = np.array([201])
calculate_event(refer_peak_indexes, reference, 1)
calculate_event(query_peak_indexes, query2, 1)


d, cost_matrix, acc_cost_matrix, path = dtw(reference[['t', 'q', 'upslope', 'downslope']].values, query2[['t', 'q', 'upslope', 'downslope']].values, dist=norm)
true_align_dict = get_true_align(query2)
fact_dict = get_fact_align(path)
get_link_graph(reference, query2, path, -3)
reverse_dict = get_reverse_dict(path)
print("path = " + str(len(path[0])))
print('group = '+str(get_k_accuracy_same(true_align_dict, fact_dict, reference)))
print("SS1 of dtw is " + str(get_W(path)))
print("SS2 of dtw is " + str(get_SS2(fact_dict, reverse_dict, 1)))
