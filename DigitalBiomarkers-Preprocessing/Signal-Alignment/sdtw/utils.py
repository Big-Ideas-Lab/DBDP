import numpy as np
import math
from sdtw.config import nBlocks, nbins, dx_scale
import matplotlib.pyplot as plt


def whichInterval(angles, ang):
    if ang < angles[0]:
        return 0
    if ang >= angles[-1]:
        return len(angles) - 2
    for i in range(len(angles)):
        if angles[i] <= ang < angles[i + 1]:
            return i


# the number of bins is 8
angles = np.linspace(-math.pi / 2, math.pi / 2, nbins + 1)
deg_angles = np.linspace(-180 / 2, 180 / 2, nbins + 1)
center_angles = np.array([])
for i in range(len(deg_angles) - 1):
    center_angles = np.append(center_angles, (angles[i] + angles[i + 1]) / 2)
    deg_center_angles = np.append(center_angles, (deg_angles[i] + deg_angles[i + 1]) / 2)


def cal_descriptor(y_list, sub_len):
    y_list = np.insert(y_list, 0, y_list[0])
    y_list = np.append(y_list, y_list[-1])
    sCell = math.ceil(sub_len / 2) - 1
    idx_start = 0

    descriptor = np.zeros((nBlocks, nbins))

    for i in range(nBlocks):
        for j in range(sCell):
            idx = i * sCell + j
            cidx = idx_start + idx
            # centered gradient
            sidx = cidx - 1
            eidx = cidx + 1
            if (sidx < 0) or (eidx > sub_len - 1):
                continue
            dx = 2 * dx_scale
            dy = y_list[eidx] - y_list[sidx]
            ang = math.atan2(dy, dx)
            mag = dy / dx

            n = whichInterval(angles, ang)
            if n == 0 and ang < center_angles[0]:
                descriptor[i, n] = descriptor[i, n] + math.fabs(mag)
            elif n == len(center_angles) - 1 and ang >= center_angles[len(center_angles) - 1]:
                descriptor[i, n] = descriptor[i, n] + math.fabs(mag)
            else:
                if math.fabs(angles[n] - ang) > math.fabs(angles[n + 1] - ang):
                    ang1 = center_angles[n]
                    ang2 = center_angles[n + 1]

                    descriptor[i, n] = descriptor[i, n] + math.fabs(mag) * math.cos(ang1 - ang)
                    descriptor[i, n + 1] = descriptor[i, n + 1] + math.fabs(mag) * math.cos(ang2 - ang)
                else:
                    ang1 = center_angles[n - 1]
                    ang2 = center_angles[n]

                    descriptor[i, n - 1] = descriptor[i, n - 1] + math.fabs(mag) * math.cos(ang1 - ang)
                    descriptor[i, n] = descriptor[i, n] + math.fabs(mag) * math.cos(ang2 - ang)

    return descriptor.reshape(descriptor.size)


def samplingSequences(sequences, sub_len):
    info = np.zeros((len(sequences), sub_len))
    original_len = len(sequences)
    if sub_len % 2 == 0:
        sequences = np.insert(sequences, 0, np.ones((math.floor(sub_len / 2) - 1,)) * sequences[0])
        sequences = np.append(sequences, np.ones((math.floor(sub_len / 2) - 1,)) * sequences[-1])
        stidx = math.floor(sub_len / 2) - 1
        edidx = len(sequences) - math.floor(sub_len / 2)
        # there is a difference between odd and equal
        for i in range(stidx, edidx):
            infoidx = i - math.floor(sub_len / 2) + 1
            info[infoidx] = sequences[i - math.floor(sub_len / 2) + 1:i + math.floor(sub_len / 2) + 1]
    else:
        sequences = np.insert(sequences, 0, np.ones((math.floor(sub_len / 2),)) * sequences[0])
        sequences = np.append(sequences, np.ones((math.floor(sub_len / 2),)) * sequences[-1])
        stidx = math.floor(sub_len / 2)
        edidx = len(sequences) - math.floor(sub_len / 2) - 1
        for i in range(stidx, edidx + 1):
            infoidx = i - math.floor(sub_len / 2)
            info[infoidx] = sequences[i - math.floor(sub_len / 2):i + math.floor(sub_len / 2) + 1]

    return info


# how to measure the distance
def norm(reference, query):
    return np.linalg.norm(reference - query)


def cal_refer_query_descriptor(reference_norm, yinterp_norm, sub_len):
    refer_subsequences = samplingSequences(reference_norm, sub_len)
    query_subsequences = samplingSequences(yinterp_norm, sub_len)
    refer_descriptors = np.zeros((len(refer_subsequences), nBlocks * 8))
    query_descriptors = np.zeros((len(query_subsequences), nBlocks * 8))
    refer_nsubsequences = len(refer_subsequences)
    query_nsubsequences = len(query_subsequences)

    for i in range(refer_nsubsequences):
        sub_seq = refer_subsequences[i]
        refer_descriptors[i] = cal_descriptor(sub_seq, sub_len)

    for i in range(query_nsubsequences):
        sub_seq = query_subsequences[i]
        query_descriptors[i] = cal_descriptor(sub_seq, sub_len)

    return refer_descriptors, query_descriptors
