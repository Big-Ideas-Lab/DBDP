# Resting Heart Rate

**Objectives:** Estimate the resting heart rate biomarker using:
1. _Personal_ data (i.e. different estimates for different individuals)
2. _Accessible_ wearable device data, specifically Fitbit data
3. _Transparent and meaningful_ model/logic based on background literature

**Organizations:** This project is part of the **Big Ideas Lab at Duke University**. We collaborated with the **DISCOVeR Lab at Stanford University**, which conducted the Strong-D study. The Strong-D Fitbit data set was used to develop, evaluate and publish this resting heart rate estimation model.

**Publication:**
C. Jiang, L. Faroqi, L. Palaniappan and J. Dunn, "Estimating Personal Resting Heart Rate from Wearable Biosensor Data," _2019 IEEE EMBS International Conference on Biomedical & Health Informatics (BHI)_, Chicago, IL, USA, 2019, pp. 1-4.
doi: 10.1109/BHI.2019.8834554
URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8834554&isnumber=8834448

Please contact the contributors of this repository if you cannot access this publication.

#### Code Available Now:
***
`RHR_estimation.R`: helper functions for estimating resting heart rate from Fitbit data (heart rate and steps)
`plotting.R`: helper functions for plotting 
`example.R`: example usage of the functions in this directory; the associated output plots are included in the `example_output` subdirectory

***

#### Dependencies
R packages:
* `data.table`
* `magrittr`
* `RcppRoll`
* `ggplot2`

**Sources:**
* [Publication: Estimating Personal Resting Heart Rate from Wearable Biosensor Data](http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8834554&isnumber=8834448)
* [Big Ideas Lab at Duke University](http://dunn.pratt.duke.edu)
* [DISCOVeR Lab at Stanford University](http://med.stanford.edu/discover.html)