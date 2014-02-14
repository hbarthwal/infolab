'''
Created on Jan 14, 2014

@author: Himanshu Barthwal
'''
from analysis.plots.coordinate_sharing import PlotUserCoordinatesSharingDistribution
from analysis.plots.home_location_sharing import PlotUserHomeLocationSharingDistribution
from analysis.plots.place_type import PlotPlacesTypeDistribution
from analysis.plots.tweet_count_distribution import  PlotUserTweetCountDistribution
from analysis.plots.sharing_device_distribution import PlotSharingDeviceDistribution
from analysis.plots.geotweet_count_distribution import PlotUserGeoTweetCountDistribution
from analysis.plots.selective_coordinate_hiding import PlotUserSelectiveCoordinatesHidingDistribution
from analysis.plots.tweet_distribution import PlotTweetDistribution
from analysis.statistics.coordinate_sharing import MRUserCoordinatesSharingDistribution
from analysis.statistics.tweet_distribution import MRTweetDistribution
from analysis.statistics.tweet_count_distribution import MRUserTweetCountDistribution
from analysis.statistics.place_type import MRPlacesTypeDistribution
from analysis.statistics.sharing_device_distribution import MRSharingDeviceDistribution
from analysis.statistics.selective_coordinate_hiding import MRUserSelectiveCoordinatesHidingDistribution
from analysis.statistics.geotweet_count_distribution import MRUserGeoTweetCountDistribution
from analysis.statistics.home_location_sharing import MRUserHomeLocationSharingDistribution
from dataextractor.partition_users_by_coordinate_sharing_behavior import MRExtractPartitionedUsersByCoordinateSharingBehavior
from dataextractor.time_series import MRExtractTimeSeries

#  File locations
raw_data_directory = '/home/himanshu/data/raw_data'
stats_data_directory = '/home/himanshu/data/stats/'
plots_directory = '/home/himanshu/data/plots'
plot_pdf_file = 'plots.pdf'

#  Modify this to specify which statistics needs to be generated
data_extractors = [
                            MRExtractPartitionedUsersByCoordinateSharingBehavior,
                            MRExtractTimeSeries
                            ]

#  Modify this to specify which statistics needs to be generated
stats_generators = [
                            MRUserCoordinatesSharingDistribution,
                            MRUserSelectiveCoordinatesHidingDistribution,
                            MRTweetDistribution,
                            MRUserGeoTweetCountDistribution,
                            MRUserTweetCountDistribution,
                            MRPlacesTypeDistribution,
                            MRSharingDeviceDistribution,
                            MRUserHomeLocationSharingDistribution
                            ]

#  Modify this to specify which plots needs to be generated
plotters = [PlotUserCoordinatesSharingDistribution, PlotPlacesTypeDistribution,
                PlotSharingDeviceDistribution, PlotUserHomeLocationSharingDistribution,
                PlotUserTweetCountDistribution, PlotUserSelectiveCoordinatesHidingDistribution,
                PlotTweetDistribution, PlotUserGeoTweetCountDistribution
                ]

#  Settings for the different statistic tasks. These are used by both the
#  stats generator and the plots generator.
jobsettings = {
               'UserCoordinatesSharingDistribution' : {'datafile' :'user_coordinates_sharing',
                                                       'plot_image_file' :'user_coordinates_sharing'},

                'UserSelectiveCoordinatesHidingDistribution' : {'datafile' :'user_selective_coordinates_hiding',
                                                       'plot_image_file' :'user_selective_coordinates_hiding'},

               'UserHomeLocationSharingDistribution' :{'datafile' : 'user_home_location_sharing',
                                                        'plot_image_file' :'user_home_location_sharing.png'},

               'PlacesTypeDistribution':{'datafile' :'place_type_distribution',
                                         'plot_image_file' :'place_type_distribution.png'},

               'SharingDeviceDistribution':{'datafile' : 'sharing_device_distribution',
                                            'plot_image_file' :'sharing_device_distribution.png'},

               'UserTweetCountDistribution':{'datafile' :'user_tweets_count',
                                             'plot_image_file' :'user_tweets_count.png'},

               'UserGeoTweetCountDistribution':{'datafile' :'user_geotweets_count',
                                             'plot_image_file' :'user_geotweets_count.png'},

               'TweetDistribution':{'datafile' :'tweets_distribution',
                                             'plot_image_file' :'tweets_distribution.png'},

               'ExtractTimeSeries':{'datafile':'tweets_timeseries', 'output_format':'json'},

               'ExtractPartitionedUsersByCoordinateSharingBehavior':{'datafile': 'user_partition_by_location_sharing_behavior',
                                                                     'output_format':'raw'}
               }

