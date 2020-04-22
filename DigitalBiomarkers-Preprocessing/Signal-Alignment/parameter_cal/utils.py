import linecache
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd
import numpy as np
import os
from scipy import stats
from scipy.misc import *
import debug.dbd_cf
from debug import dbd_cf
from parameter_cal import cf


def gaussian_bump(x, a=1):
    return math.exp(1 / (pow((x / a), 2) - 1))


# when x = 0, sigmoid's derivative value is 1/4a
def sigmoid0(x):
    return (4 * cf.warp_width) / (1 + math.exp(-x / cf.warp_width))


sigmoid = np.vectorize(sigmoid0)


def dsigmoid(warp_width, x):
    return (4 * math.exp(-x/warp_width)) / math.pow((1+math.exp(-x/warp_width)) ,2)


def get_group_devi(item, group_num_dict, true_group_num):
    return math.fabs(group_num_dict[item][0] - true_group_num)


# the key is query, the value is reference
def get_fact_align(path):
    fact_align_dict = {}.fromkeys(range(len(set(path[1]))))
    for i in range(len(set(path[1]))):
        fact_align_dict[i] = np.array([])
    for i in range(len(path[1])):
        dict_index, append_num = path[1][i], path[0][i]
        fact_align_dict[dict_index] = np.append(fact_align_dict[dict_index], append_num)
    return fact_align_dict


def get_reverse_dict(path):
    reverse_dict = {}.fromkeys(range(len(set(path[0]))))
    for i in range(len(set(path[0]))):
        reverse_dict[i] = np.array([])
    for i in range(len(path[0])):
        dict_index, append_num = path[0][i], path[1][i]
        reverse_dict[dict_index] = np.append(reverse_dict[dict_index], append_num)
    return reverse_dict


# abandon
def get_k_accuracy_same(true_align_dict, fact_dict, reference):
    misaligned = 0
    query_number = len(reference)
    consider_num = 0
    for i in range(len(fact_dict)):
        for item in fact_dict[i]:
            consider_num += 1
            misaligned += math.fabs(item - true_align_dict[i])
    print("k sum is " + str(misaligned) + " consider is " + str(consider_num))
    return 2 * misaligned / ((query_number * (query_number - 1)) * (1 + 1))


def get_W(path):
    if set(path[0]) != set(path[1]):
        raise Exception("should not apply W")
    K = len(path[0])
    m = len(set(path[0]))
    print("K = " + str(K) + "and m = " + str(m))
    print("K - m is " + str(K - m))
    return (K - m) / m


def get_SS1(fact_align_dict, ds_time):
    sum_of_deviation = 0
    for i in range(len(fact_align_dict)):
        sum_of_deviation += math.fabs(len(fact_align_dict[i]) - ds_time)
    print("sum of devi SS1 is " + str(sum_of_deviation))
    return sum_of_deviation / len(fact_align_dict)


def get_SS2(fact_align_dict, reverse_dict, ds_time):
    sum_of_deviation = 0
    for i in range(len(fact_align_dict)):
        if len(fact_align_dict[i]) > 1:
            sum_of_deviation += pow(math.fabs(len(fact_align_dict[i]) - ds_time), 2)
        else:
            refer_num = fact_align_dict[i][0]
            sum_of_deviation += pow(math.fabs((1 / len(reverse_dict[refer_num])) - ds_time), 2)
    print("sum of devi SS2 is " + str(sum_of_deviation))
    return sum_of_deviation / len(fact_align_dict)


def get_link_graph(x, y, path, vertical_mov, title=None, xlabel=None):
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.scatter(x['t'], x['q'], s=80,c='k', marker='.', label='Original signal')
    ax.scatter(y['t'], y['q'] + vertical_mov, s=150,c='b', marker='.', label='Warped signal after downsampling')
    # ax.legend(fontsize=40)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(fontsize=40, loc='upper right', edgecolor='inherit', frameon=False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel(xlabel, fontsize=40)
    for i in range(len(path[0])):
        head_num = path[0][i]
        tail_num = path[1][i]
        plt.plot((x['t'].values[head_num], y['t'].values[tail_num]),
                 (x['q'].values[head_num], y['q'].values[tail_num] + vertical_mov), 'r')
    plt.show()


def eliminate_peaks(indexes, seq, width, height):
    seq = np.array(seq)
    st = width - 1
    ed = len(seq) - 1 - width
    reset = []
    for i in indexes:
        if seq[i] - seq[i + width] > height and seq[i] - seq[i - width] > height:
            reset.append(i)
    return np.array(reset)


def find_peaks(seq, width, height, rate=0.85):
    seq = np.array(seq)
    st = width - 1
    ed = len(seq) - 1 - width
    indexes = []
    for i in range(st, ed + 1):
        num_slope_mono = 0
        height_devi = True
        for j in range(i + 1, i + width):
            if seq[j + 1] - seq[j] < 0:
                num_slope_mono += 1
        for j in range(i - width + 1, i):
            if seq[j] - seq[j - 1] > 0:
                num_slope_mono += 1
        if (num_slope_mono / 2 / width) > rate and math.fabs(seq[i + width] - seq[i]) > height and math.fabs(
                seq[i] - seq[i - width]) > height:
            indexes.append(i)
    return indexes


def calculate_event(slope_groups, reference, query, upistrue=True):
    slope_weight = 4  # to ensure that the event intensity is one
    for index, slope_group in slope_groups.iterrows():
        refer_st = slope_group['refer_st'].astype(int)
        refer_ed = slope_group['refer_ed'].astype(int)
        query_st = slope_group['query_st'].astype(int)
        query_ed = slope_group['query_ed'].astype(int)
        refer_sprd_len = math.fabs(reference.loc[refer_st, 't'] - reference.loc[refer_ed, 't'])
        query_sprd_len = math.fabs(query.loc[query_st, 't'] - query.loc[query_ed, 't'])
        if upistrue:
            for i in range(refer_st, refer_ed + 1):
                time_devi = reference.loc[i, 't'] - reference.loc[refer_st, 't']
                reference.loc[i, 'upslope'] = exp_decay(time_devi, 1, refer_sprd_len, 0.1)
            for i in range(query_st, query_ed + 1):
                time_devi = query.loc[i, 't'] - query.loc[query_st, 't']
                query.loc[i, 'upslope'] = exp_decay(time_devi, 1, query_sprd_len, 0.1)
        else:
            for i in range(refer_st, refer_ed + 1):
                time_devi = reference.loc[i, 't'] - reference.loc[refer_st, 't']
                reference.loc[i, 'downslope'] = exp_decay(time_devi, 1, refer_sprd_len, 0.1)
            for i in range(query_st, query_ed + 1):
                time_devi = query.loc[i, 't'] - query.loc[query_st, 't']
                reference.loc[i, 'downslope'] = exp_decay(time_devi, 1, query_sprd_len, 0.1)


def get_true_align(query):
    temp = pd.DataFrame(columns=['refer_true', 'query_true'])
    temp['query_true'] = query['t']
    temp['refer_true'] = query['aligned_index']
    true_align_dict = dict(zip(query['t'], np.zeros((len(query['t']), 1))))
    for i in range(0, len(query['t'])):
        true_align_dict[i][0] = query.loc[i, 'aligned_index']
    return true_align_dict


def read_mit(st, length, path):
    a = pd.read_csv(path, usecols=['MLII'])
    return stats.zscore(a.loc[st:st + length, 'MLII'])


def load_data(name=None, line_num=None):
    y = linecache.getline(name, line_num)
    y_list = y.split(',')
    # delete the index
    y_list.pop(0)
    y_list = [float(item) for item in y_list]
    return y_list


def plot_warped_signals(reference, query, ds_time, vertical_mov=0):
    if ds_time == 1:
        xvals = query['t']
        xvals = np.array(xvals)
    else:
        xvals = np.linspace(query.loc[0,'t2'], query.iloc[-1]['t2'], math.floor(len(query['t']) / cf.ds_time))
        # xvals = np.linspace(0, len(query['t']) - 1, math.floor(len(query['t']) / cf.ds_time))
    plt.figure(figsize=(20, 10))
    plt.scatter(x=query['t'], y=reference['q'], c='b', marker='.', label='before warp')
    plt.scatter(x=query['t2'], y=query['q'] + vertical_mov, c='r', marker='.', label='after warp')
    x = query['t2']
    y = query['q']
    yinterp = np.array(np.interp(xvals, x, y))
    plt.scatter(x=xvals, y=yinterp + vertical_mov, marker='.', c='g', label='after interpolate')
    plt.legend(fontsize='30')
    plt.show()
    return xvals, yinterp


def cal_warped_signals(y_list, anchor_point_pos='center'):
    anchor_index = int((0.5 if anchor_point_pos == 'center' else 2/3)* len(y_list))
    range_of_gaussian = int(0.1*len(y_list))
    reference = pd.DataFrame(y_list)
    reference['t'] = [i for i in range(0, len(reference))]
    reference.columns = ['q', 't']
    reference['shift'] = [dsigmoid(0.1*len(y_list), math.fabs(anchor_index - i)) * 10 for i in reference['t']]
    for i in reference['t']:
        i = int(i)
        if int(anchor_index - i) != 0:
            print(math.pow(math.fabs(anchor_index - i), 2))
            reference.loc[i, 'bad_shift'] = 1/(math.fabs(anchor_index - i)*math.fabs(anchor_index - i))
        else:
            reference.loc[i, 'bad_shift'] = 1/(math.fabs(anchor_index - i+1)*math.fabs(anchor_index - i+1))
    query = pd.DataFrame(reference)
    query.columns = ['q', 't', 'shift', 'bad_shift']
    # process of warping, lay the foundation for interpolation
    query['t2'] = np.array(query['t']) - np.array(query['shift'])
    query['bad_t2'] = np.array(query['t']) - np.array(query['bad_shift'])
    temp = query[
        (query['t'] < anchor_index + range_of_gaussian) & (query['t'] > anchor_index - range_of_gaussian)].index
    for i in temp:
        query.loc[i, 'q'] = query.loc[i, 'q'] + gaussian_bump(i - anchor_index, range_of_gaussian)

    return query, reference


def get_upward_slope_groups(y_list):
    upslope_grp = pd.DataFrame(columns=['st', 'ed', 'length', 'elevation', 'product'])
    # get the upward slope groups
    tvs_y_list = 0
    while tvs_y_list < len(y_list) - 2:
        if y_list[tvs_y_list + 2] > y_list[tvs_y_list + 1] > y_list[tvs_y_list]:
            length = 3
            temp = tvs_y_list + 2
            while temp < len(y_list) - 1:
                if y_list[temp + 1] > y_list[temp]:
                    length += 1
                    temp += 1
                else:
                    break
            upslope_grp.loc[len(upslope_grp)] = [tvs_y_list, temp, length, math.fabs(y_list[temp] - y_list[tvs_y_list]),
                                                 length * math.fabs(y_list[temp] - y_list[tvs_y_list])]
            tvs_y_list = temp
        tvs_y_list += 1
        # transform into int
    upslope_grp[['st', 'ed']] = upslope_grp[['st', 'ed']].astype(int)
    return upslope_grp


def get_upslope_endings(y_list, percent=0.1):
    upslope_grp = get_upward_slope_groups(y_list)

    # # plot the length and elevation
    # plt.scatter(range(0, len(upslope_grp)), upslope_grp['product'].sort_values())
    # plt.xlabel('index')
    # plt.ylabel('product')
    # plt.title('The rank of reference\'s upslope')
    # plt.show()
    # plt.scatter(upslope_grp['length'], upslope_grp['elevation'], c='b', alpha=0.5)
    # plt.xlabel('length')
    # plt.ylabel('elevation')
    # plt.title('The length and elevation of reference\'s upslope')
    # plt.show()

    upslope_grp.sort_values(by=['elevation'], ascending=False, inplace=True)

    if percent is not None:
        selected_upslope_grp = upslope_grp.iloc[0:math.ceil(percent * len(upslope_grp))]
        return upslope_grp, selected_upslope_grp
    else:
        raise Exception("percent is not set")


def get_downward_slope_groups(y_list):
    downslope_grp = pd.DataFrame(columns=['st', 'ed', 'length', 'elevation', 'product'])

    # get the upward slope groups
    tvs_y_list = 0
    while tvs_y_list < len(y_list) - 2:
        if y_list[tvs_y_list + 2] < y_list[tvs_y_list + 1] < y_list[tvs_y_list]:
            length = 3
            temp = tvs_y_list + 2
            while temp < len(y_list) - 1:
                if y_list[temp + 1] < y_list[temp]:
                    length += 1
                    temp += 1
                else:
                    break
            downslope_grp.loc[len(downslope_grp)] = [int(tvs_y_list), temp, length, y_list[temp] - y_list[tvs_y_list],
                                                     length * math.fabs(y_list[temp] - y_list[tvs_y_list])]
            tvs_y_list = temp
        tvs_y_list += 1
    return downslope_grp


def get_downslope_endings(y_list, percent=0.1):
    downslope_grp = get_downward_slope_groups(y_list)

    # # plot the length and elevation
    # plt.scatter(range(0, len(downslope_grp)), downslope_grp['product'].sort_values())
    # plt.xlabel('index')
    # plt.ylabel('product')
    # plt.title('The rank of reference\'s upslope')
    # plt.show()
    # plt.scatter(downslope_grp['length'], downslope_grp['elevation'], c='b', alpha=0.5)
    # plt.xlabel('length')
    # plt.ylabel('elevation')
    # plt.title('The length and elevation of reference\'s upslope')
    # plt.show()

    downslope_grp.sort_values(by=['elevation'], ascending=True, inplace=True)

    if percent is not None:
        selected_dwonslope_grp = downslope_grp.iloc[0:math.ceil(percent * len(downslope_grp))]
        return downslope_grp, selected_dwonslope_grp
    else:
        raise Exception("percent is not set")


def get_event_graph(x, y, refer_up, query_up, refer_down, query_down, vertical_mov, title=None):
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.scatter(x['t'], x['q'], c='k', marker='.', label='reference')
    ax.scatter(y['t'], y['q'] + vertical_mov, c='b', marker='.', label='query')
    for i in range(0, len(refer_up)):
        st = int(refer_up.iloc[i]['st'])
        ed = int(refer_up.iloc[i]['ed'])
        ax.plot(x['t'].loc[st:ed], x['q'].loc[st:ed], color='r')
    for i in range(0, len(query_up)):
        st = int(query_up.iloc[i]['st'])
        ed = int(query_up.iloc[i]['ed'])
        ax.plot(y['t'].loc[st:ed], y['q'].loc[st:ed] + vertical_mov, color='r')
    for i in range(0, len(refer_down)):
        st = int(refer_down.iloc[i]['st'])
        ed = int(refer_down.iloc[i]['ed'])
        ax.plot(x['t'].loc[st:ed], x['q'].loc[st:ed], color='g')
    for i in range(0, len(query_down)):
        st = int(query_down.iloc[i]['st'])
        ed = int(query_down.iloc[i]['ed'])
        ax.plot(y['t'].loc[st:ed], y['q'].loc[st:ed] + vertical_mov, color='g')
    plt.title(label=title, fontsize='30')
    plt.show()


def draw_the_peaks(reference, query, refer_peaks, query_peaks, vertical_mov=-3, ds_time=1):
    plt.subplots(figsize=(20, 10))
    plt.scatter(x=reference['t'], y=reference['q'], c='k', marker='.', label='reference')
    plt.scatter(x=query['t'], y=query['q'] + vertical_mov, c='b', marker='.', label='query')
    plt.scatter(x=reference.loc[refer_peaks, 't'], y=reference.loc[refer_peaks, 'q'], c='r', marker='*')
    plt.scatter(x=query.loc[query_peaks, 't'], y=query.loc[query_peaks, 'q'] + vertical_mov, c='r', marker='*')
    plt.title("Peaks pair picture", fontsize=15)
    plt.show()


def exp_decay(t, init=1, m=100.0, finish=0.1):
    alpha = np.log(init / finish) / m
    l = - np.log(init) / alpha
    decay = np.exp(-alpha * (t + l))
    return decay


def edge_matching(reference, query, refer_up, query_up):
    rising_edge_grps = pd.DataFrame(columns=['refer_st', 'refer_ed', 'query_st', 'query_ed'])
    for q_i in range(0, len(query_up)):
        query_st = query.loc[query_up.iloc[q_i]['st'], 't']
        query_ed = query.loc[query_up.iloc[q_i]['ed'], 't']
        query_devi = math.fabs(query_st-query_ed)
        for r_i in range(0, len(refer_up)):
            refer_st = reference.loc[refer_up.iloc[r_i]['st'], 't']
            refer_ed = reference.loc[refer_up.iloc[r_i]['ed'], 't']
            refer_devi = math.fabs(refer_ed - refer_st)
            if math.fabs(refer_st - query_st) < 0.5*math.fabs(refer_st-refer_ed) and math.fabs(refer_ed - query_ed) < 0.5*math.fabs(refer_st-refer_ed):
                rising_edge_grps.loc[len(rising_edge_grps)] = [refer_up.iloc[r_i]['st'], refer_up.iloc[r_i]['ed'],
                                                               query_up.iloc[q_i]['st'], query_up.iloc[q_i]['ed']]
                break
    return rising_edge_grps


def write_result_file(target_name, method_name, src_name, result_series):
    target_abs_directory = os.getcwd() + '\\csv\\' + target_name
    if not os.path.exists(target_abs_directory):
        df = pd.DataFrame(columns=pd.MultiIndex.from_product([['EventDTW', 'DTW', 'shapeDTW', 'dDTW'],['error rate', 'SS1', 'SS2']]))
        df.loc[src_name, method_name] = result_series.values
        df.to_csv(target_abs_directory, header=True, index=True)
    else:
        df = pd.read_csv(target_abs_directory, engine='python', header=[0,1], index_col=0)
        df.loc[src_name, method_name] = result_series.values
        df.to_csv(target_abs_directory, header=True, index=True)