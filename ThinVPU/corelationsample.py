import pandas as pd
import numpy as np
#from geopy import distance
from geopy.distance import geodesic
#from vincenty import vincenty
craters = pd.read_csv('C:/Users/Ujjwala Potluri/Desktop/UHCL/Capstone Project/craterdata.csv')
robins = pd.read_csv('C:/Users/Ujjwala Potluri/Desktop/UHCL/Capstone Project/robinsdata.csv')

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
    (closest['MILES'] ==0),
    (closest['MILES'].between(0.01, 0.5)),
    (closest['MILES'].between(0.5001, 1.0)),
    (closest['MILES'].between(1.0001,2.0)),
    (closest['MILES'].between(2.0001,3.0)),
    (closest['MILES'].between(3.0001,4.0)),
    (closest['MILES'].between(4.0001,5.0)),
    (closest['MILES'] >=5.0001)
    #(closest['MILES'] = range (0.51, 1)),
    #(closest['MILES'] = range(1.01,2.0)),
    #(closest['MILES'] = range(2.01,3.0)),
    #(closest['MILES'] = range(3.01,4.0)),
    #(closest['MILES'] = range(4.01,5.0)),
    #(closest['MILES'] >=5)
    

    ]

# create a list of the values we want to assign for each condition
values = ['Exact Match', 'Exact Match', 'Crater located withn 0.5 to 1 miles range','Crater located within 1 to 2 miles range','Crater located within 2 to 3 miles range','Crater located within 3 to 4 miles range','Crater located within 4 to 5 miles range','Crater located outside 5 miles range']

# create a new column and use np.select to assign values to it using our lists as arguments
closest['The Result'] = np.select(conditions, values)

closest.to_csv('C:/Users/Ujjwala Potluri/Desktop/UHCL/Capstone Project/correlationresult3.csv', index=False,header=True)