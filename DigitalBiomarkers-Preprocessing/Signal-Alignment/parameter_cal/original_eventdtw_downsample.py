import pandas as pd
import math
import linecache
import numpy as np
from parameter_cal import cf
from dtw import dtw
import scipy.signal
from scipy.misc import *
from parameter_cal.utils import get_SS1, get_fact_align, get_reverse_dict, get_SS2, calculate_event, get_link_graph, load_data
from parameter_cal.utils import plot_warped_signals, cal_warped_signals, draw_the_peaks, exp_decay
import matplotlib.pyplot as plt
from downsample.utils import get_true_aligned, get_group_number, get_k_accuracy


def sigmoid0(x):
    return (4 * cf.warp_width) / (1 + math.exp(-x / cf.warp_width))


sigmoid = np.vectorize(sigmoid0)


def calculate_event(peak_indexes, df, time):
    slope_length = 20
    slope_weight = 1
    for peak_index in peak_indexes:
        for i in range(1, int(slope_length / time)):
            df.loc[peak_index - i, 'upslope'] = derivative(sigmoid, math.fabs(i * time), dx=1e-6) * slope_weight
            df.loc[peak_index + i, 'downslope'] = derivative(sigmoid, math.fabs(i * time), dx=1e-6) * slope_weight
    for peak_index in peak_indexes:
        df.loc[peak_index, 'upslope'] = 0
        df.loc[peak_index, 'downslope'] = 0


def calculate_event0(peak_indexes, signal, time=1):
    slope_length = 20
    for peak_index in peak_indexes:
        center_time = signal.loc[peak_index, 't']
        signal.loc[peak_index, 'upslope'] = 1
        signal.loc[peak_index, 'downslope'] = 1
        for i in range(1, int(slope_length / time)):
            signal.loc[peak_index + i, 'downslope'] = exp_decay(
                math.fabs(signal.loc[peak_index + i, 't'] - center_time))
            signal.loc[peak_index - i, 'upslope'] = exp_decay(math.fabs(signal.loc[peak_index - i, 't'] - center_time))


def get_matched_pairs(reference, query, refer_peaks, query_peaks, threshold=20):
    refer_len = len(refer_peaks)
    pairs = []
    for i in range(0, refer_len):
        refer_index = refer_peaks[i]
        refer_time = reference.loc[refer_index, 't']
        get = 0
        for index in query_peaks:
            query_time = query.loc[index, 't']
            if math.fabs(query_time - refer_time) > threshold:
                continue
            else:
                pairs.append([refer_index, index])
                get = 1
                break
        if get == 1:
            continue
    return pairs


def norm(x, y):
    # return math.fabs(x[1] - y[1])
    return math.fabs(x[1] - y[1]) + math.fabs(x[2] - y[2]) + math.fabs(x[3] - y[3])


# generate warped signal
y_list = load_data('data/Beef_TRAIN')
query, reference = cal_warped_signals(y_list)

reference['upslope'] = 0
reference['downslope'] = 0

# plot warped signal
# downsample times
xvals, yinterp = plot_warped_signals(reference, query)

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

refer_peak_indexes = scipy.signal.find_peaks(y_list, height=np.mean(y_list), distance=20)
query_peak_indexes = scipy.signal.find_peaks(query2.loc[:, 'q'], height=np.mean(query2.loc[:, 'q']), distance=20)
pairs = get_matched_pairs(reference, query2, refer_peak_indexes[0], query_peak_indexes[0], 20)
refer_indexes = []
query_indexes = []

for i in range(0, len(pairs)):
    refer_indexes.append(pairs[i][0])
    query_indexes.append(pairs[i][1])

draw_the_peaks(reference, query2, refer_indexes, query_indexes, -3, 'Downsampled signal with peaks')
calculate_event(refer_indexes, reference, 1)
calculate_event(query_indexes, query2, cf.ds_time)
d, cost_matrix, acc_cost_matrix, path = dtw(reference[['t', 'q', 'upslope', 'downslope']].values,
                                            query2[['t', 'q', 'upslope', 'downslope']].values, dist=norm)

get_link_graph(reference, query2, path, -3, 'Downsampled signal with EventDTW')
fact_align_dict = get_fact_align(path)
reverse_dict = get_reverse_dict(path)
print("path = " + str(len(path[0])))
print('group = ' + str(get_k_accuracy(true_align_dict, fact_align_dict, group_num_dict)))
print("SS1 of dtw is " + str(get_SS1(fact_align_dict, cf.ds_time)))
print("SS2 of dtw is " + str(get_SS2(fact_align_dict, reverse_dict, cf.ds_time)))
