# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 08:19:19 2020

@author: shrav
"""

import pandas as pd
import numpy as np

df=pd.read_csv(r'D:/CDA_Intuitive/Metadata_USUN.txt',delimiter="\t")
new = df.loc[df['Image Name'] == 'M1260669909RC_pyr.tif']

lro_4direction = new.loc[((new['Lro flight direction'] == '-X') & (new['North azimuth'] < 180 ))]
Theta4 = (lro_4direction['North azimuth'] - 90)
Angle_Sun= (lro_4direction ['Sub solar azimuth'] + Theta4)
U4 = ((Angle_Sun + 180) - 360)
lro_4direction['U_sun_x'] = np.cos(-U4)
lro_4direction['U_sun_y']= np.sin(-U4)
lro_4direction

lro_1direction = new.loc[((new['Lro flight direction'] == '+X') & (new['North azimuth'] < 180 ))]
Theta1 = (270 - lro_1direction['North azimuth'] )
Angle_Sun= (lro_1direction ['Sub solar azimuth'] + Theta1)
U1 = Angle_Sun + 180
lro_1direction['U_sun_x'] = np.cos(U1)
lro_1direction['U_sun_y']= np.sin(U1)
lro_1direction

lro_2direction = new.loc[((new['Lro flight direction'] == '+X') & (new['North azimuth'] >= 180 ))]
Theta2 = (270 - lro_2direction['North azimuth'] )
Angle_Sun= (lro_2direction ['Sub solar azimuth'] + Theta2)
U2 = Angle_Sun + 180
lro_2direction['U_sun_x'] = np.cos(U2)
lro_2direction['U_sun_y']= np.sin(U2)
new = lro_2direction[['U_sun_x','U_sun_y']]
print(new.dtypes)
