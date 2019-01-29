# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:50:11 2018

@author: 2223
EPSG:32748 UTM48S
EPSG:4326  WGS84
EPSG:3826  TWD97
"""
import geopandas as gpd
from shapely.geometry import Point
from shapely.geometry import Polygon
from shapely.strtree import STRtree
from osgeo import ogr

###load data###
red = gpd.read_file('E:\Python\MatchCase Data\JVD_20180820.shp', encoding = 'utf-8')
red.crs = {'init':'epsg:32748'}  #initialize projection

yel = gpd.read_file('E:\Python\MatchCase Data\V6D.shp', encoding = 'utf-8')
yel.crs = {'init':'epsg:32748'}

"""
###plot###
ID = 3308
base = yel[yel['PID'] == ID].plot()
yel[yel['PID'] == ID].representative_point().plot(ax = base, color = 'red')
yel[yel['PID'] == ID].centroid.plot(ax = base, color = 'm')
"""

###Analyze Case for GroundTruth###
yel_centroid_tree = STRtree(yel.geometry.centroid)
red_case = []
for index_red, row_red in red.iterrows():
    if yel_centroid_tree.query(Polygon(row_red['geometry'])) == []:
        red_case.append([])
    else:
        point_input = []
        point = yel_centroid_tree.query(Polygon(row_red['geometry']))
        for i in range(len(point)):
            if Polygon(row_red['geometry']).intersects(point[i]) == True:
                point_input.append(point[i])
        red_case.append(point_input)

###
"""
red['Case'] = None
for index, points in enumerate(red_case):
    tempID = []
    for point in points:
        tempRow = yel[yel['geometry'].centroid == point]
        tempID.append(tempRow['PID'].values)
    if tempID:
        red.loc[index, 'Case'] = tempID
    
 """   
###Analyze Case for proposed###
red_centroid_tree = STRtree(red.geometry.centroid)
yel_case = []
for index_yel, row_yel in yel.iterrows():
    if red_centroid_tree.query(Polygon(row_yel['geometry'])) == []:
        yel_case.append([])

    else:
        point_input = []
        point = red_centroid_tree.query(Polygon(row_yel['geometry']))
        for i in range(len(point)):
            if Polygon(row_yel['geometry']).intersects(point[i]) == True:
                point_input.append(point[i])
        yel_case.append(point_input)

yel['Case'] = None #Initialized the attribute column



#for index_v6d, row_v6d in v6d.iterrows():
#    centroid_v6d.append(Point(row_v6d.geometry.centroid.x, row_v6d.geometry.centroid.y))
#    centroid_v6d.append(jvd_polygon_tree.query(Point(row_v6d.geometry.centroid.x, row_v6d.geometry.centroid.y)))