# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 13:29:40 2019

@author: 2223
"""

import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.strtree import STRtree
from osgeo import ogr
from Match.matchcase import Case

###load data###
red = gpd.read_file('Data\JVD_20180820.shp', encoding = 'utf-8')
red.crs = {'init':'epsg:32748'}  #initialize projection

yel = gpd.read_file('Data\V6D.shp', encoding = 'utf-8')
yel.crs = {'init':'epsg:32748'}

"""
###plot###
base = red[red['PID'] == 15].plot()
yel[yel['PID'] == 4515].representative_point().plot(ax = base, color = 'red')
yel[yel['PID'] == 4485].representative_point().plot(ax = base, color = 'b')
yel[yel['PID'] == 4515].centroid.plot(ax = base, color = 'm')
"""

Case.tree_query(yel, red)
#yel = Case.tree_query(red, yel)

