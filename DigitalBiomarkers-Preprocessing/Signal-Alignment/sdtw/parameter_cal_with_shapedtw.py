import pandas as pd
import math
import numpy as np
from scipy import stats
from parameter_cal import cf
from dtw import dtw
from scipy.misc import *
from sdtw.config import sub_len, nBlocks
from sdtw.utils import norm, cal_refer_query_descriptor
from parameter_cal.utils import get_fact_align, get_reverse_dict, get_k_accuracy_same, get_W, get_SS2, get_true_align, get_link_graph
from parameter_cal.utils import load_data, plot_warped_signals, cal_warped_signals
import matplotlib.pyplot as plt


y_list = load_data(True)
query, reference = cal_warped_signals(y_list)

# plot warped signal
xvals, yinterp = plot_warped_signals(reference, query, 1)

# normalize the signal
reference_norm = stats.zscore(reference['q'])
yinterp_norm = stats.zscore(yinterp)

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


if sub_len%2 == 0:
    raise Exception("Sub_len must be odd number!")

refer_descriptors, query_descriptors = cal_refer_query_descriptor(reference_norm, yinterp_norm, sub_len)


d, cost_matrix, acc_cost_matrix, path = dtw(refer_descriptors, query_descriptors, dist=norm)
get_link_graph(reference, query, path, -3, 'shapedtw without downsample')
true_align_dict = get_true_align(query2)
fact_dict = get_fact_align(path)
reverse_dict = get_reverse_dict(path)
print("error rate of shapedtw is " + str(get_k_accuracy_same(true_align_dict, fact_dict, reference)))
print("W of shapedtw is " + str(get_W(path)))
print("SS2 of shapedtw is " + str(get_SS2(fact_dict, reverse_dict, 1)))


