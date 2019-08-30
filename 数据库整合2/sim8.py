#LCS

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



def LCS(str1,str2):
    len1=len(str1)
    len2=len(str2)
    matrix=np.zeros([len1+1,len2+1],dtype=int)
    for i in range(len1):
        for j in range(len2):
            if str1[i]==str2[j]:
                matrix[i+1,j+1]=matrix[i,j]+1
            else:
                matrix[i+1,j+1]=max(matrix[i+1,j],matrix[i,j+1])
    #print(matrix)
    return(matrix[len1,len2])

def idProcess(name):
    filename = name
    df = pd.read_csv(filename)
    #df=pd.read_excel(filename,sheet_name='merged')
    #sheetList=list(df.keys())
    #print(sheetList)

    data=np.array(df)
    data2=[]
    #print(data)
    print(data.shape)
    length=data.shape[0]

    for i in range(length):#(0-64399)

        #print(data[i,1])
        temp=data[i,0].split(',')
        if len(temp)>=3:
            data[i,0]=temp[1:]
        else:
            data[i,0]=temp[1:]
            #data[i,0]=temp     #id列ID数为1时若没写1就用这个，否则用上面一行的
        syns=data[i,1][1:-1]
        syns=syns.split('],[')

        temp1=[]
        for syn in syns:
            temp=syn[3:-3]
            #print(temp)
            temp=temp.split('""","""')
            #print(temp)
            temp1.append(temp)
        data[i,1]=temp1
        #data[i]由字符串转化为列表
        if len(data[i,0])==1 or int(data[i,2])==1:
            continue
        else:
            rates=np.zeros([len(data[i,1]),len(data[i,1])],dtype=float)
            for k in range(len(data[i,1])-1,0,-1):
                for l in range(k-1,-1,-1):
                    print(i,k,l)
                    if l!=k:
                        largestRate=0.

                        for disease1 in data[i,1][k]:
                            for disease2 in data[i,1][l]:
                                temp1=disease1.lower()
                                temp2=disease2.lower()
                                temp1=temp1.split(' ')
                                temp2=temp2.split(' ')
                                temp1.sort()
                                temp2.sort()
                                temp1=' '.join(temp1)
                                temp2=' '.join(temp2)

                                lcslength=LCS(temp1,temp2)
                                tempRate=max(lcslength/len(disease1),lcslength/len(disease2))
                                if tempRate>largestRate:
                                    largestRate=tempRate
                        rates[k,l]=largestRate
                        rates[l,k]=largestRate

            indexList=[]
            for k in range(len(data[i,1])):
                #print(np.max(rates[k]))
                if np.max(rates[k])<=0.5:
                    indexList.append(k)
            indexList.sort(reverse=True)
            if indexList!=[]:
                #print(np.array([indexList,data[i,1]],dtype=object))
                #temp=np.array([indexList,data[i,1]],dtype=object).reshape(1,2)

                temp=[indexList,data[i,1].copy()]
                data2.append(temp)

            for k in indexList:
                tempID=data[i,0].pop(k)
                popid=[tempID]
                poplist=data[i,1].pop(k)
                temp=np.array([popid,poplist,0],dtype=object).reshape(1,3)
                data=np.concatenate([data,temp])




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
    data.to_csv(name[:-4]+'_LCS.csv',index=False)
    if len(data2)>0:
        data2 = np.array(data2, dtype=object)
        data2=pd.DataFrame(data2,columns=['List',"Syns"])
        data2.to_csv(name[:-4]+'_LCSlog2.csv',index=False)
    '''pdWriter = pd.ExcelWriter(name[0:17]+'_1908082'+".xlsx")
    df['DO'].to_excel(pdWriter, sheet_name="DO", index=False)
    df['ICD10CM'].to_excel(pdWriter, sheet_name="ICD10CM", index=False)
    df['ICD10'].to_excel(pdWriter, sheet_name="ICD10", index=False)
    df['MeSH'].to_excel(pdWriter, sheet_name="MeSH", index=False)
    data.to_excel(pdWriter, sheet_name="merged", index=False)
    df['xref'].to_excel(pdWriter, sheet_name="xref", index=False)
    pdWriter.save()
    pdWriter.close()'''
'''for iii in [0,3,5,6,7,8,9,10]:
    idProcess('merged190821_'+str(iii)+'_ID.csv')'''



