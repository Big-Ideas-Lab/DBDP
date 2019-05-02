#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def hrv(file, complete_sequence="false", threshold=0.1, x=50, correction="false", fs=4):

    '''(file, complete_sequence="false", threshold=0.1,  x=50, correction="false") -> {HRV Metrics}

    Returns a dictionary of time and frequency domain metricspiazza


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


# In[ ]:


#devtools = rpackages.importr('devtools')

robjects.r('''
#library("devtools", lib.loc="C:/Program Files/R/R-3.5.2/library")
library("parallel", lib.loc="C:/Program Files/R/R-3.5.2/library")
library("fasttime", lib.loc="C:/Program Files/R/R-3.5.2/library")
require(data.table)
require(plyr)
require(psych)
require(zoo)

#assignInNamespace("version_info", c(devtools:::version_info, list("3.5" = list(version_min = "3.3.0", version_max = "99.99.99", path = "bin"))), "devtools")
# #find_rtools()
# #devtools::install_github('r-dbi/RSQLite')
# library(RSQLite)
# 
# filename <- "wearables_clinical_deID.db"
# sqlite.driver <- dbDriver("SQLite")
# db <- dbConnect(sqlite.driver,
#                 dbname = filename)
# 
# ## default to_remove function
# rem <- c("5d1a706641a0b458da136a16b6c65d6b","c7c2d5fe4b4b981165a14f0684b31dae",
#          "8ce925a402a0b3e31883d3c600ede9cd","807a78004456272761454351a6a759ff")
# 
# #############
# 
# #Table Data Loader
# readDB <- function(tableName, columnString='*', where = '1 = 1'){
#   table<- dbGetQuery(db, paste('select ',columnString, 'from ', tableName, ' where ', where))
#   return(as.data.table(table))
# }
# 
# as.data.dataframe(table)

readCSV <- function(fileName){
  table<- read.csv(fileName)
  return (as.data.frame(table))
}

#Is the data in the format IBI? If yes, change flag to TRUE:
is_IBI = FALSE

#Input .csv file here:

Input_df = readCSV('Final_Test_HR_DBDP.csv')
TB = Input_df[c("iPOP_ID", "Timestamp_Local", "Heart_Rate", "Steps")]

if(is_IBI){
  TB = Input_df[c("Wearable_Account_MD5", "Timestamp_Local", "IBI", "Steps")]
}

#If data starts in HR and want IBI, divide by 60 to get average IBI per minute:
if (is_IBI){
  TB = TB %>%
    mutate(IBI = (1/Heart_Rate) * 60)
    colnames(TB)[3] <- "IBI"
}

#Assign column names:
colnames(TB)[1] <- "Wearable_Account_MD5"
colnames(TB)[2] <- "Timestamp_Local"
colnames(TB)[3] <- "Heart_Rate"
colnames(TB)[4] <- "Steps"


#########
# #pulled up here for function construction. To be deleted
# TB = readDB("wearable_data")
# demographics = readDB("demographics")
# lab_results = readDB("lab_results")
# vitals = readDB("vitals")
# TB = TB[1:100000,]
# TB

##########
#Table Cleaner ## optional
# cleanTable<-function(table, remm, colName){
#   table2<<-table[! (eval(colName)) %in% remm]
#   return(table2)
# }
# cleanTable(TB, '03de0e762b942438d6d7d8ba0ca0f929', quote(Wearable_Account_MD5))
######################

######################
#a function that automates parallel computing
parallelize<- function(data, func){
  no_cores <-  detectCores()-1
  cl <- makeCluster(no_cores)
  newData <- parLapply(cl, data, func)
  stopCluster(cl)
  return(newData)
}

######################
#change time format
formatTime<-function(table, format_DIY, colName){
  table$Date <- fastPOSIXct(table[,eval(colName)])
  return (table)
}
TB <- formatTime(TB,"%Y-%m-%d %H:%M:%S", quote(Timestamp_Local))

sapply(TB, class)

########
#columnInfoGetter
getColumnInfo<- function(table, colName){
  return(data.table(describe(table[,eval(colName)])))
  
}

#SQL version of calling Daytime data (between 8am - 8pm):
# queryDayData <- function(table,columns, dateCol){
#   getTable(table, columns, paste('time(',dateCol,') >= \'08:00:00\' AND ', 'time(',dateCol,') < \'20:00:00\''))
# }
# 
# dayDemo <- queryDayData('wearable_data', 'Timestamp_Local','Timestamp_Local')

# getNightData<- function(table, dateCol){
#   return(table[hour(eval(dateCol)) < 8 | hour(eval(dateCol)) >= 20])
# }
# 
# nightDemo <- getNightData(TB,quote(Date))

#Rewrite above daytime function for .csv files:

queryDayData <- function(table){
  library(dplyr)
  table$Timestamp_Local <- fastPOSIXct(table$Timestamp_Local)
  return(table %>% 
           filter( hour(table$Timestamp_Local) >=8 & hour(table$Timestamp_Local) < 20))
    
}

dayDemo = queryDayData(TB)

getNightData <- function(table){
  library(dplyr)
  table$Timestamp_Local <- fastPOSIXct(table$Timestamp_Local)
  return(table %>% 
           filter( hour(table$Timestamp_Local) < 8 | hour(table$Timestamp_Local) >= 20))
  
}

nightDemo = getNightData(TB)

##############

############
# before using the below functions, make sure that the columns you use are of numeric type. You can do so by doing:

dayDemo$Heart_Rate <- as.numeric(dayDemo$Heart_Rate)

nightDemo$Heart_Rate <- as.numeric(nightDemo$Heart_Rate)

if (is_IBI){
  dayDemo$IBI<- as.numeric(dayDemo$IBI)
  
  nightDemo$IBI <- as.numeric(nightDemo$IBI)
}

############
# a function that categorizes a feature to the corresponding quantile
# assumption here is that if there's at most one value that crosses multiple quantiles
# getQuantile<- function(table, column,newColName, rangeStart, rangeEnd, rangeStep){
#   vec <- table[,eval(column)]
#   #print(vec)
#   quantiles<- quantile(vec, na.rm = TRUE, probs = seq(rangeStart, rangeEnd, by = rangeStep))
#   
#   #quantiles <-quantile(vec, na.rm = TRUE, probs = seq(rangeStart, rangeEnd, by = rangeStep))
#   
#   checkPt <- which(table(quantiles) > 1)
#   for (i in (2:len)){
#     if(quantiles[i]== quantiles[checkPt])
#     {
#       quantiles[i] = quantiles[checkPt]+runif(1, quantiles[i-1], quantiles[len]/(len*len))
#     }
#   }
#   #cbind(table, findInterval(vec, quantiles))
#   return (findInterval(vec, quantiles))
#   
# }

rangeStep = 0.2
vec <- TB[,'Heart_Rate']

if (is_IBI){
  vec <- TB[,'IBI']
}

quantiles <- quantile(vec, na.rm = TRUE, probs = seq(0, 1, by = rangeStep))


#csv file version of getQuantile():
getQuantile <- function(table, rangeStep){
  quantiles <- quantile(vec, na.rm = TRUE, probs = seq(0, 1, by = rangeStep))
  vec <- as.matrix(vec)
  #quantiles <- as.double(quantiles)
  return (findInterval(vec, quantiles))
}

rangeStep = 0.2
getQuantile(TB, rangeStep)

TB = as.data.table(TB)
TB$StDecID = getQuantile(TB, rangeStep)

#dummy_wearable = makeNum(dummy_wearable, c('Skin_Temperature_F'))
#getQuantile(dummy_wearable, 'Skin_Temperature_F', 'SkinTempID',.1,1.0,.1)

######################
#create a new list which reflect the sum of the items in a specific window
window <- function(table, column, groupKey, winSize, func){
  vec <- table[,eval(column)]
  keyVec<- table[,eval(groupKey)]
  newVec = ave(vec, keyVec, FUN = function(x) rollapply(x, width =winSize, FUN= func, align ="right", partial = TRUE))
  return (newVec)
}

TB$stepWindow = window(TB, quote(Steps), quote(Wearable_Account_MD5), 10, sum)

######################
#get resting information based on $keyColumn
restInfo<- function(table, column, keyCol, threshold =10)
{
  subTable = table[(eval(keyCol))< threshold & !is.na(eval(keyCol))]
  return(subTable[,eval(column)])
}

######################

#based on the previous function, we now develop a get resting data function, which will append the resting data to the original table
TB$keyWindowValue = window(TB, quote(Steps), quote(Wearable_Account_MD5), 10, sum)
TB$restInfo = restInfo(TB, quote(Heart_Rate), quote(keyWindowValue),threshold=10)

######################
#get a subtable of high activity level according to self-defined standard

highActivityTable<- function(table, StandardColumn, decile){
    subTable <- table[(eval(StandardColumn)) >= decile & !is.na(eval(StandardColumn))]
    return (subTable)
}

HR_highActivityTable = highActivityTable(TB, quote(StDecID),5)

######################
#get a subtable of high activity level according to self-defined standard
#remember to numerize required columns
lowActivityTable<- function(table, StandardColumn, decile){
  subTable <- table[(eval(StandardColumn)) <= decile & !is.na(eval(StandardColumn))]
  return (subTable)
}

HR_lowActivityTable = lowActivityTable(TB, quote(StDecID),3)

#If IBI variable, then change table labels due to fact that IBI has inverted relationship
#with activity (i.e., is inverse of HR, which has direct relationship with activity level):

if (is_IBI){
  IBI_highActivityTable = HR_lowActivityTable
  IBI_lowActivityTable = HR_highActivityTable
}

#Get final resting HR data (night and low activity):

all_resting_HR = getNightData(lowActivityTable(TB,quote(StDecID),3))

#Generate final summarized per ID resting HR:

final_resting_HR = tapply(all_resting_HR$Heart_Rate, all_resting_HR$Wearable_Account_MD5, mean, na.rm = TRUE) 

#Create final dataframe:
final_resting_HR = as.data.frame(final_resting_HR)
''')

