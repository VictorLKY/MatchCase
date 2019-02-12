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

red_case = Case.tree_query(yel, red)
yel_case = Case.tree_query(red, yel)

yel_case['case_status'] = None

for index, row in yel_case.iterrows():
    if row['Case']:
        pids = row['Case']
        if len(pids) == 1:
            if red_case.loc[pids[0], 'Case']:
                if len(red_case.loc[pids[0], 'Case']) == 1:
                    yel_case.loc[index, 'case_status'] = 'Case2'
                else:
                    yel_case.loc[index, 'case_status'] = 'Case4'
            else:
                yel_case.loc[index, 'case_status'] = 'Case2a'
        elif len(pids) > 1:
            if red_case.loc[pids[0], 'Case']:
                if len(red_case.loc[pids[0], 'Case']) == 1:
                    yel_case.loc[index, 'case_status'] = 'Case3'
                else:
                    yel_case.loc[index, 'case_status'] = 'CaseElse'
            else:
                yel_case.loc[index, 'case_status'] = 'Case3'
    