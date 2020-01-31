# Missing Data Analysis

**Objectives:**
* Missing_Data_Plot.R script : visually indicates the % missing data per day and per hour of day for each subject present in a dataframe

**Input:**
* Missing_Data_Plot.R script : plt_missing_data() function takes 4 inputs 
  * df = a dataframe that has at least 3 columns:
    * `subject_id` (character)
    * `tod` (numeric), this is the epoch time column
    * `measure` (numeric), this is the signal magnitude column
  * hertz of data collection (for example,if there is one measurement made per second, input `1`) 
  * lubridate standard `timezone` (for example,`America/New_York`) 
  * number of days worth of data in dataframe as numeric

**Output:**
* Missing_Data_Plot.R script: plot that gives 1 subplot per unique `subject_id`, x axis is number of days present in the time range of the given dataframe, y axis is 0-23 (hour of the day)


**Organization:**


**Publications:**



#### Code Available Now:
***
Missing_Data_Plot.R

***

**Sources:**
