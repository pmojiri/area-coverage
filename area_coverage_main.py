#!/usr/bin/python
######################################################################################################################################################
# File name: area_coverage_main.py                                                                                                                   #
# Author: Parisa Mojiri Forooshani                                                                                                                   #
# Date created: 10/07/2014                                                                                                                           #
# Date last modified: 25/02/2015                                                                                                                     #
# Description: Sensor-based area coverage algorithm for a known, 2D simple polygonal static environment containing simple static polygonal obstacles #
#               Algorithm: a modification of Boustrophen Cellulat Decompostion (BCD)                                                                 #
#               Input: The input to the BCD algorithm is a binary map separating obstacles from the free space that is to be covered                 #
#               Cellular decomposition: Find critical points and cell determiation                                                                   #
#               Reeb graph construction: Reeb graph G = (V,E)                                                                                        #
#               Chinese Postman Problem (CPP): the output is an eulerian circuit                                                                     #
#               Per-cell motions: creates a sequenc of waypoints forming sweeping lines                                                              #
#               Map manager: creates a sequence of GPS (lat,lon) waypoints forming sweeping lines for each robot as the output of the algorithm      #
######################################################################################################################################################

from Read_map import read_map
from Critical_points import critical_points
from Cells import cell
from Graph import reeb_graph
from Boustrophedon_motions import boustrophedon_motions
from map_manager import MapManager

import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

# initialize the map, its size, its zoom rate
WINDOW_NAME = "Map"
MAP_HEIGHT = 640
ZOOM = 18
#starting_coords = (43.770572, -79.507184)  # stong pond
#starting_coords = (43.770972, -79.507276) # stong pond zoom 20
starting_coords = (43.723522, -79.801030) # loafers lake, brampton


# save the map
manager = MapManager(MAP_HEIGHT, ZOOM, starting_coords[0], starting_coords[1])
distance = manager.linear_meters_in_map
print manager.linear_meters_in_map


# read the map and cread a binary map
areamap = read_map()
mapfile = "map_stong.png"
mapfile = "map_zoom20.png"
mapfile = "square.png"
mapfile = "Ellipes.png"
mapfile = "map_loafers_2.jpg"
bitmap = areamap.convert_to_binary(mapfile)


# Cellural Decompostion
# find critical points and draw them
criticalpoints = critical_points()
cp = criticalpoints.find_cp(bitmap)
print cp

# construct cells
cells = cell()
all_cells = cells.cell_construction(bitmap)
print all_cells


# reeb graph construction(Reeb graph G = (V,E))
graph = reeb_graph()
g = graph.reeb_graph_construction(cp, all_cells, "map_loafers_1.jpg")
print g


# Chinese Postman Problem (CPP)
# construct new reeb graph to be eulerian (Identify and duplicate a certain set of edges to provide an even degree for corresponding vertices)
g_eulerian, new_cells = graph.eulerian_reeb_graph(g, all_cells)
print g_eulerian, new_cells.shape[0]

# eulerian list (CPP-chineese postman problem):
eulerian_list = graph.eulerian_list(g_eulerian)
print eulerian_list

# eulerian cells
eulerian_cells = graph.eulerian_cells(eulerian_list, new_cells)
print eulerian_cells


# Per-cell motions
# per-cells back and forth motions (Boustrophedon motions):
footprint_meter = 12 # footprint of fleet (meter)
diameter = 4  # meter of safe area to minnows have a turn
m_position = 4 # minnow footprint (meter)
footprint_pixel = (MAP_HEIGHT / distance) * footprint_meter
print footprint_meter, footprint_pixel
diameter_pixel = (MAP_HEIGHT / distance) * diameter
m_position_pixel = int((MAP_HEIGHT / distance) * m_position)
waypoints = boustrophedon_motions()
cell_waypoinys , cell_waypoints_m1_array, cell_waypoints_m2_array = waypoints.percell_motions(footprint_pixel, eulerian_list, eulerian_cells, diameter_pixel, m_position_pixel,  "map_loafers.jpg")


# Map manager
# convert image points to lat/lon values and save them in text files
cell_waypoints_latlon = manager.get_waypoints_as_lat_lon_list(cell_waypoinys)
cell_waypoints_m1_latlon = manager.get_waypoints_as_lat_lon_list( cell_waypoints_m1_array)
cell_waypoints_m2_latlon = manager.get_waypoints_as_lat_lon_list( cell_waypoints_m2_array)
#print cell_waypoints_latlon, cell_waypoints_m1_latlon, cell_waypoints_m2_latlon

# Output is sequence of GPS waypoints for a fleet of robots with coverage footprint f that should be traversed through all cells to cover the entire environment
f_e = open('waypoints.txt', 'w')
for i in range (0, cell_waypoints_latlon.shape[0]):
  for j in range (0, len(cell_waypoints_latlon[i][0])):
    x = cell_waypoints_latlon[i][0][j][0]
    y = cell_waypoints_latlon[i][0][j][1]
    data = str(x) + "," + str(y) + "\n"
    f_e.write(data)
f_e.close()

f_m1 = open('waypoints_m1.txt', 'w')
for i in range (0, cell_waypoints_m1_latlon.shape[0]):
  for j in range (0, len(cell_waypoints_m1_latlon[i][0])):
    x = cell_waypoints_m1_latlon[i][0][j][0]
    y = cell_waypoints_m1_latlon[i][0][j][1]
    data = str(x) + "," + str(y) + "\n"
    f_m1.write(data)
f_m1.close()

f_m2 = open('waypoints_m2.txt', 'w')
for i in range (0, cell_waypoints_m2_latlon.shape[0]):
  for j in range (0, len(cell_waypoints_m2_latlon[i][0])):
    x = cell_waypoints_m2_latlon[i][0][j][0]
    y = cell_waypoints_m2_latlon[i][0][j][1]
    data = str(x) + "," + str(y) + "\n"
    f_m2.write(data)
f_m2.close()





















