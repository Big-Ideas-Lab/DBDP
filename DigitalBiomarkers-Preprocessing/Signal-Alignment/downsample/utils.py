import numpy as np
import math
from parameter_cal.utils import get_group_devi, get_SS1, get_SS2
from parameter_cal import cf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


def get_group_len(query_st, query2_checkpoint, ds_time, query, query2):
    group_len = 0
    for i in range(0, ds_time):
        group_len += math.sqrt(pow((query2['t'][query2_checkpoint] - query['t2'][i+query_st]), 2) + pow((query2['q'][query2_checkpoint] - query['q'][i+query_st]), 2))
    return group_len


def get_true_aligned(ds_time, query, query2):
    if math.floor(ds_time) == math.ceil(ds_time):
        ds_time = int(ds_time)
    dict = {}.fromkeys(range(0, len(query2['t'])))
    for i in range(len(query2['t'])):
        dict[i] = np.array([])
    # find the closest index
    for i in range(len(query2)):
        for j in range(len(query['t']) - 1):
            if query['t2'][j] <= query2['t'][i] < query['t2'][j + 1]:
                print(i, j, query['q'][j], query2['q'][i])
                if abs(query2['q'][i] - query['q'][j]) < abs(query2['q'][i] - query['q'][j + 1]):
                    query2.loc[i, 'close_index'] = j
                    dict[i] = np.append(dict[i], j)
                else:
                    query2.loc[i, 'close_index'] = j + 1
                    dict[i] = np.append(dict[i], j+1)
        if query2['t'][i] > query['t2'].iloc[-1]:
            query2.loc[i, 'close_index'] = len(query) - 1
        elif query2['t'][i] < query['t2'].iloc[0]:
            query2.loc[i, 'close_index'] = 0
    dict[len(query2['t'])-1] = np.array([len(query)-1])
    for i in range(len(query2['t'])):
        min_len = np.inf
        center = int(dict[i][0])
        for j in range(-ds_time+1, 1):
            st, ed = center+j,center+j+ds_time-1
            if st < 0 or ed >= len(query['t2']):
                continue
            print(i, st, center, j)
            group_len = get_group_len(st, i, ds_time, query, query2)
            if group_len < min_len:
                dict[i] = np.array(list(range(center+j, center+j+ds_time)))
                min_len = group_len
    return dict


def get_group_number(true_align_dict, query):
    diction = {}.fromkeys(range(0, len(query['q'])))
    for i in range(len(query['q'])):
        diction[i] = np.array([])
    diction = {}.fromkeys(range(0, len(query['q'])))
    for i in range(len(query['q'])):
        diction[i] = np.array([])
    for i in range(len(true_align_dict)):
        for item in true_align_dict[i]:
            diction[item] = np.append(diction[item], i)
    # modify those that did not find their group
    for i in range(len(diction)):
        if len(diction[i]) == 0:
            diction[i] = np.append(diction[i], diction[i - 1][0])
    return diction


def get_k_accuracy(true_align_dict, fact_align_dict, group_num_dict):
    sum = 0
    consider_num = 0
    query_number = len(fact_align_dict)
    for i in range(len(fact_align_dict)):
        for item in fact_align_dict[i]:
            consider_num += 1
            if item in true_align_dict[i]:
                sum += 0
            else:
                # search the group number
                group_devi = get_group_devi(item, group_num_dict,i)
                sum += group_devi
            # sum+=min(np.abs(item-true_align_dict[i]))
    return 2 * sum / ((query_number * (query_number - 1)) * (1+math.fabs(cf.ds_time)))


def slope_col(query):
    # calculate the slope of query
    query_last = len(query) - 1
    query['slope'] = 0
    query.loc[1, 'slope'] = ((query.loc[1, 'q'] - query.loc[0, 'q']) + ((query.loc[2 , 'q'] - query.loc[1, 'q']) / 2)) / 2
    query.loc[0, 'slope'] = query.loc[1, 'slope']
    for i in range(2, query_last - 1):
        query.loc[i, 'slope'] = ((query.loc[i, 'q'] -query.loc[i-1, 'q']) + ((query.loc[i+1, 'q'] - query.loc[i, 'q']) / 2)) / 2
        query.loc[query_last - 1, 'slope'] = ((query.loc[query_last - 1, 'q'] - query.loc[query_last - 2, 'q']) + (
                    (query.loc[query_last, 'q'] - query.loc[query_last - 1, 'q']) / 2)) / 2
        query.loc[query_last, 'slope'] = query.loc[query_last - 1, 'slope']


def reference_slope_col(query, ds_time):
    slope_col(query)
    query['avg_slope'] = 0
    left_right = ds_time
    st = 0 + left_right
    ed = len(query) - 1 - left_right
    for i in range(0, ed+1):
        query.loc[i, 'avg_slope'] = (query.loc[i+left_right, 'q'] - query.loc[i, 'q']) / 2
    for i in range(ed+1, len(query) - 1):
        query.loc[i, 'avg_slope'] = query.loc[i, 'slope']


def get_warped_signals(query, ds_time):
    if ds_time == 1:
        xvals = query['t']
        xvals = np.array(xvals)
    else:
        xvals = np.linspace(query.loc[0,'t2'], query.iloc[-1]['t2'], math.floor(len(query['t']) / cf.ds_time))
    x = query['t2']
    y = query['q']
    yinterp = np.array(np.interp(xvals, x, y))
    return xvals, yinterp


def connect_edges(rising_edge_grps, raw_reference_uslope):
    for i in range(len(rising_edge_grps)):
        st_conct = int(rising_edge_grps.loc[i, 'refer_st'])
        ed_conct = int(rising_edge_grps.loc[i, 'refer_ed'])
        for j in range(len(raw_reference_uslope)):
            if math.fabs(st_conct - raw_reference_uslope.iloc[j]['ed']) <= 2:
                rising_edge_grps.iloc[i]['refer_st'] = raw_reference_uslope.iloc[j]['st']
            elif math.fabs(ed_conct - raw_reference_uslope.iloc[j]['st']) <= 2:
                rising_edge_grps.iloc[i]['refer_ed'] = raw_reference_uslope.iloc[j]['ed']
    return rising_edge_grps


def get_matched_graph(rising_edge_grps, down_edge_grps, x, y, vertical_mov, title=None):
    fig, ax = plt.subplots(1, 1, figsize=(25, 12))
    legend_elements = [Line2D([0], [0], marker='o',color='w',label='               ',markerfacecolor='black',markersize=15),
                       Line2D([0], [0], marker='o',color='w',label='                                                    ',markerfacecolor='blue',markersize=20),
                       Line2D([0], [0], color='r', lw=4),
                       Line2D([0], [0], color='cyan', lw=4)
                       ]
    ax.scatter(x['t'], x['q'], c='k', marker='.')
    ax.scatter(y['t'], y['q'] + vertical_mov, c='b', s=160, marker='.')
    b = ax.get_position()
    ax.legend(ncol=2, handles = legend_elements, fontsize=40, frameon=False, loc='lower left', bbox_to_anchor=(0,1.05))
    for i in range(0, len(rising_edge_grps)):
        refer_st = int(rising_edge_grps.iloc[i]['refer_st'])
        refer_ed = int(rising_edge_grps.iloc[i]['refer_ed'])
        query_st = int(rising_edge_grps.iloc[i]['query_st'])
        query_ed = int(rising_edge_grps.iloc[i]['query_ed'])
        ax.plot(x['t'].loc[refer_st:refer_ed], x['q'].loc[refer_st:refer_ed], color='r', linewidth=5)
        ax.plot(y['t'].loc[query_st:query_ed], y['q'].loc[query_st:query_ed] + vertical_mov, color='r', linewidth=5)

    for i in range(0, len(down_edge_grps)):
        refer_st = int(down_edge_grps.iloc[i]['refer_st'])
        refer_ed = int(down_edge_grps.iloc[i]['refer_ed'])
        query_st = int(down_edge_grps.iloc[i]['query_st'])
        query_ed = int(down_edge_grps.iloc[i]['query_ed'])
        ax.plot(x['t'].loc[refer_st:refer_ed], x['q'].loc[refer_st:refer_ed], color='cyan', linewidth=5)
        ax.plot(y['t'].loc[query_st:query_ed], y['q'].loc[query_st:query_ed] + vertical_mov, color='cyan', linewidth=5)
    ax.set_title(title, fontsize='30')
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()