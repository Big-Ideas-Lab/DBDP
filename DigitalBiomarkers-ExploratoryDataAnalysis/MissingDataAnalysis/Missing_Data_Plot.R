## Missing Data Graph Script
## By Emilia Grzesiak, BIG IDEAS Lab 2020

#required packages
library(ggplot2)
library(tidyverse)
library(dplyr)
library(lubridate)
library(tidyr)
library(bigmemory)
library(biganalytics)
library(anytime)


plt_missing_data <- function(df, hertz, timezone, num_days){
  # Finds the amount of missing data per day and hour of any E4 signal data
  # Can be generalized to any time series data if pre-processed in fashion described below
  
  # inputs: 1) dataframe that has at least 3 columns named `subject_id` as string/character object,
  # `tod` as a numeric object (this is the epoch time column), and `measure` as a numeric
  # object (this is the signal magnitude column); 2) hertz of data collection (for example, 
  # if there is one measurement made per second, input `1`); 3) lubridate standard `timezone` 
  # (for example,`America/New_York`); 4) number of days worth of data in dataframe as numeric
  
  # output: plot that gives 1 subplot per unique `subject_id`, x axis is number of days present
  # in the time range of the given dataframe, y axis is 0-23 (hour of the day)
  
  
  #processing data to index days and convert epoch time to datetime object
  df <- setDT(df, keep.rownames=TRUE, key=NULL, check.names=FALSE)
  df$ftime <- anytime(df$tod, timezone)
  df$fday <- day(df$ftime)
  df <- df[,index_day := .GRP, by = .(subject_id, fday)]
  df <- df[, index_day:=index_day-index_day[1]+1L, by="subject_id"]
  
  df_missing_perHour <- df %>% 
    group_by(subject_id, index_day, (format(ftime, format = "%H"))) %>%
    dplyr::summarize(count=n()*100/(3600*hertz))
  colnames(df_missing_perHour)[3] <- "hour"
  df_missing_perHour$hour <- as.integer(df_missing_perHour$hour)
  
  df_missing_perHour = df_missing_perHour %>%
    group_by(subject_id, index_day, hour) %>%
    complete(index_day=1:num_days)
  df_missing_perHour[is.na(df_missing_perHour)] <- 0
  
  
  
  df_missing_data <- ggplot(df_missing_perHour, aes(index_day, hour, fill = count))+
    geom_tile()+
    facet_wrap(~subject_id, nrow=5)+
    scale_fill_gradient(
      guide = guide_colorbar(label = TRUE,
                             draw.ulim = TRUE, 
                             draw.llim = TRUE,
                             ticks = TRUE, 
                             nbin = 10,
                             frame.colour = "black",
                             label.position = "bottom",
                             barwidth = 10,
                             barheight = .8, 
                             direction = 'horizontal')) +
    theme(panel.background = element_rect(fill = "white", colour = "grey50"),
          legend.position = 'bottom', text = element_text(size=10, face = "bold"))+
    scale_x_continuous(breaks = unique(df_missing_perHour$index_day), 
                       labels=  unique(df_missing_perHour$index_day))+
    #scale_y_continuous(breaks = unique(HR_missing_perHour$hour), 
    #                   labels=  unique(HR_missing_perHour$hour))+
    xlab("Day")+
    ylab("Hour of Day")+
    ggtitle("Missing Data per Day per Subject")+
    labs(fill="% Data Present")
  print(df_missing_data)
  
}
