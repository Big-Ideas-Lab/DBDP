##### RHR_estimation_model.R
# Example usage of the helper functions defined in RHR_estimation.R and plotting.R
# The original Strong-D data has not been included for participant confidentiality purposes.
##### Input:
# HR data.table with columns: "Id" (id of participant/individual), "Time" (POSIXct) and "Values" (integer heart rate value)
# Steps data.table with columns:  "Id" (id of participant/individual), "ActivityMin" (POSIXct) and "Steps" (integer count of num. steps)
# Note that the steps measurement frequency (ActivityMin; in minutes) is lower than the HR steps measurement frequency (Time; in seconds)
##### Output: 
# Data structures and plots containing the estimated RHR and associated parameters and data.

source("RHR_estimation.R")
source("plotting.R")

# Load Data ----
# e.g.:
# load("cleaning/RData_clean/dt_steps.RData")
# load("cleaning/RData_clean/dt_hr_filtered.RData")

# head(dt_hr)
# Id                Time Value
# 1: 0005 2017-08-03 07:00:04   105
# 2: 0005 2017-08-03 07:00:09   105
# 3: 0005 2017-08-03 07:00:14   105
# 4: 0005 2017-08-03 07:00:19   105
# 5: 0005 2017-08-03 07:00:34   105
# 6: 0005 2017-08-03 07:00:49   105

# head(dt_steps_perMin)
# Id         ActivityMin Steps
# 1: 0004 2017-08-01 00:00:00     0
# 2: 0004 2017-08-01 00:01:00     0
# 3: 0004 2017-08-01 00:02:00     0
# 4: 0004 2017-08-01 00:03:00     0
# 5: 0004 2017-08-01 00:04:00     0
# 6: 0004 2017-08-01 00:05:00     0

# Interpolate per second HR measurement for each per minute step measurement ----
# note that interpolating in the other direction (find per minute step measurement for each per second HR measurement)
# would create duplicate step measurements, making it seem like the participant took more steps

# setup for join on id and then within each unique id value, join on time
dt_hr[, join_time := Time]
dt_steps_perMin[, join_time := ActivityMin]
setkey(dt_hr, Id, join_time)
setkey(dt_steps_perMin, Id, join_time)

# right outer join (include all measurements from dt_steps_perMin), interpolating the temporally closest HR measurement for each steps measurement
# we're interested in HR changes that RESULT FROM previously taken steps
# thus, we roll backward to interpolate the closest HR measurement that occurs AFTER each steps measurement

# limit interpolation to HR measurement that occur at most 1min (60s) after step measurement
join_steps_hr <- dt_hr[dt_steps_perMin, roll = -60] 
dt_steps_hr <- join_steps_hr[, .(Id, ActivityMin, Value, Steps)]
# remove step measurements that do not have an interpolated HR value
dt_steps_hr <- dt_steps_hr[!is.na(Value)]
id_list <- dt_steps_hr$Id %>% unique()

setkey(dt_steps_hr, Id, ActivityMin)

# Quick search over sampled participants -----
set.seed(0)
id_sample <- sample(id_list, 3)

# step threshold search over hundreds
window_size_list <- c(1, 5, 10, 30, 60)  # minutes
steps_threshold_list <- c(0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000)  # num. steps

plots_metrics_list <- gridsearch_per_id(id_sample, get_rhr_metrics, window_size_list, steps_threshold_list, save = FALSE)
# stdout:
# [1] "Searching for participant with id 0032"
# |===================================================================================================================| 100%
# steps_threshold window_size  RHR_dev notRHR_dev RHR_median notRHR_median
# 1:             100          10 14.31484   14.66551         86           104
# [1] "Searching for participant with id 0119"
# |===================================================================================================================| 100%
# steps_threshold window_size RHR_dev notRHR_dev RHR_median notRHR_median
# 1:               0          60 5.83718   11.37373         88           100
# [1] "Searching for participant with id 0011"
# |===================================================================================================================| 100%
# steps_threshold window_size  RHR_dev notRHR_dev RHR_median notRHR_median
# 1:             100          10 12.63982   15.71807         79           100

plots <- plots_metrics_list$plots

png(filename = sprintf("example_output/%s.png", paste(id_sample, collapse="_")), width = 8, height = 6, units = "in", res = 500)
multiplot(plotlist = plots, layout = matrix(1:(length(id_sample)*2), ncol = 2, byrow=TRUE))
dev.off()

# Fine grain search over all participants -----
window_size_list <- seq(1, 120, 1)  # minutes
steps_threshold_list <- seq(0, 1000, 10) # num. steps

plots_metrics_list <- gridsearch_per_id(id_list, get_rhr_metrics, window_size_list, steps_threshold_list, save = FALSE)