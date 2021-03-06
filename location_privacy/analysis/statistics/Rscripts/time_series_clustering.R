# This file contains the script to read time series generated by the time_series.py
# and then cluster them according to their seasonal trends.
# 
# Author: Himanshu Barthwal
###############################################################################
require(rjson)

# Function used to trimming the quotes from a given string
Trim <- function (x) gsub("^\\s+|\\s+$", "", x)

# Function used for reading timeseries data from the file.
ReadTimeSeriesData <- function(timeSeriesData) {
	timeseriesJsonData <- gsub('\"\"','',timeSeriesData)
	timeseriesJsonData <- Trim(timeseriesJsonData)
	timeseries <- fromJSON(timeseriesJsonData)
	timeseries <- as.numeric(unlist(strsplit(timeseries[[1]], ",") ))
	return(timeseries)
}

# This function loads the timeseries data in to a dataframe
LoadTimeSeriesData <- function(filename) {
fileConnection  <- file(filename, open = "r")
dataLine <- readLines(fileConnection, n = 1, warn = FALSE)
timeseries = ReadTimeSeriesData(dataLine)
timeseriesLength = length(timeseries)
dataFrame <- as.data.frame(matrix(nrow = 0, ncol = timeseriesLength))
while (length(dataLine <- readLines(fileConnection, n = 1, warn = FALSE)) > 0) {
	dataFrame = rbind(dataFrame, timeseries)
	timeseries = ReadTimeSeriesData(dataLine)	
} 
close(fileConnection)
return(dataFrame)
}

dataFrame <- LoadTimeSeriesData('/home/himanshu/data/raw_data/users_checkins_timeseries')
print(dataFrame)
library(dtw)
distMatrix <- dist(dataFrame, method='DTW')
print(distMatrix)
hc <- hclust(distMatrix, method='average')
plot(hc, main='')
