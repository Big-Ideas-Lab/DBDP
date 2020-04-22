# ibeat-edtw
## About the data source
84 public data sets in the ***data*** folder could be downloaded from http://www.cs.ucr.edu/~eamonn/time_series_data/

## Supoorted Dynamic Time Warping Methods
The comparison of the following four DTW methods based on Singularity Score and Error Rate could be obtained by running programs in ***downsample*** folder
* Dynamic Time Warping
* Derivative Dynamic Time Warping
* shapeDTW
* EventDTW

Table 1 in supplementary materials and Table 1 in article are available by running

```
downsample_with_dDTW.py
downsample_with_dtw.py
downsample_with_eventdtw.py
downsample_with_shapedtw.py
```

## Signal Alignment Visualization tool

The alignment visualization could be realized by running programs in ***debug*** folder. Figure 2(a) middle and Figure 4 are available by running 

```
downsample_ddtw_dbg.py
downsample_dtw_dbg.py
downsample_eventdtw_dbg.py
downsample_shapedtw_dbg.py
```

Edit dbd_cf.py to set the name of data set and the number of signals
```
debug_file = 'data/Beef_TRAIN'
debug_line = 1
```

***
Please note that this project works in Pycharm 2019.2.2
