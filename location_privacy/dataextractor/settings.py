'''
Created on Feb 12, 2014

@author: Himanshu Barthwal
'''

jobsettings = {
               #  Both the start and end times are in UNIX epoch time.
               #  These are epoch times with respect to GMT , although
               #  the tweet timestamps are in local time zone but since we
               #  are no interested in the daily patterns so we can avoid translating
               #  the local time to GMT, and thus we will use the GMT epoch times
               #  for creating buckets.
               'ExtractTimeSeries':{'start_timestamp' : 1357083600,
                                    'end_timestamp' : 1357084800,
                                    #Bucket width is in seconds
                                    'bucket_width': 60},
               'ExtractPartitionedUsersByCoordinateSharingBehavior':{}
               }
