def hrv(file, complete_sequence="false", threshold=0.1, x=50, correction="false", fs=4):
    '''(file, complete_sequence="false", threshold=0.1,  x=50, correction="false") -> {HRV Metrics}

    Returns a dictionary of time and frequency domain metrics

    file - is the data file with the first column as time, and the second column as IBI
    complete_sequence - takes a true or false argument for whether you require the longest sequence of non missing data
    threshold - is used to set the permissible difference between IBI
    x - is the time in milliseconds for calculating pNN and NN
    correction - is to take care of outliers, should be used carefully
    fs - for sample rate interpolation in frequency domain

    example:

    >>> h = hrv("ibi.csv")

    {'MeanRR': 1033.9,
     'MeanHR': 58.6,
     'MinHR': 48.1,
     'MaxHR': 89.5,
     'SDNN': 103.1,
     'RMSSD': 70.9,
     'NNx': 2257.0,
     'pNNx': 38.7,
     'PowerVLF': 1828.85,
     'PowerLF': 1852.32,
     'PowerHF': 1299.42,
     'PowerTotal': 4980.6,
     'LF/HF': 1.43,
     'PeakVLF': 0.02,
     'PeakLF': 0.05,
     'PeakHF': 0.27,
     'FractionLF': 58.77,
     'FractionHF': 41.23}
    '''
    import numpy as np
    import pandas as pd
    from scipy.stats import zscore
    from scipy.interpolate import interp1d
    from scipy import signal
    from scipy.integrate import trapz

    metrics = {}

    # Function for reading csv file and extracting timer and ibi
    def readTimerIBI(file, complete_sequence, threshold):
        '''(file_location, complete_sequence="false",threshold=0.1) -> {time_domain dictionary}

        Returns file in the required format.

        file_location is the data file with the first column as time, and the second column as IBI
        complete_sequence takes a true or false argument for whether you require the longest sequence of non missing data
        threshold is used to set the permissible difference between IBI
        '''
        file = pd.read_csv(file)
        file.columns = ['time', 'IBI']

        if complete_sequence == "false":
            # ibi = file['IBI']
            # timer = file['time']
            # timerIBI  = {"ibi": ibi, "timer": timer}
            # return timerIBI
            return file
        else:
            start = [file['time'][0]]
            end = []
            for i in range(1, len(file['time'] + 1)):
                if abs(file['time'][i] - file['time'][i - 1] - file['IBI'][i]) > threshold:
                    end.append(file['time'][i - 1])
                    start.append(file['time'][i])
                else:
                    continue
            end.append(file['time'][len(file) - 1])

            # get max data sequence
            time_diff = list(np.array(end) - np.array(start))
            index = [0]
            max_cut_off = 0
            for i in time_diff:
                if i >= max_cut_off:
                    max_cut_off = i
                    index[0] = time_diff.index(i)
            s = []
            e = []
            d = []
            for i in index:
                s.append(start[i])
                e.append(end[i])
                d.append(end[i] - start[i])
            data = {'start': s, 'end': e, 'difference': d}

            df = file.loc[(file['time'] >= data['start']) & (file['time'] <= data['end'])]

            return (df)

    # Function for calculating Time domain
    # Takes two parameters: timerIBI, an optional x for NN calculations, and correction, if outliers should be corrected for
    def timeDomain(timerIBI, x, correction):
        ''' (readTimerIBI object, x=50, correction="false") -> Time Domain Dictionary

        Returns a time domain dictionary of readTimerIBI object

        x is the time in milliseconds for calculating pNN and NN
        correction is to take care of outliers, should be used carefully
        '''
        t = timerIBI['time']
        ibi2 = timerIBI['IBI'] * 1000  # converts seconds to ms
        ibi = ibi2.rolling(window=10).mean()[10:]

        if correction == "true":
            ibi_set = ibi.copy()
            ibi[np.abs(zscore(ibi_set)) > 2] = np.median(ibi_set)

        def pNNX(ibi, x):
            differences = abs(np.diff(ibi))
            n = np.sum(differences > x)
            p = (n / len(differences)) * 100
            return (p, n)

        def RMSSD(ibi):
            differences = abs(np.diff(ibi))
            rmssd = np.sqrt(np.sum(np.square(differences)) / len(differences))
            return rmssd

        maxHrv = round(max(ibi) * 10) / 10
        minHrv = round(min(ibi) * 10) / 10
        meanHrv = round(np.mean(ibi) * 10) / 10
        medianHrv = round(np.median(ibi) * 10) / 10
        sdnn = round(np.std(ibi) * 10) / 10
        p, n = pNNX(ibi2, x)
        nnx = round(n * 10) / 10
        pnnx = round(p * 10) / 10
        rmssd = round(RMSSD(ibi2) * 10) / 10
        hr = 60 / (ibi / 1000)
        meanHR = round(np.mean(hr) * 10) / 10
        maxHR = round(np.max(hr) * 10) / 10
        minHR = round(np.min(hr) * 10) / 10
        time_domain = {"MeanRR": meanHrv, "MeanHR": meanHR,
                       "MinHR": minHR, "MaxHR": maxHR,
                       "SDNN": sdnn, "RMSSD": rmssd, "NNx": nnx,
                       "pNNx": pnnx}

        return time_domain

    # Function for calculating Frequency domain
    # Takes two parameters: timerIBI, an optional fs for frequency interpolation
    def frequencyDomain(timerIBI, fs):

        ibi = timerIBI['IBI'] * 1000
        steps = 1 / fs

        # create interpolation function based on the rr-samples.
        x = np.cumsum(ibi) / 1000.0
        f = interp1d(x, ibi, kind='cubic')

        # now we can sample from interpolation function
        xx = np.arange(1, np.max(x), steps)
        ibi_interpolated = f(xx)

        # second part
        fxx, pxx = signal.welch(x=ibi_interpolated, fs=fs)

        '''
        Segement found frequencies in the bands 
         - Very Low Frequency (VLF): 0-0.04Hz 
         - Low Frequency (LF): 0.04-0.15Hz 
         - High Frequency (HF): 0.15-0.4Hz
        '''
        cond_vlf = (fxx >= 0) & (fxx < 0.04)
        cond_lf = (fxx >= 0.04) & (fxx < 0.15)
        cond_hf = (fxx >= 0.15) & (fxx < 0.4)

        # calculate power in each band by integrating the spectral density
        vlf = trapz(pxx[cond_vlf], fxx[cond_vlf])
        lf = trapz(pxx[cond_lf], fxx[cond_lf])
        hf = trapz(pxx[cond_hf], fxx[cond_hf])

        # sum these up to get total power
        total_power = vlf + lf + hf

        # find which frequency has the most power in each band
        peak_vlf = fxx[cond_vlf][np.argmax(pxx[cond_vlf])]
        peak_lf = fxx[cond_lf][np.argmax(pxx[cond_lf])]
        peak_hf = fxx[cond_hf][np.argmax(pxx[cond_hf])]

        # fraction of lf and hf
        lf_nu = 100 * lf / (lf + hf)
        hf_nu = 100 * hf / (lf + hf)

        results = {}
        results['PowerVLF'] = round(vlf, 2)
        results['PowerLF'] = round(lf, 2)
        results['PowerHF'] = round(hf, 2)
        results['PowerTotal'] = round(total_power, 2)
        results['LF/HF'] = round(lf / hf, 2)
        results['PeakVLF'] = round(peak_vlf, 2)
        results['PeakLF'] = round(peak_lf, 2)
        results['PeakHF'] = round(peak_hf, 2)
        results['FractionLF'] = round(lf_nu, 2)
        results['FractionHF'] = round(hf_nu, 2)

        return results

    data = readTimerIBI(file, complete_sequence, threshold)
    td = timeDomain(data, x, correction)
    fd = frequencyDomain(data, fs)

    for k, v in td.items():
        metrics[k] = v
    for k, v in fd.items():
        metrics[k] = v

    return metrics