from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
#from gensim import corpora, models
#import gensim
from simhash import Simhash,SimhashIndex
import re
import xlrd
import os
from xlutils.copy import copy
import pandas as pd
import numpy as np
import time


def idProcess(name):
    filename = name
    df = pd.read_csv(filename)

    #sheetList=list(df.keys())
    #print(sheetList)

    data=np.array(df)
    print(data)
    #print(data)
    print(data.shape)
    length=data.shape[0]


    for i in range(length):#(0-64399)
        #print(data[i,1])
        temp=data[i,0].split(',')
        if int(data[i,2])==1:
            data[i,0]=temp[2:]
            print(data[i,0])
        elif len(temp)>=3:
            data[i,0]=temp[1:]
        else:
            data[i,0]=temp[1:]
        syns=data[i,1][1:-1]
        syns=syns.split('],[')
        #print(j)
        temp1=[]
        for syn in syns:
            temp=syn[3:-3]
            #print(temp)
            temp=temp.split('""","""')
            #print(temp)
            temp1.append(temp)
        data[i,1]=temp1
        #print(data[i,1])
        if int(data[i,2])==0:
            for k in range(len(data[i,1])-1,-1,-1):# i行第k个syn列表
                for disease in data[i,1][k]:
                    matched = re.match(r'[A-Za-z]+[\d]+', disease)
                    if matched:
                        #print(disease)
                        '''if data[i,0]==['DOID:80356']:
                            print(data[i,0])'''
                        ID=data[i,0].pop(k)
                        popid=[ID]
                        poplist=data[i,1].pop(k)
                        #print(popid,poplist)
                        temp=np.array([popid,poplist,0],dtype=object).reshape(1,3)
                        data=np.concatenate([data,temp])
                        #print(k,i,data.shape[0],data[-1])
                        break

    emptyList=[]
    #[DOIS:222  nsioasd]
    for i in range(data.shape[0]):
        if len(data[i,0])==0:
            emptyList.append(i)
        elif type(data[i,0])!=type([]) and type(data[i,1])!=type([]):#array的两个列表长度都为1时会自动变为长度2的列表，需要区分处理
            tempStr='1,'+data[i,0]
            data[i,0]=tempStr

            data[i,1]='["""'+data[i,1]+'"""]'
            #print(data[i,1])
        else:
            tempLen=len(data[i,0])
            tempStr=str(tempLen)+','
            for j in data[i,0]:
                tempStr=tempStr+j+','
            tempStr=tempStr[:-1]
            data[i,0]=tempStr
            if type(data[i,1][0])!=type([]):
                data[i,1]=[data[i,1]]
            tempStr=''
            for list1 in data[i,1]:
                tempStr=tempStr+'['
                for names in list1:
                    tempStr=tempStr+'"""'+names+'""",'
                tempStr=tempStr[:-1]+'],'
            tempStr=tempStr[:-1]
            data[i,1]=tempStr

    emptyList.sort(reverse=True)
    for i in emptyList:
        data=np.delete(data,i,axis=0)


    data=pd.DataFrame(data,columns=['ID','Syn','CrossReference'])
    data.to_csv(name[:-4]+'_ID'+".csv",index=False)
    '''pdWriter = pd.ExcelWriter(name[0:17]+'_1908082'+".xlsx")
    df['DO'].to_excel(pdWriter, sheet_name="DO", index=False)
    df['ICD10CM'].to_excel(pdWriter, sheet_name="ICD10CM", index=False)
    df['ICD10'].to_excel(pdWriter, sheet_name="ICD10", index=False)
    df['MeSH'].to_excel(pdWriter, sheet_name="MeSH", index=False)
    data.to_excel(pdWriter, sheet_name="merged", index=False)
    df['xref'].to_excel(pdWriter, sheet_name="xref", index=False)
    pdWriter.save()
    pdWriter.close()'''

'''for i in [0,3,5,6,7,8,9,10]:
    print(i)
    idProcess('merged190821_'+str(i)+'.csv')'''

#idProcess('merged(IDfixed)_10.xlsx')


