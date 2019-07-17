from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
from simhash import Simhash
import re
import xlrd
import os
from xlutils.copy import copy
import pandas as pd

#OriginalFile = pd.read_excel("test1.xls", None)
#print(type(OriginalFile['merged']['Syn'][1]))

filename = "digestive_system.xls"
workbook = xlrd.open_workbook(filename)
def get_simhash_topics(sheet_name):
    sheet = workbook.sheet_by_name(sheet_name)
    cols = sheet.col_values(2)
    #print(cols)
    cols_name = sheet.col_values(1)
    cols_id = sheet.col_values(0)
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
        #print(id)
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
        simhash_topics.append((doc_tokens, doc_set, id, sheet_name))
        #提取词干后的同义词表，同义词表，ID，来自哪个库
    return simhash_topics

DO = get_simhash_topics("DOID")
#print(len(DO))
Mesh = get_simhash_topics("Mesh")
#print(len(Mesh))
ICD = get_simhash_topics("ICD")
#print(len(ICD))
DO.extend(Mesh)
DO.extend(ICD)
print(DO)
def contrast(threshold):
    df=pd.DataFrame({"ID":[],"Syn":[]})
    #a,adoc_set,aid,sheet_name,from

    dict={}     #ID：同义词表
    IDPairList=[]   #两两匹配的ID
    unMerged=[] #未匹配的ID
    flags=[0 for i in range(len(DO))]
    for i in range(len(DO)):
        for j in range(i+1,len(DO)):
            distance_simhash=Simhash(DO[i][0]).distance(Simhash(DO[j][0]))
            if distance_simhash<threshold+1:
                flags[i]=1
                flags[j]=1
                print(i,j)
                str1='['
                for k in DO[i][1]:
                    str1=str1+"'"+str(k)+"',"
                str1=str1[:-1]+']'
                str2 = '['
                for k in DO[j][1]:
                    str2 = str2 + "'" + str(k) + "',"
                str2 = str2[:-1] + ']'
                dict[str(DO[i][2])]=str1
                dict[str(DO[j][2])]=str2
                IDPair=[str(DO[i][2]),str(DO[j][2])]
                IDPairList.append(IDPair)
                #df1=pd.DataFrame({"ID":[ID],"Syn":[Syn]})
                #df=df.append(df1)
    for index,i in enumerate(flags):
        if i==0:
            str1 = '['
            for k in DO[index][1]:
                str1 = str1 + "'" + str(k) + "',"
            str1 = str1[:-1] + ']'

            dict[str(DO[index][2])]=str1
            unMerged.append(str(DO[index][2]))


    flags=[0 for i in range(len(IDPairList))]
    diseases=[] #疾病类列表
    for i in range(len(IDPairList)):
        if flags[i]==0:
            diseases.append([str(IDPairList[i][0]),str(IDPairList[i][1])])
            flags[i]=1
            for j in range(i + 1, len(IDPairList)):
                if flags[j] == 0:
                    if (IDPairList[j][0] in diseases[-1]):
                        flags[j] = 1
                        diseases[-1].append(str(IDPairList[j][1]))
                    if (IDPairList[j][1] in diseases[-1]):
                        flags[j] = 1
                        diseases[-1].append(str(IDPairList[j][0]))
        else:
            continue
    for i in diseases:
        IDs = list(set(i))
        if len(IDs)==1:
            continue
        str1 = ','.join(IDs)
        str1=str(len(IDs))+':'+str1
        SynList = []
        for id in IDs:
            SynList.append(dict[id])

        str2 = ','.join(SynList)
        print(str2)
        df1 = pd.DataFrame({"ID": [str1], "Syn": [str2]})
        df = df.append(df1)
    for i in unMerged:
        str1=i
        str2=dict[i]
        df1 = pd.DataFrame({"ID": [str1], "Syn": [str2]})
        df = df.append(df1)



    '''for index1,i in enumerate(Mesh):
        for index2,j in enumerate(DO):
            distance_simhash= Simhash(i[0]).distance(Simhash(j[0]))
            if distance_simhash < threshold:
                pd1 = pd.DataFrame({"aID": [i[3]], "aName": [i[1]],"aSyn":[i[2]],"bID": [j[3]], "bName": [j[1]],"bSyn":[j[2]],"distance": [distance_simhash]})
                row = str(i[3]) + ";" + 'Mesh-sim: ' + str(i[1]) + ';  ' + str(j[3]) + ";" + 'DO-sim: ' + str(j[1]) + " " + 'distance_simhash：' + str(distance_simhash)
                print(row)
                df=df.append(pd1)'''

    #df.to_csv('sim'+str(threshold)+'.csv',index=False)
    OriginalFile = pd.read_excel("digestive_system.xls", None)
    pdWriter = pd.ExcelWriter("test"+str(threshold)+".xlsx")
    OriginalFile['ICD'].to_excel(pdWriter, sheet_name="ICD", index=False)
    OriginalFile['DOID'].to_excel(pdWriter, sheet_name="DOID", index=False)
    OriginalFile['Mesh'].to_excel(pdWriter, sheet_name="Mesh", index=False)
    df.to_excel(pdWriter, sheet_name="merged", index=False)
    pdWriter.save()
    pdWriter.close()

te.filesToExcel()

contrast(0)
contrast(3)
contrast(5)
contrast(8)
contrast(10)
contrast(11)
contrast(12)
