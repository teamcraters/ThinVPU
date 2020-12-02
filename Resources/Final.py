# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 12:12:51 2020

@author: shrav
"""

import glob
import cv2
import numpy as np
import copy
import os, gdal
from PIL import Image
import crater_detect as cd
Image.MAX_IMAGE_PIXELS = None
import pandas as pd
pd.options.display.max_columns=15
#import U_Sun_Cal as usun

# Spilting the images
in_path = os.path.abspath('D:/CDA_Intuitive/LowMB/M1233757731LC_pyr.tif')
out_path = os.path.abspath('D:/CDA_Intuitive/M1233757731LC_pyr01/out')
output_filename = 'tile'

# dimensions of each images
tile_size_x = 2000
tile_size_y = 2000

# Opening the image using gdal
ds = gdal.Open(in_path)
band = ds.GetRasterBand(1)
xsize = band.XSize
ysize = band.YSize

for i in range(0, xsize, tile_size_x):
    for j in range(0, ysize, tile_size_y):
        print("values are" + str(i)+ ", " + str(j))
        com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path) + " " + str(out_path) + str(output_filename) + str(i) + "_" + str(j) + ".tif"
        os.system(com_string)
        
cv2.destroyAllWindows()
debug_plots = False # Turning this on displays more details on the output img

# considering empty list, to append all center_lists
main_list=[]

# OpenCV Initialization
Internal = cd.InternalClass()

# Specifying split images folder path
path = glob.glob("D:/CDA_Intuitive/M1233757731LC_pyr01/*.tif")

#calculating usun
#a,b = usun.calculate_usun()
#print(a)
#print(b)
image_no = 1
# Iterating throught images folder
for img in path:
    imgo= cv2.imread(img, cv2.IMREAD_COLOR)
    imagein = copy.deepcopy(imgo)
    u_sun = np.array([0,1])
    print(u_sun)

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
    framec = cv2.resize(imagein, (1000, 1000), interpolation = cv2.INTER_AREA)
    # Saving the generated crater found images into folder
    name = 'D:/CDA_Intuitive/M1233757731LC_pyr01/file_' + str(image_no) + '.jpg'
    cv2.imwrite(name, framec)
    image_no += 1
    
    # Appending each center_list of each image to main_list
    main_list.append(center_list)
main_list
print(main_list)
# Reading the metadata file
#df1=pd.read_csv(r'C:/Users/s/Desktop/crater_nav/metadata_info.txt',delimiter=",")
df1 = pd.read_csv(r'D:/CDA_Intuitive/metadata_info.txt',delimiter=",")

# Retrieving the specific metadata row based on the input
result = df1.loc[df1['Image Name'] == 'M1233757731LC_pyr.tif']

# Creating a empty dataframe with columns
cal_values = pd.DataFrame(columns = ['center_x','center_y','lat','long']) 

# Cleansing the main lists as it contains the data as [[(1,2),(2,3)],[(3,4),(4,5),(5,6)]] - Nested Comprehension list
flattened  = [val for sublist in main_list for val in sublist]

# Calculating the length of final list flattened
no_of_records = len(flattened)-1

# Building a dataframe, by using the inputs of length of the list and metadata
initial_df = result.append([result]*no_of_records,ignore_index=True)

for x,y in flattened:
    
    s_lat = (result['Upper left latitude'] - result['Lower left latitude']) / (0 - result['Image lines'])
    d_lat = (y-0)
    latc = (s_lat * d_lat + result['Upper left latitude']).to_string()

# Calculating the longitude of crater. 

    s_long = (result['Upper left longitude'] - result['Upper right longitude']) / (39 -result['Line samples'])
    d_long = (x-39)
    longc = (s_long * d_long + result['Lower left longitude']).to_string()
    
    cal_values = cal_values.append({'center_x': x, 'center_y': y,'lat': latc,'long': longc},  ignore_index=True)

#final_df=pd.concat([initial_df,cal_values], axis=1)
#print(final_df)
frames = [initial_df,cal_values]
final_df = pd.concat(frames, axis=1)
print(final_df)
final_df.to_csv('D:/CDA_Intuitive/M1233757731LC_pyr01.csv', index=False,header=True)
