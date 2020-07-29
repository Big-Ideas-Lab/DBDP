[![Data+](https://user-images.githubusercontent.com/43549914/73490405-77035680-437a-11ea-94c8-bbc555f443f0.png)](https://bigdata.duke.edu/data)

# How to Use this Repository
## Kush Gulati, Annie Hirsch, Noah Lanier, Nathan Warren
***

## 0. Prerequisites
***
### 0.1. Software
 * Python 3
 * Github
 * Jupyter Notebook Interface (optional)
 * Tableau (optional)
### 0.2. Dependencies
* datetime
* ffmpeg
* keras
* matplotlib
* more_itertools
* numpy
* pandas
* plotly
* random
* scipy
* seaborn
* sklearn
* tensorflow
* torch
* window_slider
 
## 1. The Repo 
***
### 1.1. Instructions for getting started with Git 
* Set up Git on your system (Mac: https://www.macworld.co.uk/how-to/mac-software/how-use-git-github-on-your-mac-3639136/; Windows download Git Bash: https://gitforwindows.org/)
* In Bash (Windows) or Command Line (Mac), cd to directory you want to clone this repo into
* Fork or clone GitHub see here: https://www.toolsqa.com/git/difference-between-git-clone-and-git-fork/

### 1.2. Clone the Repository
Cd to a preferred location on your local machine & clone this repository with the following entry to your terminal:

```
git clone https://github.com/Big-Ideas-Lab/DBDP/tree/master/DigitalBiomarkers-HumanActivityRecognition.git
```
&nbsp;
## 2. The Source (00_source)
### Methods
1. Removing columns that have data that does not originate from the Empatica E4 sensors
2. Compiling all individual .csv files of subjects by sensor type
3. Arranging data by Subject_ID
***
You do not need to run anything in this section, but feel free to check out the functions we used to do some cleaning of the source data in this section before we move to analysis code. This folder also contains the source data, with 280 .csv files __(56 participants X 5 sensors)__ 
### 2.1. Outcomes File Cleaning (00_output_cleaner.ipynb)
This notebook will remove columns that have data that does not originate from Empatica E4 sensors and outputs start & end times for each subject's respective activity periods. 

### 2.2. Sensor Concatenation (01_sensor_concat.ipynb)
This notebook takes properly formatted .csv files from the E4FileFormatter (DBDP preprocessing not shown) and compiles all .csv files of subjects by sensor type. 
&nbsp;
## 3. The Code (10_code)
***
Let's walk through the code pipeline step-by-step.
### 3.1. Data Resampling and Cleaning (10_data_preprocessing.ipynb)
### Methods
1. Resample the combined sensor data at 4 Hz 
2. Clean outcomes dataset to select periods of time where activity occured in the combined sensor dataset. 
3. Add time segments to a new dataframe and output for each participant, and all participants

***
This notebook is composed of data resampling from the combined sensor data and cleaning the outcomes dataset, taking in the combined sensor and outcomes time files  and returning Datasets for Individuals and Outcomes Dataset w/ End-Times. 
### 3.2. Exploratory Data Analysis (20_exploratory_data_analysis.ipynb)
### Methods
1. Explore Class Distribution and Comparing Classes by Sensor Distribution
2. Analyze Outliers by Time and by Acticity
3. Cluster on Sensor Summary Statistics
4. Plot 3D Anmiated Sensor Plots
***
This notebook contains the exploratory data analysis for the Human Activity Recognition team's data. It uses the aggregated w/ activity csv. Check out our analysis of the data, including target class distribution, outlier detection, sensor distribution, activity comparison, 3D animation, etc.

### 3.3. End Preprocessing (30_end_pre_processing folder)
### Methods
1. Remove rows of data where the Apple Watch sensors were used instead of the Empatica E4 sensor, to allow for a consistent sampling rate among the data without the need for extra interpolation. 
2. Remove Subject ID 19-028 from data because activity key stated that their rounds were flipped, but when flipped this resulted in an odd amount of rows of data
3. Create a rolling analysis of our time series data, which is used to capture our sensor instability over time 
4. Compute parameter estimates over a rolling window of a fixed size through the sample
5. Add 'super rows' to your code which will also include all sensor readings and activity, Subject ID, and round labels for the next time point, attempt to bypass data augmentation. 
6. Engineer features of our rolled data that will be used in the Random Forest models & Deep Learning Models. 
***
#### &nbsp;&nbsp;&nbsp;3.3.1. Outlier Removal (31_outlier_removal.ipynb)
This notebook removes rows of data where the Apple Watch sensors were used instead of the Empatica E4 sensor, to allow for a consistent sampling rate among the data without the need for extra interpolation. Using the aggregated file, it outputs:
1. .csv without Apple Watch Data: label rounds 1 & 2 separated 
2. .csv without Apple Watch Data: label rounds 1 & 2 combined
#### &nbsp;&nbsp;&nbsp;3.3.2. Feature Engineering (31_roll_timepoints.ipynb, 32_super.ipynb, 33_feature_engineering.ipynb)
1. __31_roll_timepoints.ipynb__ contains our procedure for creating a rolling analysis of our time series data, which is used to capture our sensor instability over time. A common technique to assess the constancy of a model’s parameters is to compute parameter estimates over a rolling window of a fixed size through the sample. As the sensor parameters due to some variability in time sampling, the rolling estimates should capture this instability. 
2. __32_super.ipynb__ provides code to add 'super rows' to your code. Each row will also include all sensor readings and activity, Subject ID, and round labels for the next time point. The goal is to include other time points as features for each row, without relying on other data augmentation methods that reduce the total amount of data, such as windowing, rolling, or aggregating. 
3. __33_feature_engineering.ipynb__ outlines the process for engineering features of our data that will be used in the Random Forest models. The five types of features we created are window mean, standard deviation, skew, minimum, and maximum. 

### 3.4. Usable Data for Models (40_usable_data_for_models folder)
***
We have been working entirely with the Duke_Data so far. It comes from this study: https://www.nature.com/articles/s41746-020-0226-6. We also used the PAMAP2 Dataset to further test our models. 
#### &nbsp;&nbsp;&nbsp;3.4.1. Our Data (41_Duke_Data folder)
#### &nbsp;&nbsp;&nbsp;3.4.2. PAMAP2 Data (42_PAMAP2 folder)

### 3.5. Deep Learning (50_deep_learning folder)
### Methods
1. ANN on raw sensor values, LOOCV validation
2. ANN with engineered window features (e.g., summary stats on 10s windows no overlap), LOOCV validation
3. ANN on engineered window features with multinomial voting classification mechanism, LOOCV validation
***

![Deep Learning Pipeline](https://github.com/Big-Ideas-Lab/Data-2020/blob/master/30_docs/DataPipeline.png)
#### &nbsp;&nbsp;&nbsp;3.5.1. Model Templates (51_model_templates folder)
Provides just the data preparation needed to input data into any neural network, split by data source

#### &nbsp;&nbsp;&nbsp;3.5.2. Pytorch Models (52_pytorch_models folder)
Contains ANN models for both the STEP and PAMAP2 data.

#### &nbsp;&nbsp;&nbsp;3.5.3. Tensorflow Models (53_tensorflow_models folder)
Contains a multitude of deep learning models that have a specific notebook for each data source. Also has model files for each model run, including models with only mechanical, phyiological, and all sensors. These models use the STEP dataset which is also refered to as the Duke dataset. 
#### 1. ANN (10_ANN.ipynb) 
This artificial neural network has 2 hidden fully connected layers with a dropout layer between them to prevent overfitting. The finaly fully connected layer classifies each timepoint fed into the model into 4 classes. This model uses leave-one-person-out validation. With this model we are able to compare the difference between including only mechanical sensors, only physiological sensors, or both. 
#### 2. ANN with feature engineering (20_ANN_WFE.ipynb) 
This model uses engineered features from 20 second windows, with 10 second overlap. The engineered features are min, max, mean, standard deviation of our sensor values during these windows of time. The model consists of 6 hidden fully connected layers, a dropout layer and uses leave-one-person-out validation. With this model we are able to compare the difference between including only mechanical sensors, only physiological sensors, or both. 

### 3.6. Random Forests (60_random_forests folder)
### Methods
1. Run Functions for Random Forest feature importances on feature engineered data
2. Develop Random Forest on Individual Data
3. Develop Random Forest on Feature Engineered Data
4. Compare results w/ ACC-Only, PHYS-Only, ACC+PHYS
***
#### &nbsp;&nbsp;&nbsp;3.6.1. RF Functions (61_rf_functions.ipynb)
This notebook contains functions for the Random Forest w/ LOOCV. It also contains code for evaluating feature importances from the random forest. These functions are modular and can be adapted to your own classification needs. The model is built on the rolling average data with engineered features and helped us calculate feature importances, compare ACC+PHYS vs ACC-Only models, and incorporate LOOCV. 
#### &nbsp;&nbsp;&nbsp;3.6.2. RF w/ Individual Data (62_rf_individual.ipynb)
This notebook is composed of a random forest classification model to evaluate a general accuracy level of traditional ML methods in classifying our HAR data based on activity. The model is built on the individual raw signal data.
#### &nbsp;&nbsp;&nbsp;3.6.3. RF w/ Feature-Engineered Sliding Window Data (63_rf_feature_engineering.ipynb)
This notebook is composed of a random forest classification model to evaluate a general accuracy level of traditional ML methods in classifying our HAR data based on activity. The model is built on sliding window average data with engineered features.

&nbsp;

&nbsp;
## 4. The Results (20_results)
***
These are the overall best results for our models using balanced classes. Higher accuracy and F1 score was actually achieved for ANN_WFE when using our imbalanced dataset. This points to the idea that our models metrics could possibly be improved with more data as currently only 505 rows of data are fed into ANN_WFE for each class during training.  

| Model Name    | Data Input Type            | Data Source | Accuracy | F1 Score |
|---------------|----------------------------|-------------|----------|----------|
| ANN_WFE          | Feature Engineered Windows | STEP        | 0.81     | 0.80     |
| Random Forest | Feature Engineered Windows | STEP        | 0.84     | 0.81     |
| ANN           | Individual Timepoints      | STEP        | 0.64     | 0.61     |
| ANN           | Individual Timepoints      | PAMAP2      | 0.96     | 0.96     |  

**Accuracy Comparisons**

![**Model and Sensor Comparisons**](https://github.com/Big-Ideas-Lab/Data-2020/blob/master/20_results/40_other_figures/overall_accuracy_v2.png)

The figure above displays the overall F1 scores for our Random Forest, ANN, and ANN with feature engineered windows. The highest F1 score achieved is the ANN_WFE model only using accelerometry data. 


**Confusion Matrix Results: ANN_WFE**
![**Confusion Matrix Comparison for ANN_WFE**](https://github.com/Big-Ideas-Lab/Data-2020/blob/master/20_results/20_confusion_matrix/20_ANN_WFE/ANN_WFE_CF_results.png)

**Accuracy Results: ANN_WFE**
|                     | Accuracy | Accuracy SD | F1   | F1 SD |
|---------------------|----------|-------------|------|-------|
| All Sensors         | 0.81    | 0.12       | 0.79 | 0.14  |
| Accelerometry Only  | 0.84    | 0.11       | 0.83 | 0.12  |
| Physiological Only  | 0.60    | 0.16       | 0.57 | 0.18  |

Based on our ANN_WFE model, it appears that the addition of physiological data does not improve the model. The results shown in the table above are based on our leave-one-person-out validation. Interestingly, It appears that only physiological sensors are unable to classify the class, "activity" well. Classification for the class, "Type", is strong regardless of the kind of sensors used. 

**Confusion Matrix Results: Random Forest**

![**Confusion Matrix Comparison for Random Forest**](https://github.com/Big-Ideas-Lab/Data-2020/blob/master/20_results/20_confusion_matrix/30_RF/RF_CFs.png)

&nbsp;


