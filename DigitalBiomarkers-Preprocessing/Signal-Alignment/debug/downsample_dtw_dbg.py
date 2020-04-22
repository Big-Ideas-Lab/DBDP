import pandas as pd
import math
import numpy as np
from parameter_cal import cf
from dtw import dtw
from parameter_cal.utils import get_SS1, get_fact_align, get_reverse_dict, get_SS2, get_link_graph
from parameter_cal.utils import load_data, plot_warped_signals, cal_warped_signals
import matplotlib.pyplot as plt
from downsample.utils import get_true_aligned, get_group_number, get_k_accuracy
from debug.dbd_cf import debug_file, debug_line


def norm(x, y):
    return math.fabs(x[1] - y[1])


y_list = load_data(debug_file, debug_line)
query, reference = cal_warped_signals(y_list, 'right')

# plot warped signal
# downsample times
xvals, yinterp = plot_warped_signals(reference, query, cf.ds_time)

# calculate the corresponding point pair
query.drop('shift', axis=1)
query.drop('t', axis=1)
query2 = pd.DataFrame({'t': xvals, 'q': yinterp})
query2['close_index'] = 0
true_align_dict = get_true_aligned(cf.ds_time, query, query2)
group_num_dict = get_group_number(true_align_dict, query)

d, cost_matrix, acc_cost_matrix, path = dtw(reference[['t', 'q']].values, query2[['t', 'q']].values, dist=norm)
get_link_graph(reference, query2, path, -3, None, '(c) DTW')
fact_align_dict = get_fact_align(path)
reverse_dict = get_reverse_dict(path)
print('group = '+str(get_k_accuracy(true_align_dict, fact_align_dict, group_num_dict)))
print("SS1 of dtw is " + str(get_SS1(fact_align_dict, cf.ds_time)))
print("SS2 of dtw is " + str(get_SS2(fact_align_dict, reverse_dict, cf.ds_time)))
