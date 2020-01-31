##### RHR_estimation.R
# This script defines the R helper functions used for estimating resting heart rate from Fitbit data (heart rate and steps).
# These functions include: get_rhr_metrics, gridsearch_per_id

library(data.table)
library(magrittr)
library(RcppRoll)

# Define RHR in terms of num. steps taken within some time window ----
get_rhr_metrics <- function(dt_steps_hr, window_size_list, steps_threshold_list) {
  # initialize table with all possible combinations of the step thresholds and window sizes specified above
  dt_results <- data.table(steps_threshold = rep(steps_threshold_list, each = length(window_size_list)),
                           window_size = window_size_list,  # will be recycled
                           RHR_dev = as.numeric(rep(NA, length(steps_threshold_list)*length(window_size_list))),
                           notRHR_dev = as.numeric(rep(NA, length(steps_threshold_list)*length(window_size_list))),
                           RHR_median = as.numeric(rep(NA, length(steps_threshold_list)*length(window_size_list))),
                           notRHR_median = as.numeric(rep(NA, length(steps_threshold_list)*length(window_size_list)))
                           )
  
  num_participants <- dt_steps_hr$Id %>% unique() %>% length()
  
  # progress bar
  pb <- txtProgressBar(min = 0, max = nrow(dt_results), style = 3)
  i = 1
  for (n in window_size_list) {
    # cleanup
    dt_steps_hr[, rolling_sum_steps := NULL]
    
    dt_steps_hr[, 
                rolling_sum_steps := roll_sum(Steps, n, align = "right", fill = NA),
                by = Id]
    
    # TODO: get rid of multi-id logic
    for (m in steps_threshold_list) {
      # summary HR where rolling_sum_steps <= steps_threshold for each participant
      dt_low_deviationHR_byId <- dt_steps_hr[rolling_sum_steps <= m,
                                           .(low_deviationHR = sd(Value, na.rm = TRUE)),
                                           by = Id]
      
      # summary HR where rolling_sum_steps > steps_threshold for each participant
      dt_high_deviationHR_byId <- dt_steps_hr[rolling_sum_steps > m,
                                            .(high_deviationHR = sd(Value, na.rm = TRUE)),
                                            by = Id]
      
      # only consider participants with who have associated values in BOTH the "low" and "high" tables above
      # id_list <- intersect(dt_low_deviationHR_byId$Id, dt_high_deviationHR_byId$Id)
      # dt_id <- data.table(Id = id_list)
      
      # if (nrow(dt_id) >= ceiling(num_participants/2)) {
      dt_low_deviationHR_byId <- dt_low_deviationHR_byId  #[dt_id, on = "Id"]
      dt_high_deviationHR_byId <- dt_high_deviationHR_byId  #[dt_id, on = "Id"]
      
      if (nrow(dt_low_deviationHR_byId) == 1) {
        dt_results[window_size == n & steps_threshold == m]$RHR_dev <- dt_low_deviationHR_byId$low_deviationHR 
      }
      
      if (nrow(dt_high_deviationHR_byId) == 1) {
        dt_results[window_size == n & steps_threshold == m]$notRHR_dev <- dt_high_deviationHR_byId$high_deviationHR 
      }
      
      dt_low_medianHR <- dt_steps_hr[rolling_sum_steps <= m,
                                     .(low_medianHR = median(Value, na.rm = TRUE)),
                                     by = Id]
      dt_high_medianHR <-  dt_steps_hr[rolling_sum_steps > m,
                                       .(high_medianHR = median(Value, na.rm = TRUE)),
                                       by = Id]
      
      if (nrow(dt_low_medianHR) == 1) {
        dt_results[window_size == n & steps_threshold == m]$RHR_median <- dt_low_medianHR$low_medianHR
      }
      
      if (nrow(dt_high_medianHR) == 1) {
        dt_results[window_size == n & steps_threshold == m]$notRHR_median <- dt_high_medianHR$high_medianHR 
      }
      
      setTxtProgressBar(pb, i)
      i = i + 1
    }
  }
  
  close(pb)
  return(dt_results)
}

# Best window + step threshold combination for each participant ----
gridsearch_per_id <- function(id_list, rhr_metrics_func, window_size_list, steps_threshold_list, soft = FALSE, save = FALSE) {
  rhr_metrics_func_name <- substitute(rhr_metrics_func) %>% as.character()
  
  plots <- list()
  dt_metrics <- data.table(Id = id_list,
                           penalty = as.numeric(rep(NA, length(id_list))),
                           steps_threshold = as.numeric(rep(NA, length(id_list))),
                           window_size = as.numeric(rep(NA, length(id_list))),
                           RHR_median = as.numeric(rep(NA, length(id_list))),
                           notRHR_median = as.numeric(rep(NA, length(id_list))),
                           RHR_mean = as.numeric(rep(NA, length(id_list))),
                           notRHR_mean = as.numeric(rep(NA, length(id_list))),
                           RHR_size = as.numeric(rep(NA, length(id_list))),
                           notRHR_size = as.numeric(rep(NA, length(id_list))),
                           RHR_max = as.numeric(rep(NA, length(id_list))),
                           notRHR_max = as.numeric(rep(NA, length(id_list))),
                           RHR_min = as.numeric(rep(NA, length(id_list))),
                           notRHR_min = as.numeric(rep(NA, length(id_list)))
  )
  for(i in 1:length(id_list)) {
    id <- id_list[i]
    print(sprintf("Searching for participant with id %s", id))
    
    if (soft == TRUE) {
      softmin <- dt_steps_hr[Id == id]$Value %>% quantile(0.05, na.rm = TRUE)
      softmax <- dt_steps_hr[Id == id]$Value %>% quantile(0.95, na.rm = TRUE)
      
      dt_results <- rhr_metrics_func(dt_steps_hr[Id == id & Value < softmax & Value > softmin], window_size_list, steps_threshold_list)  
    } else {
      dt_results <- rhr_metrics_func(dt_steps_hr[Id == id], window_size_list, steps_threshold_list)  
    }
    
    best_index <- dt_results[, 3] %>% unlist() %>% as.numeric() %>% which.min()
    dt_best <- dt_results[best_index]
    print(dt_best)
   
    window_size <- dt_best$window_size
    steps_threshold <- dt_best$steps_threshold
    
    dt_metrics[Id == id]$penalty <- dt_best[, 3]
    dt_metrics[Id == id]$steps_threshold <- steps_threshold
    dt_metrics[Id == id]$window_size <- window_size
    
    dt_steps_hr[, rolling_sum_steps := NULL]
    dt_steps_hr[Id == id, rolling_sum_steps := roll_sum(Steps, window_size, align = "right", fill = NA)]
    
    dt_steps_hr[, isRHR := NULL]
    dt_steps_hr[(Id == id) & (rolling_sum_steps <= steps_threshold),
                isRHR := TRUE]
    dt_steps_hr[(Id == id) & (rolling_sum_steps > steps_threshold),
                isRHR := FALSE]
    
    # median
    dt_metrics[Id == id]$RHR_median <- dt_steps_hr[(Id == id) & isRHR == TRUE & !is.na(Value)]$Value %>% median()
    dt_metrics[Id == id]$notRHR_median <- dt_steps_hr[(Id == id) & isRHR == FALSE & !is.na(Value)]$Value %>% median()
    
    # mean
    dt_metrics[Id == id]$RHR_mean <- dt_steps_hr[(Id == id) & isRHR == TRUE & !is.na(Value)]$Value %>% mean()
    dt_metrics[Id == id]$notRHR_mean <- dt_steps_hr[(Id == id) & isRHR == FALSE & !is.na(Value)]$Value %>% mean()
    
    # size
    dt_metrics[Id == id]$RHR_size <- dt_steps_hr[(Id == id) & isRHR == TRUE & !is.na(Value)]$Value %>% length()
    dt_metrics[Id == id]$notRHR_size <- dt_steps_hr[(Id == id) & isRHR == FALSE & !is.na(Value)]$Value %>% length()
    
    # min
    dt_metrics[Id == id]$RHR_min <- dt_steps_hr[(Id == id) & isRHR == TRUE & !is.na(Value)]$Value %>% min()
    dt_metrics[Id == id]$notRHR_min <- dt_steps_hr[(Id == id) & isRHR == FALSE & !is.na(Value)]$Value %>% min()
    
    # max
    dt_metrics[Id == id]$RHR_max <- dt_steps_hr[(Id == id) & isRHR == TRUE & !is.na(Value)]$Value %>% max()
    dt_metrics[Id == id]$notRHR_max <- dt_steps_hr[(Id == id) & isRHR == FALSE & !is.na(Value)]$Value %>% max()
    
    # plots
    plots[[(i-1)*2 + 1]] <- show_linePerGroup(dt_steps_hr[isRHR == TRUE & Id == id], "ActivityMin", "Value", "Id") +
      scale_color_manual(values = "#66C2A5") +
      ylim(c(20, 220)) +
      theme(plot.title = element_text(hjust = 0.5, size = 9), axis.title = element_text(size = 7)) +
      labs(title = sprintf("%s: estimated RHR, window=%d, steps=%d", id, window_size, steps_threshold),
           x = "Minutes",
           y = "Heart Rate")
    
    if (save == TRUE) {
      sprintf("%s_window=%d_steps=%d_isRHR=TRUE_%s_soft=%s.png", id, window_size, steps_threshold, rhr_metrics_func_name, as.character(soft)) %>%
        ggsave(path = "./temp_plots/", width = 8, height = 6, units = "in")
    }
    
    plots[[(i-1)*2 + 2]] <- show_linePerGroup(dt_steps_hr[isRHR == FALSE & Id == id], "ActivityMin", "Value", "Id") +
      scale_color_manual(values = "#FC8D62") +
      ylim(c(20, 220)) +
      theme(plot.title = element_text(hjust = 0.5, size = 9), axis.title = element_text(size = 7)) +
      labs(title = sprintf("%s: estimated regular HR: window=%d, steps=%d", id, window_size, steps_threshold),
           x = "Minutes",
           y = "Heart Rate")
    
    if (save == TRUE) {
      sprintf("%s_window=%d_steps=%d_isRHR=FALSE_%s_soft=%s.png", id, window_size, steps_threshold, rhr_metrics_func_name, as.character(soft)) %>%
        ggsave(path = "./temp_plots/", width = 8, height = 6, units = "in")
    }
  }
  
  return(list("plots" = plots, "dt_metrics" = dt_metrics))
}