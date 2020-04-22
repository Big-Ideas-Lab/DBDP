import math
import numpy as np
import pandas as pd
from scipy import stats
from scipy.misc import *
from downsample.utils import get_true_aligned, get_group_number, get_k_accuracy
from dtw import dtw
from parameter_cal import cf
from parameter_cal.cf import ds_time
from parameter_cal.utils import cal_warped_signals, plot_warped_signals
from parameter_cal.utils import get_fact_align, get_reverse_dict, get_SS2, get_SS1, get_link_graph, load_data
from sdtw.config import sub_len, nBlocks
from sdtw.utils import cal_descriptor, samplingSequences, norm
from debug.dbd_cf import debug_line, debug_file


# generate warped signal
y_list = load_data(debug_file, debug_line)
query, reference = cal_warped_signals(y_list, 'right')

# plot warped signal
# downsample times
xvals, yinterp = plot_warped_signals(reference, query, cf.ds_time)


# normalize the signal
reference_norm = stats.zscore(reference['q'])
yinterp_norm = stats.zscore(yinterp)

# store the corresponding point pair
query.drop(['t','shift'], axis=1)
query2 = pd.DataFrame({'t': xvals, 'q': yinterp})
query2['close_index'] = 0
true_align_dict = get_true_aligned(cf.ds_time, query, query2)
group_num_dict = get_group_number(true_align_dict, query)

refer_subsequences = samplingSequences(reference_norm, sub_len)
query_subsequences = samplingSequences(yinterp_norm, int(sub_len/cf.ds_time))
refer_descriptors = np.zeros((len(refer_subsequences), nBlocks * 8))
query_descriptors = np.zeros((len(query_subsequences), nBlocks * 8))
refer_nsubsequences = len(refer_subsequences)
query_nsubsequences = len(query_subsequences)

for i in range(refer_nsubsequences):
    sub_seq = refer_subsequences[i]
    refer_descriptors[i] = cal_descriptor(sub_seq, sub_len)

for i in range(query_nsubsequences):
    sub_seq = query_subsequences[i]
    query_descriptors[i] = cal_descriptor(sub_seq, int(sub_len/cf.ds_time))

d, cost_matrix, acc_cost_matrix, path = dtw(refer_descriptors, query_descriptors, dist=norm)
get_link_graph(reference, query2, path, -3, 'Downsampled signal with shapedtw','(d) shapeDTW')
fact_align_dict = get_fact_align(path)
reverse_dict = get_reverse_dict(path)
print("error rate of shapedtw is " + str(get_k_accuracy(true_align_dict, fact_align_dict, group_num_dict)))
print("SS1 of shapedtw is " + str(get_SS1(path, cf.ds_time)))
print("SS2 of shapedtw is " + str(get_SS2(fact_align_dict, reverse_dict, ds_time)))
