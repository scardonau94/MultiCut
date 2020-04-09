# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 17:27:29 2020

@author: Vias
"""

import pandas as pd
import geopandas as gpd
import shapely.geometry as geom
import numpy as np
from shapely.geometry import LineString
from shapely.geometry import Point
from shapely.geometry import MultiLineString

# Firts we define the function cut from shapely docs
# cut uses a line (LineString) and a define distance to cut the line in two parts
def cut(line, distance):
    # Cuts a line in two at a distance from its starting point
    if distance <= 0.0 or distance >= line.length:
        return [LineString(line)]
    coords = list(line.coords)
    for i, p in enumerate(coords):
        pd = line.project(Point(p))
        if pd == distance:
            return [
                LineString(coords[:i+1]),
                LineString(coords[i:])]
        if pd > distance:
            cp = line.interpolate(distance)
            return [
                LineString(coords[:i] + [(cp.x, cp.y)]),
                LineString([(cp.x, cp.y)] + coords[i:])]

# MultiCut is define with the line to cut and the number of pieces that you want to obtain from the line
def MultiCut(line, pieces):
    
    lines_result = []
    lines_to_cut = []
    
    if pieces == 1:
        lines_result.append(line) 
    elif pieces == 2:
        distance = (line.length)/pieces
        lines_result.append(cut(line, distance)[0])
        lines_result.append(cut(line, distance)[1])
    else:
        for i in range(1, pieces):
            if i == 1:
                distance = (line.length)/pieces
                #lines_cut = cut(line, distance)
                lines_result.append(cut(line, distance)[0])
                lines_to_cut = cut(line, distance)[1]

            if  1 < i <= pieces - 2:
                distance = (line.length)/pieces
                lines_result.append(cut(lines_to_cut, distance)[0])
                lines_to_cut = cut(lines_to_cut, distance)[1]

            if (i != 1) and (i == pieces-1):
                distance = (line.length)/pieces
                lines_result.append(cut(lines_to_cut, distance)[0])
                lines_result.append(cut(lines_to_cut, distance)[1])
    
    return lines_result 