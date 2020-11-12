# -*- coding: utf-8 -*-
import pandas as pd 
import os
import numpy as np 
from xlsxwriter.utility import xl_rowcol_to_cell 
 
template = pd.read_excel('C:/Users/anirv/OneDrive/Desktop/FALL 2020/Capstone/compare/Robins.xlsx',na_values=np.nan,header=None) 
testSheet = pd.read_excel('C:/Users/anirv/OneDrive/Desktop/FALL 2020/Capstone/compare/Crater.xlsx',na_values=np.nan,header=None) 
 
rt,ct = template.shape 
rtest,ctest = testSheet.shape 
 
df = pd.DataFrame(columns=['Cell_Location','Robins','Crater']) 
 
for rowNo in range(max(rt,rtest)): 
    for colNo in range(max(ct,ctest)): 
        # Fetching the template value at a cell 
        try: 
            template_val = template.iloc[rowNo,colNo] 
        except: 
            template_val = np.nan 
         
        # Fetching the testsheet value at a cell 
        try: 
            testSheet_val = testSheet.iloc[rowNo,colNo] 
        except: 
            testSheet_val = np.nan 
             
        # Comparing the values 
        if (str(template_val)!=str(testSheet_val)): 
            cell = xl_rowcol_to_cell(rowNo, colNo) 
            dfTemp = pd.DataFrame([[cell,template_val,testSheet_val]], 
                                  columns= ['Cell_Location','Robins','Crater']) 
            df = df.append(dfTemp)
            #comparing
           # comparevalues = template.values == testSheet.values
            
#print(comparevalues)

#rows,cols = np.where(comparevalues==False)

##for item in zip(rows,cols):
    #df.iloc[item[0],item[1]] = ' {} --> {} '.format(template.iloc[item[0], item[1]], testSheet.iloc[item[0],item[1]])
#path='C:/Users/anirv/OneDrive/Desktop/FALL 2020/Capstone/compare/'
#file = 'myoutput.xlsx'
#with open(os.path.join(path,file),'w') as fp:
   # pass

df.to_excel('C:/Users/anirv/OneDrive/Desktop/FALL 2020/Capstone/compare/output22.xlsx','w',index=False,header=True)

