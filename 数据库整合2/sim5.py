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
import time
import jieba

import toExcel
#toExcel.filesToExcel()
#OriginalFile = pd.read_excel("test1.xls", None)
#print(type(OriginalFile['merged']['Syn'][1]))

#seg_list = jieba.cut('胃癌影像数据')
#print(u"[默认模式]: ", "/ ".join(seg_list))

filename = "胃癌影像数据.xlsx"
workbook = xlrd.open_workbook(filename)
def get_simhash_topics(sheet_name):
    sheet = workbook.sheet_by_name(sheet_name)
    col0 = sheet.col_values(0)
    col1=sheet.col_values(1)
    col2=sheet.col_values(2)
    col3=sheet.col_values(3)
    col4=sheet.col_values(4)
    col5=sheet.col_values(5)
    col6=sheet.col_values(6)
    cols_jczd=sheet.col_values(7)
    doc_list = []
    for index, col in enumerate(cols_jczd):
        if index == 0:
            continue
        if col == '':
            col = []
        doc_list.append(col)
    # 第一阶段：清洗文档，结果是文本texts
    simhash_topics = []
    for index,doc_set in enumerate(doc_list):
        doc_tokens=[]
        seg_list = jieba.cut(doc_set)
        a="/ ".join(seg_list)
        a=a.split('/')
        doc_tokens=list(set(seg_list))
        #print(doc_tokens)
        simhash_topics.append((a, col0[index+1],col1[index+1],col2[index+1],
                               col3[index+1],col4[index+1],col5[index+1],
                               col6[index+1],doc_set))
        #print(simhash_topics[-1])
    return simhash_topics
def getObjs(objects,base):
    for i,j in enumerate(base):
        #print(j)
        if objects!=[]:
            objects.append((str(int(objects[-1][0])+1),Simhash(j[0])))
        else:
            objects.append((str(i),Simhash(j[0])))

SimhashObjs=[]

DO = get_simhash_topics("原始数据")
print('len    %d'%(len(DO)))
print(DO)
getObjs(SimhashObjs,DO)
print(SimhashObjs)


#print(DO)
def contrast(threshold):
    SimIndex=SimhashIndex(SimhashObjs,k=threshold)
    df=pd.DataFrame({"ID":[],"Syn":[]})
    df2=pd.DataFrame({"ID":[],"Syn":[]})
    df3=pd.DataFrame({"姓名":[],"检查号":[],"报告日期":[],"临床诊断":[],"检查所见":[],
                      "检查类型":[],"检查部位":[],"检查诊断":[]})
    #a,adoc_set,aid,sheet_name,from
    dict={}         #ID：同义词表
    xref=[]         #id匹配
    IDPairList=[]   #两两匹配的ID
    unMerged=[]     #未匹配的ID
    #flags=[0 for i in range(len(DO))]   #1已配对 0未配对
    for i in range(len(DO)):
        print('\r'+str(i),end='',flush=True)
        #print(DO[i][0])
        near = SimIndex.get_near_dups(Simhash(DO[i][0]))
        if len(near) == 1:  # 未匹配
            '''str1 = '['
            for k in DO[i][1]:
                str1 = str1 + '"""' + str(k) + '""",'
            str1 = str1[:-1] + ']' 
            '''
            unMerged.append(str(i))
        # elif len(near)>1 and idMatched==0:
        elif len(near) > 1:
            IDPair = []
            if len(near) > 1:
                while len(near) > 0:
                    temp = int(near.pop())
                    '''str1 = '['
                    for k in DO[temp][1]:
                        str1 = str1 + '"""' + str(k) + '""",'
                    str1 = str1[:-1] + ']'
                    '''
                    #dict[str(DO[temp][2])] = str1
                    #flags[temp] = 1
                    IDPair.append(int(temp))
                    #print(DO[temp][1])
                IDPairList.append(IDPair)
                #print(IDPair)


    #二次查找实体对
    flagChanged=1
    while flagChanged==1:
        diseases=[]
        flags = [0 for i in range(len(IDPairList))]
        for i in range(len(IDPairList)):
            if flags[i] == 0:
                temp = []
                for ii in IDPairList[i]:
                    temp.append(int(ii))
                diseases.append(temp)
                flags[i] = 1
                for j in range(i + 1, len(IDPairList)):
                    if flags[j] == 0:
                        for k in IDPairList[j]:
                            if k in diseases[-1]:
                                #print(IDPairList[j],diseases[-1])
                                flags[j] = 1
                                for l in IDPairList[j]:
                                    diseases[-1].append(int(l))
                                break
                                #IDPairList[j]=[]
        if len(diseases)==len(IDPairList):

            flagChanged=0
            break
        IDPairList=diseases

    for i in diseases:
        IDs = list(set(i))
        '''if len(IDs)==1:
            continue'''
        '''str1 = ','.join(IDs)
        str1=str(len(IDs))+','+str1 #id数：所有id
        '''
        IDs.sort()
        #print(IDs)
        str1=str(len(IDs))+'['
        str2 = str(len(IDs)) + '['
        str3 = str(len(IDs)) + '['
        str4 = str(len(IDs)) + '['
        str5 = str(len(IDs)) + '['
        str6 = str(len(IDs)) + '['
        str7 = str(len(IDs)) + '['
        str8 = str(len(IDs)) + '['
        for id in IDs:
            str1=str1+'"""'+str(DO[id][1])+'""",'
            str2 = str2 + '"""' + str(DO[id][2]) + '""",'
            str3 = str3 + '"""' + str(DO[id][3]) + '""",'
            str4 = str4 + '"""' + str(DO[id][4]) + '""",'
            str5 = str5 + '"""' + str(DO[id][5]) + '""",'
            str6 = str6 + '"""' + str(DO[id][6]) + '""",'
            str7 = str7 + '"""' + str(DO[id][7]) + '""",'
            str8 = str8 + '"""' + str(DO[id][8]) + '""",'
        str1=str1[:-1]+']'
        str2 = str2[:-1] + ']'
        str3 = str3[:-1] + ']'
        str4 = str4[:-1] + ']'
        str5 = str5[:-1] + ']'
        str6 = str6[:-1] + ']'
        str7 = str7[:-1] + ']'
        str8 = str8[:-1] + ']'


        df1 = pd.DataFrame({"姓名": [str1], "检查号": [str2], "报告日期": [str3], "临床诊断": [str4],
                            "检查所见": [str5],"检查类型": [str6], "检查部位": [str7], "检查诊断": [str8]})
        df3 = df3.append(df1)

    for i in unMerged:
        str1 = str(DO[int(i)][1])
        str2 = str(DO[int(i)][2])
        str3 = str(DO[int(i)][3])
        str4 = str(DO[int(i)][4])
        str5 = str(DO[int(i)][5])
        str6 = str(DO[int(i)][6])
        str7 = str(DO[int(i)][7])
        str8 = str(DO[int(i)][8])
        df1 = pd.DataFrame({"姓名": [str1], "检查号": [str2], "报告日期": [str3], "临床诊断": [str4],
                            "检查所见": [str5],"检查类型": [str6], "检查部位": [str7], "检查诊断": [str8]})
        df3 = df3.append(df1)


    #df.to_csv('sim'+str(threshold)+'.csv',index=False)
    OriginalFile = pd.read_excel(filename, None)
    pdWriter = pd.ExcelWriter("检查诊断_"+str(threshold)+".xlsx")
    #OriginalFile['DO'].to_excel(pdWriter, sheet_name="DO", index=False)
    #OriginalFile['ICD10CM'].to_excel(pdWriter, sheet_name="ICD10CM", index=False)
    #OriginalFile['ICD10'].to_excel(pdWriter, sheet_name="ICD10", index=False)
    #OriginalFile['MeSH'].to_excel(pdWriter, sheet_name="MeSH", index=False)
    df3.to_excel(pdWriter, sheet_name="merged", index=False)
    #df2.to_excel(pdWriter,sheet_name="xref",index=False)
    pdWriter.save()
    pdWriter.close()

start=time.perf_counter()
contrast(15)
dur1=time.perf_counter()
print("time:",dur1-start)
contrast(20)
dur2=time.perf_counter()
print("time:",dur2-dur1)
contrast(5)
dur3=time.perf_counter()
print("time:",dur3-dur2)
contrast(6)
dur4=time.perf_counter()
print("time:",dur4-dur3)
contrast(7)
dur5=time.perf_counter()
print("time:",dur5-dur4)
contrast(8)
dur6=time.perf_counter()
print("time:",dur6-dur5)
contrast(9)
dur7=time.perf_counter()
print("time:",dur7-dur6)
contrast(10)
dur8=time.perf_counter()
print("time:",dur1-start,'\n',
      dur2-dur1,'\n',
      dur3-dur2,'\n',
      dur4-dur3,'\n',
      dur5-dur4,'\n',
      dur6-dur5,'\n',
      dur7-dur6,'\n',
      dur8-dur7)