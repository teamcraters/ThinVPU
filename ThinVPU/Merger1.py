# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:30:45 2020

@author: shrav
"""

import glob
import cv2
import numpy as np
import copy
import matplotlib.pyplot as plt
import os, gdal
from os import listdir
from os.path import isfile, join
from PIL import Image
import crater_detect as cd
Image.MAX_IMAGE_PIXELS = None

# Spiltting the images
in_path = os.path.abspath('D:/CDA_Intuitive/pics/M1273914000RC_pyr.tif')
out_path = os.path.abspath('D:/CDA_Intuitive/output1/out')
output_filename = 'tile'

tile_size_x = 3000
tile_size_y = 3000

ds = gdal.Open(in_path)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize

for i in range(0, xsize, tile_size_x):
    for j in range(0, ysize, tile_size_y):
        print("values are" + str(i)+ ", " + str(j))
        #com_string = "gdal_translate -of GTIFF -srcwin " + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(output_filename) + str(i) + "_" + str(j) + ".tif"
        com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
        os.system(com_string)

cv2.destroyAllWindows()
debug_plots = False # Turning this on displays more details on the output img
main_list=[]

# OpenCV Initialization
Internal = cd.InternalClass()
path = glob.glob("D:/CDA_Intuitive/output1/*.tif")
for img in path:
    imgo= cv2.imread(img, cv2.IMREAD_COLOR)
    imagein = copy.deepcopy(imgo)
    u_sun = np.array([1.0, 0])

    # Adjust the tuning parameters
    Internal.params.light_thresh_mult = 1.0  # standard deviation for specular regions
    Internal.params.shadow_thresh_mult = 1.0 # standard deviation for shadow regions
    Internal.params.area_frac_threshold = .7  # minimum fraction of found features area to fit circle area
    Internal.params.max_shadow_contour_area = 1000*1000  # maximum shadow feature area
    Internal.params.max_light_contour_area = 1000*1000  # maximum specular feature area
    Internal.params.min_light_contour_area = 7  # minimum specular feature area
    Internal.params.min_shadow_contour_area = 70  # minimum shadow feature area

    # Run the CDA algorithm
    shadows, lights, found_craters, center_list = cd.detectCrater(imagein, Internal, u_sun, False)
    main_list.append(center_list)

print(main_list)


