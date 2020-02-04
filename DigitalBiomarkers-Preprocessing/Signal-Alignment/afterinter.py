import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial.distance import seuclidean
from biosppy.signals import ecg
from dtw import dtw
from visualization import scatter_vis, design_dis
import math


# In[2]:
def get_link(x, y, path, vertical_mov, shift_time):
    # make use of the feature of continuous increasing
    for i in range(len(path[0])):
        head_num = path[0][i]
        tail_num = path[1][i]
        plt.plot((x[head_num][0], y[tail_num][0]), (x[head_num][1], y[tail_num][1]+vertical_mov), 'r')

def hdf_to_dict(hdf_file):
    # Read all the keys in the file
    with pd.HDFStore(hdf_file, mode='r') as hdf:
        keys = hdf.keys()

    # Read all tables, store in dictionary
    data = {}
    for key in keys: data[key] = pd.read_hdf(hdf_file, key)
    return data

ecg_analysis_file = pd.read_csv('csv/ecg_analysis.csv')
ecg_analysis = pd.DataFrame(ecg_analysis_file)

alg_hdf = '/home/jyh/CS/ecg/ibeat/ibeat/Subject044/SE_GENERIC_DATA_EVENT_6671_001/Subject044_Device010_ibeat_alg.hdf'
alg_data = hdf_to_dict(alg_hdf)

ppg_analysis = alg_data['/pulse_rate_alg']
# pick up utc and bpm_raw
ppg_analysis = ppg_analysis.loc[:, ['utc', 'bpm_raw']]

ecg_analysis = ecg_analysis.loc[:, ['utc', 'ecg_heart_rate']]
ecg_analysis.utc.values

# In[10]:


from scipy import signal

ppg_st = 1527109440
ppg_chunk_len = 270
# ppg_st = 1527109395
# ppg_chunk_len = 30
ecg_match_len = ppg_chunk_len
abs_drift_val = 20
shift_time = 0
min_d = 0
final_matrix = 0
final_path = 0
final_ppg_hr = 0

ppg_et = ppg_st + ppg_chunk_len

shift = 0
ecg_st = ppg_st + shift
ecg_et = ecg_st + ecg_match_len

ecg_hr = ecg_analysis[(ecg_analysis.utc > ecg_st) & (ecg_analysis.utc < ecg_et)]
ppg_hr = ppg_analysis[(ppg_analysis.utc > ppg_st) & (ppg_analysis.utc < ppg_et)]

# ppg_value after interpolate
ecg_utc_old = ecg_hr.utc.values
ppg_utc_old = ppg_hr.utc.values
ppg_bpm_old = ppg_hr.bpm_raw.values

ppg_bpm_new = np.interp(ecg_utc_old, ppg_utc_old, ppg_bpm_old)
ppg_analysis_inter = pd.DataFrame(np.vstack((ecg_hr.utc, ppg_bpm_new)).transpose())
ppg_analysis_inter = ppg_analysis_inter.rename(columns={0: 'utc', 1: 'bpm_raw'})
ppg_hr = ppg_analysis_inter

# utc_var = np.hstack((ecg_hr.utc.values, ppg_hr.utc.values)).var()
# rate_var = np.hstack((ecg_hr.ecg_heart_rate.values, ppg_hr.bpm_raw.values)).var()

# print(utc_var, rate_var)

# norm = lambda x, y: seuclidean(x, y, [utc_var,rate_var])

# norm = dist_with_punish
norm = lambda x, y: math.fabs(x[1] - y[1])

# changed Manhattan distance
# norm = lambda x, y: math.fabs(x[1]-y[1])+0.1*math.fabs(x[0]-y[0])

# norm = lambda x, y: np.abs(x - y)
# only absolute value
# d, cost_matrix, acc_cost_matrix, path = dtw(ecg_hr.ecg_heart_rate.values.reshape(-1,1), ppg_hr.bpm_raw.values.reshape(-1,1), dist=norm)

# include time variant utc26
d, cost_matrix, acc_cost_matrix, path = dtw(ecg_hr.values, ppg_hr.values, dist=norm)

shift_time = shift
min_d = d
final_matrix = acc_cost_matrix
final_path = path
final_ppg_hr = ppg_hr
print("final path belongs to " + str(final_path[1].shape))


print(shift_time)
plt.imshow(acc_cost_matrix.T, origin='lower', cmap='gray', interpolation='nearest')
plt.plot(final_path[0], final_path[1], 'r')
plt.show()


fig, ax = plt.subplots(figsize=(20, 10))

# ax[0].set_xlim([1527108100,1527108500])

# shift_time = -23 prove sensitivity
print(shift_time)

ecg_hr = ecg_analysis[
    (ecg_analysis.utc > ppg_st + shift_time) & (ecg_analysis.utc < ppg_st + shift_time + ppg_chunk_len)]
ppg_hr = final_ppg_hr
# this dtw is used for modification
d, cost_matrix, acc_cost_matrix, path = dtw(ecg_hr.values, ppg_hr.values, dist=norm)
vertical_mov = -150

# the x, y should be in the ssame order as dtw function
get_link(ecg_hr.values, ppg_hr.values, final_path, vertical_mov, shift_time)

# when ecg is at 1st, ppg at 2nd
ax.scatter(ecg_hr.utc, ecg_hr.ecg_heart_rate, c='k', marker='.')
ax.scatter(ppg_hr.utc, ppg_hr.bpm_raw+vertical_mov, label='PPG Pulse Rate', c='b')

plt.show()

scatter_vis(ecg_hr, ppg_hr, 0, 'real shift graph')
plt.show()

dis = design_dis(final_path[0], final_path[1], ecg_hr.ecg_heart_rate.values, ppg_hr.bpm_raw.values)
print(dis)


