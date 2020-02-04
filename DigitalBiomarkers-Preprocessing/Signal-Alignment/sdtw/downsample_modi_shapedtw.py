import pandas as pd
import math
import linecache
import numpy as np
from scipy import stats
from parameter_cal import cf
from dtw import dtw
from scipy.misc import *
from sdtw.config import sub_len, nBlocks
from sdtw.utils import cal_descriptor, samplingSequences, norm
from parameter_cal.utils import get_fact_align, get_reverse_dict, get_SS2, get_SS1, get_link_graph
from parameter_cal.cf import ds_time
from downsample.utils import get_true_aligned, get_group_number, get_k_accuracy
import matplotlib.pyplot as plt


# when x = 0, sigmoid's derivative value is 1/4a
def sigmoid0(x):
    return (4 * 40) / (1 + math.exp(-x / 40))


def gaussian_bump(x, a=1):
    return math.exp(1 / (pow((x / a), 2) - 1))


sigmoid = np.vectorize(sigmoid0)

# generate warped signal
y = linecache.getline('data/Beef_TRAIN', 1)
y_list = y.split(',')
# delete the index
y_list.pop(0)
y_list = [float(item) for item in y_list]
reference = pd.DataFrame(y_list)
reference['t'] = [i for i in range(0, len(reference))]
reference.columns = ['q', 't']
anchor_index = 220
anchor_shift = 10
reference['shift'] = [derivative(sigmoid, math.fabs(anchor_index - i), dx=1e-6) * anchor_shift for i in reference['t']]
query = pd.DataFrame(reference)
query.columns = ['q', 't', 'shift']
query['t2'] = 0.1
temp = []
for i, j in zip(query['t'].values, query['shift'].values):
    temp.append(i - j)
query['t2'] = temp
# add gaussian bump
range_of_gaussian = 40
height_of_gaussian = 1.2
temp = query[(query['t'] < anchor_index + 40) & (query['t'] > anchor_index - 40)].index
for i in temp:
    query.loc[i, 'q'] = query.loc[i, 'q'] + height_of_gaussian * gaussian_bump(i - anchor_index, range_of_gaussian)

# plot warped signal
_, ax = plt.subplots(1, 1, figsize=(20, 10))
ax.scatter(x=query['t'], y=reference['q'], c='b', marker='.', label='before warp')
ax.scatter(x=query['t2'], y=query['q'], c='r', marker='.', label='after warp')
xvals = np.linspace(0, len(query['t']) - 1, math.floor(len(query['t']) / cf.ds_time))
x = query['t2']
y = query['q']
yinterp = np.array(np.interp(xvals, x, y))
xvals = np.array(xvals)
ax.scatter(x=xvals, y=yinterp, marker='.', c='g', label='after interp')
ax.legend(fontsize='30')

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
get_link_graph(reference, query2, path, -3, 'downsampled shapedtw')
fact_align_dict = get_fact_align(path)
reverse_dict = get_reverse_dict(path)
print("error rate of shapedtw is " + str(get_k_accuracy(true_align_dict, fact_align_dict, group_num_dict)))
print("SS1 of shapedtw is " + str(get_SS1(path, cf.ds_time)))
print("SS2 of shapedtw is " + str(get_SS2(fact_align_dict, reverse_dict, ds_time)))
