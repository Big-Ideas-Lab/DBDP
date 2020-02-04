import matplotlib.pyplot as plt
import math
from numpy import inf
import pandas as pd
import numpy as np

def get_link(x, y, path, vertical_mov, shift_time):
    # make use of the feature of continuous increasing
    # make sure that x and y are 2D ndArray
    for i in range(len(path[0])):
        head_num = path[0][i]
        tail_num = path[1][i]
        plt.plot((x[head_num][0], y[tail_num][0]+shift_time), (x[head_num][1], y[tail_num][1]+vertical_mov), 'r', alpha=0.5)


def scatter_vis(ecg_hr, ppg_hr, shift_time=0, title=None, lines=False, final_path=None):
    vertical_mov = 0
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.scatter(ecg_hr.utc, ecg_hr.ecg_heart_rate, c='k', marker='.', label='ecg heart rate')
    ax.scatter(ppg_hr.utc + shift_time, ppg_hr.bpm_raw, c='b', label='PPG heart rate')
    ax.legend(fontsize='30')
    a = 0
    print('scatter_vis:')
    if title is not None:
        plt.title(title, fontweight = 'bold')
    if lines == True:
        get_link(ecg_hr.values, ppg_hr.values, final_path, vertical_mov=0, shift_time=shift_time)
    plt.show()

def design_dis(x, y, ecg_val, ppg_val):
    pairs = zip(x, y)
    sum = 0
    for items in pairs:
        print(items[0], items[1], ecg_val[items[0]], math.fabs(ecg_val[items[0]]-ppg_val[items[0]]))
        sum+=math.fabs(ecg_val[items[0]]-ppg_val[items[1]])
    return sum

def get_sing_point(path0, path1):
    path0_count = pd.value_counts(path0)
    path1_count = pd.value_counts(path1)
    return path0_count, path1_count

def ppg_height_devi(ppg_hr,thres):
    ppg_last = len(ppg_hr) - 1
    # add a column
    ppg_hr['h_devi'] = 0
    ppg_hr['h_devi'].iloc[0] = 0
    for i in range(0, ppg_last):
        after_devi=ppg_hr['bpm_raw'].iloc[i+1]-ppg_hr['bpm_raw'].iloc[i]
        pre_devi=ppg_hr['bpm_raw'].iloc[i]-ppg_hr['bpm_raw'].iloc[i-1]
        gap_devi = ppg_hr['bpm_raw'].iloc[i+1]-ppg_hr['bpm_raw'].iloc[i-1]
        abs_gap_devi = np.fabs(gap_devi)
        abs_after_devi=np.fabs(after_devi)
        abs_pre_devi = np.fabs(pre_devi)
        vibrate = abs_after_devi>thres/2 and abs_pre_devi>thres/2 and abs_gap_devi<10
        if abs_after_devi>thres and vibrate==False:
            ppg_hr['h_devi'].iloc[i] = 1
        else:
            ppg_hr['h_devi'].iloc[i] = 0
    for i in range(0, ppg_last-2):
        if ppg_hr['h_devi'].iloc[i] == 1:
            if(ppg_hr['h_devi'].iloc[i+1] == 1 or ppg_hr['h_devi'].iloc[i+2]):
                ppg_hr['h_devi'].iloc[i] = 0
    ppg_hr['h_devi'].iloc[ppg_last] = 1
    return ppg_hr

