import linecache
import numpy as np
import scipy.signal
import pandas as pd
import matplotlib.pyplot as plt
from parameter_cal import cf
import math
from parameter_cal.utils import find_peaks, eliminate_peaks

def get_convex(indexes, inverse_indexes, combined_indexes):
    convex_group = []
    for i in range(len(combined_indexes) - 2):
        if combined_indexes[i] in inverse_indexes \
                and combined_indexes[i + 1] in indexes \
                and combined_indexes[i + 2] in inverse_indexes:
            convex_group.append([combined_indexes[i], combined_indexes[i + 1], combined_indexes[i + 2]])
    return convex_group


def plot_convex(st, md, ed, series):
    _, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(series[st:ed], 'b', lw=1)
    ax.plot(md - st, series[md], '+', mfc=None, mec='r', mew=2, ms=8)


def plot_peaks(x, indexes, algorithm=None, mph=None, mpd=None):
    """Plot results of the peak dectection."""
    _, ax = plt.subplots(1, 1, figsize=(8, 4))
    ax.plot(x, 'b', lw=1)
    if indexes.size:
        label = 'peak'
        label = label + 's' if indexes.size > 1 else label
        ax.plot(indexes, x[indexes], '+', mfc=None, mec='r', mew=1, ms=4,
                label='%d %s' % (indexes.size, label))
        ax.legend(loc='best', framealpha=.5, numpoints=1)
    ax.set_xlim(-.02 * x.size, x.size * 1.02 - 1)
    ymin, ymax = x[np.isfinite(x)].min(), x[np.isfinite(x)].max()
    yrange = ymax - ymin if ymax > ymin else 1
    ax.set_ylim(ymin - 0.1 * yrange, ymax + 0.1 * yrange)
    ax.set_xlabel('Data #', fontsize=14)
    ax.set_ylabel('Amplitude', fontsize=14)
    ax.set_title('%s (mph=%s, mpd=%s)' % (algorithm, mph, mpd))


file = linecache.getline('data/Beef_TRAIN', 1)
y_list = file.split(',')
# delete the index
y_list.pop(0)
y_list = [float(item) for item in y_list]
upslope_grp = pd.DataFrame(columns=['st', 'ed', 'length', 'height'])

# get the upward slope groups
tvs_y_list = 0
while tvs_y_list < len(y_list)-2:
    if y_list[tvs_y_list+2] > y_list[tvs_y_list+1] > y_list[tvs_y_list]:
        length = 3
        temp = tvs_y_list + 2
        while temp < len(y_list)-1:
            if y_list[temp+1]>y_list[temp]:
                length+=1
                temp+=1
            else:
                break
        upslope_grp.loc[len(upslope_grp)] = [tvs_y_list,temp,length,math.fabs(y_list[temp]-y_list[tvs_y_list])]
        tvs_y_list = temp
    tvs_y_list += 1

cp_y_list = y_list
inverse_y_list = [-item for item in y_list]
# inverse_y_list = scipy.signal.savgol_filter(inverse_y_list, 11, 3)
cp_ivs_y_list = inverse_y_list
# should be 53 91 297 334 391
# should be 73 263 373
indexes, _ = scipy.signal.find_peaks(y_list, height=np.mean(y_list), distance=20)
inverse_indexes, _ = scipy.signal.find_peaks(inverse_y_list, height=-0.5, distance=cf.warp_width)

indexes = np.array(indexes)
inverse_indexes = np.array(inverse_indexes)
combined_indexes = np.sort(np.append(indexes, inverse_indexes))

convex_group = get_convex(indexes, inverse_indexes, combined_indexes)
convex_list = []
for i in range(len(convex_group)):
    convex_list.append(y_list[convex_group[i][0]:convex_group[i][2]])
    plot_convex(0, convex_group[i][1] - convex_group[i][0], convex_group[i][2] - convex_group[i][0], convex_list[i])
    len_pre = convex_group[i][2] - convex_group[i][1]
    pre_x = np.linspace(0, len_pre, len_pre + 1) * 2
    after_x = np.linspace(0, 2 * len_pre, 2 * len_pre + 1)
    print(convex_group[i])

plot_peaks(np.array(y_list), indexes, mph=1, mpd=1.8, algorithm='scipy.signal.find_peaks')
plot_peaks(np.array(inverse_y_list), inverse_indexes, mph=1, mpd=1.9, algorithm='scipy.signal.find_peaks')
plt.show()

indexes2 = eliminate_peaks(indexes, y_list, 10, 0.25)
plot_peaks(np.array(y_list), indexes2, mph=1, mpd=1.9, algorithm='scipy.signal.find_peaks')
plt.show()
