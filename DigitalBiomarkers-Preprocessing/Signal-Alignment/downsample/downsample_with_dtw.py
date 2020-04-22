import pandas as pd
import math
import linecache
import numpy as np
from parameter_cal import cf
from dtw import dtw
import os
from scipy.misc import *
from parameter_cal.utils import get_SS1, get_fact_align, get_reverse_dict, get_SS2, write_result_file
from parameter_cal.utils import load_data, cal_warped_signals
from downsample.utils import get_true_aligned, get_group_number, get_k_accuracy, get_warped_signals


def norm(x, y):
    return math.fabs(x[1] - y[1])


def pkg_dtw(file_name, line_num, df):
    file_name = 'data/' + file_name
    y_list = load_data(file_name, line_num)
    query, reference = cal_warped_signals(y_list)

    # plot warped signal
    # downsample times
    xvals, yinterp = get_warped_signals(query, cf.ds_time)

    # calculate the corresponding point pair
    query.drop(['shift', 't'], axis=1)
    query2 = pd.DataFrame({'t': xvals, 'q': yinterp})
    query2['close_index'] = 0
    true_align_dict = get_true_aligned(cf.ds_time, query, query2)
    group_num_dict = get_group_number(true_align_dict, query)

    d, cost_matrix, acc_cost_matrix, path = dtw(reference[['t', 'q']].values, query2[['t', 'q']].values, dist=norm)
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
            event_result = pkg_dtw(oslist[i], j, event_result)
        print(event_result.mean())
        print('file'+str(i))
        write_result_file('result.csv', 'DTW', oslist[i], event_result.mean())