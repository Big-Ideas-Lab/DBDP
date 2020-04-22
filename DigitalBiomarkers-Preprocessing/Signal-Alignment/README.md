# ibeat-edtw
## About the data source
84 public data sets in the ***data*** folder could be downloaded from http://www.cs.ucr.edu/~eamonn/time_series_data/

## Supoorted Dynamic Time Warping Methods
The comparison of the following four DTW methods based on Singularity Score and Error Rate could be obtained by running programs in ***downsample*** folder
* Dynamic Time Warping
* Derivative Dynamic Time Warping
* shapeDTW
* EventDTW

## Signal Alignment Visualization tool
![avatar](https://github.com/Big-Ideas-Lab/DBDP/blob/master/DigitalBiomarkers-Preprocessing/Signal-Alignment/figure/Alignment.jpg)

The alignment visualization could be realized by running programs in ***debug*** folder.

Edit dbd_cf.py to set the name of data set and the number of signals
```
debug_file = 'data/Beef_TRAIN'
debug_line = 1
```

***
Please note that this project works in Pycharm 2019.2.2
