import pandas as pd
import math
import os, sys
import linecache
import numpy as np
from parameter_cal import cf
from dtw import dtw
from parameter_cal.utils import get_fact_align, get_reverse_dict, calculate_event, load_data, edge_matching, write_result_file
from parameter_cal.utils import get_SS1, get_SS2, cal_warped_signals, get_upslope_endings, get_downslope_endings
from downsample.utils import get_true_aligned, get_k_accuracy, get_group_number, get_warped_signals


def norm(x, y):
    # return math.fabs(x[1] - y[1])
    return math.fabs(x[1] - y[1]) + math.fabs(x[2] - y[2]) + math.fabs(x[3] - y[3])


def event_dtw(file_name, line_num, df):
    file_name = 'data/' + file_name
    y_list = load_data(file_name, line_num)
    query, reference = cal_warped_signals(y_list)

    reference['upslope'] = 0
    reference['downslope'] = 0

    # plot warped signal
    # downsample times
    xvals, yinterp = get_warped_signals(query, cf.ds_time)

    # calculate the corresponding point pair
    query.drop('shift', axis=1)
    query.drop('t', axis=1)
    query2 = pd.DataFrame({'t': xvals, 'q': yinterp})
    query2['close_index'] = 0
    query2['upslope'] = 0
    query2['downslope'] = 0
    true_align_dict = get_true_aligned(cf.ds_time, query, query2)
    group_num_dict = get_group_number(true_align_dict, query)

    raw_reference_uslope, reference_upslope = get_upslope_endings(reference['q'], cf.refer_percent)
    raw_query_uslope, query_upslope = get_upslope_endings(query2['q'], cf.query_percent)

    raw_reference_downlope, reference_downslope = get_downslope_endings(reference['q'], cf.refer_percent)
    raw_query_downlope, query_downslope = get_downslope_endings(query2['q'], cf.query_percent)

    rising_edge_grps = edge_matching(reference, query2, reference_upslope, query_upslope)
    down_edge_grps = edge_matching(reference, query2, reference_downslope, query_downslope)

    calculate_event(rising_edge_grps, reference, query2, True)
    calculate_event(down_edge_grps, reference, query2, False)
    d, cost_matrix, acc_cost_matrix, path = dtw(reference[['t', 'q', 'upslope', 'downslope']].values,
                                                query2[['t', 'q', 'upslope', 'downslope']].values, dist=norm)
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
    oslist = [f for f in os.listdir(data_dir) if os.path.isfile(data_dir + f)]
    # target_abs_directory = os.getcwd() + '\\csv\\' + 'result.csv'
    # df = pd.read_csv(target_abs_directory, engine='python')
    # print(df)
    # for i in range(0, len(oslist)):
    for i in range(0,84):
        event_result = pd.DataFrame(columns=['Error rate', 'SS1', 'SS2'])
        for j in range(1, 16):
            event_result = event_dtw(oslist[i], j, event_result)
            print('group' + str(j))
        print(event_result.mean())
        print("file" + str(i) + "this is len" + str(len(event_result)))
        write_result_file('result.csv', 'EventDTW', oslist[i], event_result.mean())
