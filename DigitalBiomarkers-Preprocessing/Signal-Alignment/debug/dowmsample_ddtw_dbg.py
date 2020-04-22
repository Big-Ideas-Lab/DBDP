import pandas as pd
import math
from parameter_cal import cf
from dtw import dtw
from downsample.utils import get_true_aligned, get_group_number
from parameter_cal.utils import get_SS2, get_group_devi, get_SS1, get_fact_align, get_reverse_dict, get_link_graph
from parameter_cal.utils import load_data, plot_warped_signals, cal_warped_signals
from downsample.utils import slope_col, reference_slope_col, get_k_accuracy
from debug.dbd_cf import debug_file, debug_line


def norm(x, y):
    return math.fabs(x[1] - y[1])


# generate warped signal
y_list = load_data(debug_file, debug_line)
y_list = y_list[:-(len(y_list)%cf.ds_time)]
query, reference = cal_warped_signals(y_list, 'right')

# plot warped signal
# downsample times
xvals, yinterp = plot_warped_signals(reference, query, cf.ds_time)
query2 = pd.DataFrame({'t':xvals, 'q':yinterp})


# calculate the corresponding point pair
query.drop(['shift','t'], axis=1)
query2['close_index'] = 0
true_align_dict = get_true_aligned(cf.ds_time, query, query2)
group_num_dict = get_group_number(true_align_dict, query)


reference_slope_col(reference, cf.ds_time)
slope_col(query2)
d, cost_matrix, acc_cost_matrix, path = dtw(reference[['t', 'avg_slope']].values, query2[['t', 'slope']].values, dist=norm)
get_link_graph(reference, query2, path, -3, 'Downsampled signal with dDTW', '(b) dDTW')
fact_align_dict = get_fact_align(path)
reverse_dict = get_reverse_dict(path)
print("path = "+ str(len(path[0])))
print('group = '+str(get_k_accuracy(true_align_dict, fact_align_dict, group_num_dict)))
print("SS1 of ddtw is "+ str(get_SS1(fact_align_dict, cf.ds_time)))
print("SS2 of ddtw is " + str(get_SS2(fact_align_dict, reverse_dict, cf.ds_time)))