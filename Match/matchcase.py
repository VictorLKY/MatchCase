# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 09:57:31 2019

@author: 2223
"""

from shapely.geometry import Polygon
from shapely.strtree import STRtree

class Case:
    def __init__(self):
        pass
    
    def tree_query(tree, queried): # tree: point, queried: polygon
        case_list = []
        centroid_tree = STRtree(tree.geometry.representative_point())
        for index, row in queried.iterrows():
            if centroid_tree.query(Polygon(row['geometry'])) == []:
                case_list.append([])
            else:
                point_input = []
                point = centroid_tree.query(Polygon(row['geometry']))
                for i in range(len(point)):
                    if Polygon(row['geometry']).intersects(point[i]) == True:
                        point_input.append(point[i])
                case_list.append(point_input)
    

        tree['X'] = tree['geometry'].representative_point().x
        tree['Y'] = tree['geometry'].representative_point().y
        queried['Case'] = None    # Initialized the attribute column
        for index, points in enumerate(case_list):
            tempID = []
            for point in points:
                tempRow = tree.query('X == @point.x and Y == @point.y')
                tempID.append(tempRow['PID'].values)
            if tempID:
                queried.loc[index, 'Case'] = tempID
        return queried