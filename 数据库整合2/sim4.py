#先按id匹配，后以固定阈值的SimhashIndex方法查找
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
a=np.array([1,2])
a=pd.DataFrame(a)
a.columns=['AA']
a.to_csv('test.csv',index=False)

filename = "base2.xlsx"
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
    df=pd.DataFrame({"ID":[],"Syn":[]})
    df2=pd.DataFrame({"ID":[],"Syn":[]})
    #a,adoc_set,aid,sheet_name,from
    dict={}         #ID：同义词表
    xref=[]         #id匹配
    IDPairList=[]   #两两匹配的ID
    unMerged=[]     #未匹配的ID
    flags=[0 for i in range(len(DO))]   #1已配对 0未配对
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
                        # print(id1, id2)
                        # print(DO[i][3],DO[j][3])
                        idMatch = 1
                        idMatched = 1
                        break
            # distance_simhash=Simhash(DO[i][0]).distance(Simhash(DO[j][0]))
            if idMatch == 1:
                idMatch = 0
                # flags[i]=1
                # flags[j]=1
                # print(i,j)
                str1 = '['
                for k in DO[i][1]:  # DO[i][1]=syn
                    str1 = str1 + '"""' + str(k) + '""",'
                str1 = str1[:-1] + ']'
                str2 = '['
                for k in DO[j][1]:
                    str2 = str2 + '"""' + str(k) + '""",'
                str2 = str2[:-1] + ']'
                # print(str1,str2)
                dict[str(DO[i][2])] = str1  # DO[i][2]=id
                dict[str(DO[j][2])] = str2
                IDPair = [str(DO[i][2]), str(DO[j][2])]
                # IDPairList.append(IDPair)
                IDPairList.append(IDPair)
                xref.append(IDPair)
                # df1=pd.DataFrame({"ID":[ID],"Syn":[Syn]})
                # df=df.append(df1)
        if flags[i]==0:
            near=SimIndex.get_near_dups(Simhash(DO[i][0]))
            if len(near)==1 and near[0]==str(i) and idMatched==0:    #未匹配
                str1= '['
                for k in DO[i][1]:
                    str1 = str1 + '"""' + str(k) + '""",'
                str1 = str1[:-1] + ']'
                dict[str(DO[i][2])]=str1
                unMerged.append(str(DO[i][2]))
            #elif len(near)>1 and idMatched==0:
            elif len(near)>1:
                IDPair=[]
                if len(near)>1:
                    while len(near)>0:
                        temp=int(near.pop())
                        str1 = '['
                        for k in DO[temp][1]:
                            str1 = str1 + '"""' + str(k) + '""",'
                        str1 = str1[:-1] + ']'
                        dict[str(DO[temp][2])]=str1
                        flags[temp]=1
                        IDPair.append(str(DO[temp][2]))
                    IDPairList.append(IDPair)



    #二次查找实体对
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
        IDPairList=diseases


    '''diseases=[] #疾病类列表
    for i in range(len(IDPairList)):
        #print(i)
        if flags[i]==0:
            temp=[]
            for ii in IDPairList[i]:
                temp.append(str(ii))
            diseases.append(temp)
            flags[i]=1
            for j in range(i + 1, len(IDPairList)):
                if flags[j] == 0:
                    for k in IDPairList[j]:
                        if k in diseases[-1]:
                            flags[j]=1
                            for l in IDPairList[j]:
                                diseases[-1].append(str(l))
                            break
        else:
            continue'''
    for i in xrefs:
        IDs=list(set(i))
        str1= ','.join(IDs)
        str1=str(len(IDs))+','+'xref'+','+str1 #id数：所有id
        SynList = []
        for id in IDs:
            SynList.append(dict[id])

        str2 = ','.join(SynList)
        #print(str2)
        df1 = pd.DataFrame({"ID": [str1], "Syn": [str2]})
        df2 = df2.append(df1)

    for i in diseases:
        IDs = list(set(i))
        '''if len(IDs)==1:
            continue'''
        str1 = ','.join(IDs)
        str1=str(len(IDs))+','+str1 #id数：所有id
        SynList = []
        for id in IDs:
            SynList.append(dict[id])

        str2 = ','.join(SynList)
        #print(str2)
        df1 = pd.DataFrame({"ID": [str1], "Syn": [str2]})
        df = df.append(df1)
    for i in unMerged:
        str1=i
        str2=dict[i]
        df1 = pd.DataFrame({"ID": [str1], "Syn": [str2]})
        df = df.append(df1)


    df.to_csv("12merged(IDfixed)_"+str(threshold)+".csv",index=False)
    df2.to_csv("12xref_" + str(threshold) + ".csv", index=False)
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

'''start=time.perf_counter()
contrast(0)
dur1=time.perf_counter()
print("time:",dur1-start)
contrast(3)
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
print("time:",dur6-dur5)'''
#contrast(9)
#dur7=time.perf_counter()
#print("time:",dur7-dur6)
contrast(1)
#dur8=time.perf_counter()
'''print("time:",dur1-start,'\n',
      dur2-dur1,'\n',
      dur3-dur2,'\n',
      dur4-dur3,'\n',
      dur5-dur4,'\n',
      dur6-dur5,'\n',
      dur7-dur6,'\n',
      dur8-dur7)'''