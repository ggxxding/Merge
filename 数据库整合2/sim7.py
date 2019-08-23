#先按id匹配，根据最大类数调整阈值
#问题：flags=1的影响
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
#import toExcel
#toExcel.filesToExcel()
#OriginalFile = pd.read_excel("test1.xls", None)
#print(type(OriginalFile['merged']['Syn'][1]))


filename = "base3(IDfixed).xlsx"
workbook = xlrd.open_workbook(filename)
def get_simhash_topics(sheet_name):
    sheet = workbook.sheet_by_name(sheet_name)
    cols = sheet.col_values(3)      #同义词列表
    #print(cols)
    cols_name = sheet.col_values(2) #名称
    cols_id = sheet.col_values(0)   #id
    cols_ids=sheet.col_values(1)
    doc_list = []
    for index, col in enumerate(cols):
        if index == 0:
            continue
        if col == '':
            col = []
        else:
            col = eval(col)
        col = set(col)
        col.add(cols_name[index])
        col=list(col)
        #print(col)
        doc_list.append(col)
    #print(doc_list)
    tokenizer = RegexpTokenizer(r'\w+')  # 1匹配所有单字字符，直到其遇到像空格这样的非单字的字符。
    en_stop = get_stop_words("en")  # 1移除停用词
    p_stemmer = PorterStemmer()  # 1词干提取
    # 第一阶段：清洗文档，结果是文本texts
    simhash_topics = []
    for index,doc_set in enumerate(doc_list):
        id = cols_id[index+1]
        ids=cols_ids[index+1]
        ids=eval(ids)
        ids.append(id)
        ids=list(set(ids))
        #print(ids)
        #ids=eval(ids)
        #print(id)
        #print(ids)
        doc_tokens=[]
        for i in doc_set:
            texts = []
            raw = i.lower() #str
            #print(raw)
            tokens = tokenizer.tokenize(raw)  # 2匹配所有单字字符，直到其遇到像空格这样的非单字的字符。 list
            #print(tokens)
            stopped_tokens = [i for i in tokens if not i in en_stop]  # 2移除停用词
            stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]  # 2词干提取
            #texts.append(stemmed_tokens)
            '''print(texts)
            print(stemmed_tokens)'''
            # 第二阶段：构建 document-term matrix
            '''dictionary = corpora.Dictionary(texts)  # Dictionary() 方法遍历所有的文本，为每个不重复的单词分配一个单独的整数 ID，同时收集该单词出现次数以及相关的统计信息
            #print(i,dictionary)
            corpus = [dictionary.doc2bow(text) for text in texts]  # doc2bow() 方法将 dictionary 转化为一个词袋。得到的结果 corpus 是一个向量的列表，向量的个数就是文档数。
            #print(corpus)
            # 第三阶段：应用LDA模型
            ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=3)
            #print(ldamodel)
            topics = ldamodel.print_topics(num_topics=1, num_words=4)
            #print(topics)

            simhash_topic = re.findall('"(\w+)"', topics[0][1])
            print(simhash_topic,i,doc_set,id)
            simhash_topics.append((simhash_topic,i,doc_set,id))'''
            #print(i,stemmed_tokens)
            doc_tokens.extend(stemmed_tokens)
            #print(tokens)
            #print(stemmed_tokens,i,doc_set,id)
            #['dentin', 'secondari'] Dentin, Secondary {'Dentin, Secondary', 'Secondary Dentin'} Mesh:D003809
        doc_tokens=list(set(doc_tokens))
        simhash_topics.append((doc_tokens, doc_set, id,ids, sheet_name))
        #print(simhash_topics[-1])
        #提取词干后的同义词表，同义词表，ID，id列表，来自哪个库
    return simhash_topics

def listProceed(inputLists):
    #inputLists=[ [],[],...,[] ]
    flagChanged = 1
    while flagChanged == 1:
        tempLists = []
        flags = [0 for i in range(len(inputLists))]
        for i in range(len(inputLists)):
            if flags[i] == 0:
                temp = []
                for ii in inputLists[i]:
                    temp.append(ii)
                tempLists.append(temp)
                flags[i] = 1
                for j in range(i + 1, len(inputLists)):
                    if flags[j] == 0:
                        for k in inputLists[j]:
                            if k in tempLists[-1]:
                                flags[j] = 1
                                for l in inputLists[j]:
                                    tempLists[-1].append(str(l))
                                break
                                # IDPairList[j]=[]
        if len(tempLists) == len(inputLists):
            flagChanged = 0
            break
        inputLists = tempLists.copy()
    inputLists2=[list(set(x)) for x in inputLists]
    return inputLists2

def getObjs(objects,base):
    for i,j in enumerate(base):
        if objects!=[]:
            objects.append((str(int(objects[-1][0])+1),Simhash(j[0])))
        else:
            objects.append((str(i),Simhash(j[0])))

SimhashObjs=[]

DO = get_simhash_topics("DO")
print('lenDOID    %d'%(len(DO)))
getObjs(SimhashObjs,DO)

ICD10CM= get_simhash_topics("ICD10CM")
print('lenICD10CM %d'%(len(ICD10CM)))
getObjs(SimhashObjs,ICD10CM)

ICD10=get_simhash_topics("ICD10")
print('lenICD10   %d'%(len(ICD10)))
getObjs(SimhashObjs,ICD10)

MeSH = get_simhash_topics("MeSH")
print('lenMeSH    %d'%(len(MeSH)))
getObjs(SimhashObjs,MeSH)

print('len        %d'%(len(SimhashObjs)))
DO.extend(ICD10CM)
DO.extend(ICD10)
DO.extend(MeSH) #delete?
#print(DO)
def contrast(threshold):
    SimIndex=SimhashIndex(SimhashObjs,k=threshold)
    df=pd.DataFrame({"ID":[],"Syn":[],"CrossReference":[]})
    df2=pd.DataFrame({"ID":[],"Syn":[]})
    #a,adoc_set,aid,sheet_name,from
    dict={}         #ID：同义词表 type:list
    xref=[]         #id匹配
    IDPairList=[]   #两两匹配的ID
    IDPairSynList=[]
    unMerged=[]     #未匹配的ID
    unMergedSyn=[]
    flags=[0 for i in range(len(DO))]   #1已配对 0未配对
    idflags=[0 for i in range(len(DO))]
    for i in range(len(DO)):
        print('\r'+str(i),end='',flush=True)
        idMatched = 0
        for j in range(i + 1, len(DO)):
            idMatch = 0
            for id1 in DO[i][3]:
                if idMatch == 1:
                    break
                for id2 in DO[j][3]:
                    if id1 == id2:
                        idMatch = 1
                        idMatched = 1
                        break
            # distance_simhash=Simhash(DO[i][0]).distance(Simhash(DO[j][0]))
            if idMatch == 1:
                idMatch = 0
                idflags[i]=1
                idflags[j]=1
                dict[str(i)] = DO[i][1]  # DO[i][2]=id
                dict[str(j)] = DO[j][1]
                IDPair = [str(i), str(j)]

                IDPairList.append(IDPair)
                xref.append(IDPair)

        if flags[i]==0:
            near=SimIndex.get_near_dups(Simhash(DO[i][0]))
            if len(near)==1 and near[0]==str(i) and idMatched==0:    #未匹配
                dict[str(i)]=DO[i][1]
                unMerged.append(str(i))
                unMergedSyn.append(DO[i][1])
            #elif len(near)>1 and idMatched==0:
            elif len(near)>1:
                IDPair=[]
                if len(near)>1:
                    while len(near)>0:
                        temp=int(near.pop())
                        dict[str(temp)]=DO[temp][1]
                        #flags[temp]=1
                        IDPair.append(str(temp))
                    if len(IDPair)>1:
                        IDPairList.append(IDPair)


    #二次查找实体对,把xref中互相关联的结果并到一起
    flagChanged = 1
    while flagChanged == 1:
        xrefs = []
        flags = [0 for i in range(len(xref))]
        for i in range(len(xref)):
            # print(i)
            if flags[i] == 0:
                temp = []
                for ii in xref[i]:
                    temp.append(str(ii))
                xrefs.append(temp)
                flags[i] = 1
                for j in range(i + 1, len(xref)):
                    if flags[j] == 0:
                        for k in xref[j]:
                            if k in xrefs[-1]:
                                flags[j] = 1
                                for l in xref[j]:
                                    xrefs[-1].append(str(l))
                                break
                                # IDPairList[j]=[]
        if len(xrefs) == len(xref):
            flagChanged = 0
            break
        xref= xrefs

    # 二次查找实体对,把IDPairList中互相关联的结果并到一起
    flagChanged=1
    while flagChanged==1:
        diseases=[]

        flags = [0 for i in range(len(IDPairList))]
        for i in range(len(IDPairList)):
            # print(i)
            if flags[i] == 0:
                temp = []
                for ii in IDPairList[i]:
                    temp.append(str(ii))
                diseases.append(temp)
                flags[i] = 1
                for j in range(i + 1, len(IDPairList)):
                    if flags[j] == 0:
                        for k in IDPairList[j]:
                            if k in diseases[-1]:
                                flags[j] = 1
                                for l in IDPairList[j]:
                                    diseases[-1].append(str(l))
                                break
                                #IDPairList[j]=[]
        if len(diseases)==len(IDPairList):
            flagChanged=0
            break
        IDPairList=diseases.copy()


    #检测最大类，对该类应用阈值减小的simhash
    print(IDPairList)
    IDPairListLens = [len(list(set(x))) for x in IDPairList]
    maxLen = max(IDPairListLens)
    #print(maxLen)
    tempThreshold=threshold
    while maxLen>10 and tempThreshold>0:
        print(maxLen,tempThreshold)
        tempThreshold=tempThreshold-1
        indexList=[]    #记录大于10的类的index
        for index,IDPair in enumerate(IDPairList):
            tempIDPair=list(set(IDPair))
            if len(tempIDPair)>10:#类内进行更小阈值计算
                indexList.append(index)
                tempIDPairLists = []
                SimhashObjs2=[]
                for x in tempIDPair:
                    #print(x,DO[int(x)][0])
                    SimhashObjs2.append((str(x),Simhash(DO[int(x)][0])))
                SimIndex2 = SimhashIndex(SimhashObjs2, k=tempThreshold)
                flags=[0 for x in range(len(tempIDPair))]
                tempIDPairList=[]
                for i in range(len(tempIDPair)):
                    if flags[i]==0:
                        #print(IDPair[i])
                        near=SimIndex2.get_near_dups(Simhash(DO[int(tempIDPair[i])][0]))
                        if len(near)==1 and near[0]==tempIDPair[i]:
                            unMerged.append(str(tempIDPair[i]))
                            #dict.append
                            #unMergedSyn.append(DO[int(IDPair[i])][1])
                        elif len(near)>1:
                            tempIDPair2=[]
                            while len(near) > 0:
                                temp = near.pop()
                                #dict[str(temp)] = DO[temp][1]
                                #flags[tempIDPair.index(temp)] = 1
                                tempIDPair2.append(str(temp))
                                #print(tempIDPair2)
                            if len(tempIDPair2) > 1:
                                tempIDPairLists.append(tempIDPair2)
                tempIDPairLists=listProceed(tempIDPairLists)

                for k in tempIDPairLists:
                    diseases.append(k)
        indexList.sort(reverse=True)
        for k in indexList:
            diseases.pop(k)
        IDPairList=diseases.copy()
        IDPairListLens = [len(list(set(x))) for x in IDPairList]
        maxLen = max(IDPairListLens)


    #xref中的类转为字符串输入到dataframe中
    for i in xrefs:
        IDs=list(set(i))
        realIDs=[DO[int(x)][2] for x in IDs]
        str1= ','.join(realIDs)
        str1=str(len(realIDs))+','+'xref'+','+str1 #id数：所有id
        SynList = []
        for id in IDs:
            tempList=dict[id]
            #print(tempList)
            #print(DO[int(id)][1])
            str3 = '['
            for k in tempList:
                str3 = str3 + '"""' + str(k) + '""",'
            str3 = str3[:-1] + ']'
            SynList.append(str3)

        str2 = ','.join(SynList)
        #print(str2)
        df1 = pd.DataFrame({"ID": [str1], "Syn": [str2],"CrossReference":['1']})
        df = df.append(df1)
        df2 = df2.append(df1[["ID","Syn"]])
    # diseases中的类转为字符串输入到dataframe中
    for i in diseases:
        IDs = list(set(i))
        realIDs=[DO[int(x)][2] for x in IDs]
        '''if len(IDs)==1:
            continue'''
        str1 = ','.join(realIDs)
        str1=str(len(realIDs))+','+str1 #id数：所有id
        SynList = []
        for id in IDs:
            tempList=dict[id]
            str3 = '['
            for k in tempList:
                str3 = str3 + '"""' + str(k) + '""",'
            str3 = str3[:-1] + ']'

            SynList.append(str3)

        str2 = ','.join(SynList)
        #print(str2)
        df1 = pd.DataFrame({"ID": [str1], "Syn": [str2],"CrossReference":['0']})
        df = df.append(df1)
    # unmerged中的类转为字符串输入到dataframe中
    for i in unMerged:
        str1='1,'+DO[int(i)][2]
        tempList=dict[i]

        str2 = '['
        for k in tempList:
            str2 = str2 + '"""' + str(k) + '""",'
        str2 = str2[:-1] + ']'

        df1 = pd.DataFrame({"ID": [str1], "Syn": [str2],"CrossReference":['0']})
        df = df.append(df1)


    df.to_csv("merged190821_"+str(threshold)+".csv",index=False)
    df2.to_csv("merged190821_"+str(threshold)+"_xref.csv",index=False)
    #OriginalFile = pd.read_excel(filename, None)
    #pdWriter = pd.ExcelWriter("merged(IDfixed)_"+str(threshold)+".xlsx")
    #OriginalFile['DO'].to_excel(pdWriter, sheet_name="DO", index=False)
    #OriginalFile['ICD10CM'].to_excel(pdWriter, sheet_name="ICD10CM", index=False)
    #OriginalFile['ICD10'].to_excel(pdWriter, sheet_name="ICD10", index=False)
    #OriginalFile['MeSH'].to_excel(pdWriter, sheet_name="MeSH", index=False)
    #df.to_excel(pdWriter, sheet_name="merged", index=False)
    #df2.to_excel(pdWriter,sheet_name="xref",index=False)
    #pdWriter.save()
    #pdWriter.close()

start=time.perf_counter()
contrast(10)
dur1=time.perf_counter()
print("time:",dur1-start)
contrast(9)
dur2=time.perf_counter()
print("time:",dur2-dur1)
contrast(8)
dur3=time.perf_counter()
print("time:",dur3-dur2)
contrast(7)
dur4=time.perf_counter()
print("time:",dur4-dur3)
contrast(6)
dur5=time.perf_counter()
print("time:",dur5-dur4)
contrast(5)
dur6=time.perf_counter()
print("time:",dur6-dur5)
contrast(3)
dur7=time.perf_counter()
print("time:",dur7-dur6)
contrast(0)
dur8=time.perf_counter()
print("time:",dur1-start,'\n',
      dur2-dur1,'\n',
      dur3-dur2,'\n',
      dur4-dur3,'\n',
      dur5-dur4,'\n',
      dur6-dur5,'\n',
      dur7-dur6,'\n',
      dur8-dur7)