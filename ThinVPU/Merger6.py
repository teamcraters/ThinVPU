# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 15:30:45 2020

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
import usun as usun
        
cv2.destroyAllWindows()
debug_plots = False # Turning this on displays more details on the output img

# considering empty list, to append all center_lists
main_list=[]

# OpenCV Initialization
Internal = cd.InternalClass()

# Specifying split images folder path
path = glob.glob("D:/CDA_Intuitive/output1/*.tif")

# Iterating throught images folder
for img in path:
    imgo= cv2.imread(img, cv2.IMREAD_COLOR)
    imagein = copy.deepcopy(imgo)
    u_sun_values = usun.calculate_usun()
    print(u_sun_values)
    a= u_sun_values['U_sun_x']
    b= u_sun_values['U_sun_y']
    print(a.dtypes)
    print(b.dtypes)
    u_sun = np.array([a,b])

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
    cv2.imwrite('new13.png', framec)
    
    # Appending each center_list of each image to main_list
    main_list.append(center_list)
main_list
print(main_list)
# Reading the metadata file
df1=pd.read_csv(r'D:/CDA_Intuitive/metadata_info.txt',delimiter=",")

# Retrieving the specific metadata row based on the input
result = df1.loc[df1['Image Name'] == 'M1260669909RC_pyr.tif']

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

# Calculating the longitude of crater. xc should be replaced by the from imgcor data farme 'crater x'
# insert the crater x

    s_long = (result['Upper left longitude'] - result['Upper right longitude']) / (39 -result['Line samples'])
    d_long = (x-39)
    longc = (s_long * d_long + result['Lower left longitude']).to_string()
    
    cal_values = cal_values.append({'center_x': x, 'center_y': y,'lat': latc,'long': longc},  ignore_index=True)

final_df=pd.concat([initial_df,cal_values], axis=1)
print(final_df)
final_df.to_csv('D:/CDA_Intuitive/output1.csv', index=False,header=True)

