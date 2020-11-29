import pandas as pd
import numpy as np
#from geopy import distance
from geopy.distance import geodesic
#from vincenty import vincenty
craters = pd.read_csv('C:/Users/Ujjwala Potluri/Desktop/UHCL/Capstone Project/craters.csv')
robins = pd.read_csv('C:/Users/Ujjwala Potluri/Desktop/UHCL/Capstone Project/robins.csv')

df_all = pd.merge(craters.assign(key=0), robins.assign(key=0), on='key').drop('key', axis=1)
df_all['MILES'] = df_all.apply(
    (lambda row: geodesic(
        (row['crater_lat'], row['crater_long']),
        (row['robins_lat'], row['robins_long'])
    ).miles),
    axis=1
)


closest = df_all.loc[df_all.groupby(['crater_lat', 'crater_long'])["MILES"].idxmin()]

#closest.to_excel('C:/Users/Ujjwala Potluri/Desktop/UHCL/Capstone Project/output2.xlsx', index=False,header=True)

#adding the 'the Result' column to the data frame  
conditions = [
    (closest['MILES'] == 0),
    (closest['MILES'] <= 2), 
    (closest['MILES'] >= 2.1)

    ]

# create a list of the values we want to assign for each condition
values = ['Exact Matched', 'Nearest match with 2 miles', 'Craters more than 2 miles']

# create a new column and use np.select to assign values to it using our lists as arguments
closest['The Result'] = np.select(conditions, values)

closest.to_csv('C:/Users/Ujjwala Potluri/Desktop/UHCL/Capstone Project/sampleoutput2.csv', index=False,header=True)