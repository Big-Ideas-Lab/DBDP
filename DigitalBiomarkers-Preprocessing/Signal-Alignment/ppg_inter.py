import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.spatial.distance import seuclidean
from dtw import dtw
from visualization import scatter_vis
import math

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

ppg_st = 1527109440
ppg_chunk_len = 270
ecg_match_len = ppg_chunk_len
abs_drift_val = 20
shift_time = 0
min_d = 0
final_matrix = 0
final_path = 0

ppg_et = ppg_st + ppg_chunk_len

ecg_hr = ecg_analysis[(ecg_analysis.utc > ppg_st) & (ecg_analysis.utc < ppg_et)]
ppg_hr = ppg_analysis[(ppg_analysis.utc > ppg_st) & (ppg_analysis.utc < ppg_et)]

# ppg_value after interpolate
ecg_utc_old = ecg_hr.utc.values
ppg_utc_old = ppg_hr.utc.values
ppg_bpm_old = ppg_hr.bpm_raw.values

ppg_bpm_new = np.interp(ecg_utc_old, ppg_utc_old, ppg_bpm_old)
ppg_analysis_inter = pd.DataFrame(np.vstack((ecg_hr.utc, ppg_bpm_new)).transpose())
ppg_analysis_inter = ppg_analysis_inter.rename(columns={0:'utc',1:'bpm_raw'})
ppg_hr_new = ppg_analysis_inter[(ppg_analysis_inter.utc > ppg_st) & (ppg_analysis_inter.utc < ppg_et)]

fig, ax = plt.subplots(figsize=(20, 10))

ax.scatter(ppg_hr.utc, ppg_hr.bpm_raw, c='k', marker='.')
ax.scatter(ppg_hr_new.utc, ppg_hr_new.bpm_raw-10, label='PPG Pulse Rate', c='b', marker='.')

plt.show()

