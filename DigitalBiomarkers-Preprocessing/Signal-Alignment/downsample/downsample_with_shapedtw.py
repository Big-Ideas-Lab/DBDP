import pandas as pd
import math
import linecache
import numpy as np
from scipy import stats
from parameter_cal import cf
from dtw import dtw
import os
from scipy.misc import *
from sdtw.config import sub_len, nBlocks
from sdtw.utils import cal_descriptor, samplingSequences, norm
from parameter_cal.utils import get_fact_align, get_reverse_dict, get_SS2, get_SS1, get_link_graph, load_data
from parameter_cal.utils import load_data, cal_warped_signals, write_result_file
from downsample.utils import get_true_aligned, get_group_number, get_k_accuracy, get_warped_signals


def pkg_shapedtw(file_name, line_num, df):
    file_name = 'data/' + file_name
    y_list = load_data(file_name, line_num)
    query, reference = cal_warped_signals(y_list)

    # plot warped signal
    xvals, yinterp = get_warped_signals(query, cf.ds_time)

    # normalize the signal
    reference_norm = stats.zscore(reference['q'])
    yinterp_norm = stats.zscore(yinterp)

    # store the corresponding point pair
    query.drop(['shift', 't'], axis=1)
    query2 = pd.DataFrame({'t': xvals, 'q': yinterp})
    query2['close_index'] = 0
    true_align_dict = get_true_aligned(cf.ds_time, query, query2)
    group_num_dict = get_group_number(true_align_dict, query)

    refer_subsequences = samplingSequences(reference_norm, sub_len)
    query_subsequences = samplingSequences(yinterp_norm, int(sub_len / cf.ds_time))
    refer_descriptors = np.zeros((len(refer_subsequences), nBlocks * 8))
    query_descriptors = np.zeros((len(query_subsequences), nBlocks * 8))
    refer_nsubsequences = len(refer_subsequences)
    query_nsubsequences = len(query_subsequences)

    for i in range(refer_nsubsequences):
        sub_seq = refer_subsequences[i]
        refer_descriptors[i] = cal_descriptor(sub_seq, sub_len)

    for i in range(query_nsubsequences):
        sub_seq = query_subsequences[i]
        query_descriptors[i] = cal_descriptor(sub_seq, int(sub_len / cf.ds_time))

    d, cost_matrix, acc_cost_matrix, path = dtw(refer_descriptors, query_descriptors, dist=norm)
    fact_align_dict = get_fact_align(path)
    reverse_dict = get_reverse_dict(path)
    error_rate = get_k_accuracy(true_align_dict, fact_align_dict, group_num_dict)
    SS1 = get_SS1(fact_align_dict, cf.ds_time)
    SS2 = get_SS2(fact_align_dict, reverse_dict, cf.ds_time)
    df.loc[line_num] = [error_rate, SS1, SS2]
    return df

if __name__ == "__main__":
    # generate warped signal
    os.chdir(os.path.abspath('..'))
    data_dir = os.getcwd() + '\\data\\'
    oslist = [f for f in os.listdir(data_dir) if os.path.isfile(data_dir+f)]
    # for i in range(0, len(oslist)):
    for i in range(0, 84):
        event_result = pd.DataFrame(columns=['Error rate','SS1','SS2'])
        for j in range(1, 16):
            event_result = pkg_shapedtw(oslist[i], j, event_result)
        print(event_result.mean())
        print('file'+str(i))
        write_result_file('result.csv', 'shapeDTW', oslist[i], event_result.mean())
