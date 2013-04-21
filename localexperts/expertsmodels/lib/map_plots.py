'''
Created on Apr 18, 2013

@author: himanshu
'''
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import time


def draw_screen_poly( lats, lons, m, color = 'yellow'):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( xy, facecolor= color, alpha=0.4 )
    plt.gca().add_patch(poly)

def plotRegion(expertiseRegions, models):
    colors = ['red', 'aqua','blue','green','yellow','magenta','purple', 'grey', 'violet', 'white']
    # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
    # are the lat/lon values of the lower left and upper right corners
    # of the map.
    # lat_ts is the latitude of true scale.
    # resolution = 'c' means use crude resolution coastlines.
    m = Basemap(projection='merc',llcrnrlon=-129,llcrnrlat=27,urcrnrlon=-60,urcrnrlat=50,
                lat_ts=20,resolution='c')
    m.drawcoastlines()
    m.fillcontinents(color='coral',lake_color='aqua')
    # draw parallels and meridians.
    m.drawstates()
    lon = -125.3318
    lat = 37.0799
    x,y = m(lon, lat)
    index = 0
    for region in expertiseRegions:
        lats = [ region._leftTop[0], region._rightBottom[0], region._rightBottom[0], region._leftTop[0] ]
        lons = [ region._leftTop[1], region._leftTop[1], region._rightBottom[1], region._rightBottom[1] ]
        draw_screen_poly( lats, lons, m, color = colors[index])
    
    for model in models:
        x = model['center'][0]
        y = model['center'][1]
        m.plot(x, y, 'bo', markersize=10)
    m.drawmapboundary(fill_color='aqua')
    plt.title("Expert Regions")
    plt.savefig('region.png')
    plt.clf()
    
