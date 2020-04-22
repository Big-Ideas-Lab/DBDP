import pandas as pd
import math
import numpy as np
from parameter_cal import cf
from dtw import dtw
from parameter_cal.utils import get_fact_align, get_SS1, get_SS2, get_reverse_dict, calculate_event, get_link_graph, load_data, exp_decay, edge_matching
from parameter_cal.utils import plot_warped_signals, cal_warped_signals, get_upslope_endings, get_downslope_endings
import matplotlib.pyplot as plt
from downsample.utils import get_true_aligned, get_group_number, get_k_accuracy, get_matched_graph, connect_edges
from debug.dbd_cf import debug_file, debug_line


def norm(x, y):
    #return math.fabs(x[1] - y[1])
    return math.fabs(x[1] - y[1])+math.fabs(x[2] - y[2])+math.fabs(x[3] - y[3])

y_list = load_data(debug_file, debug_line)
query, reference = cal_warped_signals(y_list, 'right')

reference['upslope'] = 0
reference['downslope'] = 0

# plot warped signal
xvals, yinterp = plot_warped_signals(reference, query, cf.ds_time)

# calculate the corresponding point pair
query.drop('shift', axis=1)
query.drop('t', axis=1)
query2 = pd.DataFrame({'t': xvals, 'q': yinterp})
query2['close_index'] = 0
query2['upslope'] = 0
query2['downslope'] = 0
true_align_dict = get_true_aligned(cf.ds_time, query, query2)
group_num_dict = get_group_number(true_align_dict, query)
plt.show()

raw_reference_uslope, reference_upslope = get_upslope_endings(reference['q'], cf.refer_percent)
raw_query_uslope, query_upslope = get_upslope_endings(query2['q'], cf.query_percent)

raw_reference_downslope, reference_downslope = get_downslope_endings(reference['q'], cf.refer_percent)
raw_query_downslope, query_downslope = get_downslope_endings(query2['q'], cf.query_percent)

rising_edge_grps = edge_matching(reference, query2, reference_upslope, query_upslope)
down_edge_grps = edge_matching(reference, query2, reference_downslope, query_downslope)
rising_edge_grps = connect_edges(rising_edge_grps, raw_reference_uslope)
get_matched_graph(rising_edge_grps, down_edge_grps, reference, query2, -3)

calculate_event(rising_edge_grps, reference, query2, True)
calculate_event(down_edge_grps, reference, query2, False)
d, cost_matrix, acc_cost_matrix, path = dtw(reference[['t', 'q', 'upslope', 'downslope']].values,
                                            query2[['t', 'q', 'upslope', 'downslope']].values, dist=norm)
get_link_graph(reference, query2, path, -3, 'Downsampled signal with EventDTW', '(a) EventDTW')
fact_align_dict = get_fact_align(path)
reverse_dict = get_reverse_dict(path)
print('group = ' + str(get_k_accuracy(true_align_dict, fact_align_dict, group_num_dict)))
print("SS1 of dtw is " + str(get_SS1(fact_align_dict, cf.ds_time)))
print("SS2 of dtw is " + str(get_SS2(fact_align_dict, reverse_dict, cf.ds_time)))

