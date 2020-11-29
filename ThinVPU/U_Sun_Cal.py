# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 13:40:46 2020

@author: Sahar
"""


import pandas as pd
import numpy as np

def calculate_usun():
#Read the .txt metadata dataset 
    #df = pd.read_csv(r'C:/Users/s/Desktop/crater_nav/resource/Metadata_USUN.txt',delimiter=",")
    df = pd.read_excel (r'C:/Users/s/Desktop/crater_nav/resource/Metadata_usun.xlsx')

    new = df.loc[df['Image Name'] == 'M1260669909RC_pyr.tif']

    lro_4direction = new.loc[((new['Lro flight direction'] == '-X') & (new['North azimuth'] < 180 ))]
    Theta4 = (lro_4direction['North azimuth'] - 90)
    Angle_Sun= (lro_4direction ['Sub solar azimuth'] + Theta4)
    U4 = ((Angle_Sun + 180) - 360)
    lro_4direction['U_sun_x'] = np.cos(-U4)
    lro_4direction['U_sun_y']= np.sin(-U4)
    #result1 = lro_4direction[['U_sun_x','U_sun_y']]

    lro_3direction = new.loc[((new['Lro flight direction'] == '-X') & (new['North azimuth'] >= 180 ))]
    Theta3 = (lro_3direction['North azimuth'] - 270)
    Angle_Sun= (lro_3direction ['Sub solar azimuth'] + Theta3)
    U3 = ((Angle_Sun + 180) - 360)
    lro_3direction['U_sun_x'] = np.cos(-U3)
    lro_3direction['U_sun_y']= np.sin(-U3)
    #result2 = lro_3direction[['U_sun_x','U_sun_y']]
    
    lro_2direction = new.loc[((new['Lro flight direction'] == '+X') & (new['North azimuth'] >= 180 ))]
    Theta2 = (270 - lro_2direction['North azimuth'] )
    Angle_Sun= (lro_2direction ['Sub solar azimuth'] + Theta2)
    U2 = Angle_Sun + 180
    lro_2direction['U_sun_x'] = np.cos(U2)
    lro_2direction['U_sun_y']= np.sin(U2)
    #result3 = lro_2direction[['U_sun_x','U_sun_y']]

    lro_1direction = new.loc[((new['Lro flight direction'] == '+X') & (new['North azimuth'] < 180 ))]
    Theta1 = (270 - lro_1direction['North azimuth'] )
    Angle_Sun= (lro_1direction ['Sub solar azimuth'] + Theta1)
    U1 = Angle_Sun + 180
    lro_1direction['U_sun_x'] = np.cos(U1)
    lro_1direction['U_sun_y']= np.sin(U1)
    #result4 = lro_1direction[['U_sun_x','U_sun_y']]

    frames = [lro_4direction, lro_2direction, lro_3direction, lro_1direction]
    result = pd.concat(frames)
    new1 = result[['U_sun_x', 'U_sun_y']]
    a= new1.loc[4437].at['U_sun_x']
    b= new1.loc[4437].at['U_sun_y']
    return a,b


val = calculate_usun()
print(val)