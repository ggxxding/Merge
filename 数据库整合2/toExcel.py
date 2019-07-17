import pandas as pd
import numpy as np

#DO
def DOtoEXCEL(path):
    df = pd.read_csv(path, dtype='str')  # use_cols=[] low_memory
    df = df.fillna('')
    print(df.columns)
    df['id'] = 'DOID:' + df['dms_id']
    id = df['id'].values.reshape(-1, 1)

    df['ids'] = ('["' + df['dms_ids.0.db'] + ':' + df['dms_ids.0.id'] + '","' + df['dms_ids.1.db'] + ':' + df['dms_ids.1.id'] +\
                 '","'+ df['dms_ids.2.db'] + ':' + df['dms_ids.2.id'] + '","'+ df['dms_ids.3.db'] + ':' + df['dms_ids.3.id'] +\
                 '","'+ df['dms_ids.4.db'] + ':' + df['dms_ids.4.id'] + '","'+ df['dms_ids.5.db'] + ':' + df['dms_ids.5.id'] +\
                 '","'+ df['dms_ids.6.db'] + ':' + df['dms_ids.6.id'] + '","'+ df['dms_ids.7.db'] + ':' + df['dms_ids.7.id'] +\
                 '","'+ df['dms_ids_extend.0.db'] + ':' + df['dms_ids_extend.0.id'] +\
                 '","'+ df['dms_ids_extend.1.db'] + ':' + df['dms_ids_extend.1.id'] +\
                 '","'+ df['dms_ids_extend.2.db'] + ':' + df['dms_ids_extend.2.id'] +\
                 '","'+ df['dms_ids_extend.3.db'] + ':' + df['dms_ids_extend.3.id'] +\
                 '","'+ df['dms_ids_extend.4.db'] + ':' + df['dms_ids_extend.4.id'] +\
                 '","'+ df['dms_ids_extend.5.db'] + ':' + df['dms_ids_extend.5.id'] +\
                 '","'+ df['dms_ids_extend.6.db'] + ':' + df['dms_ids_extend.6.id'] +\
                 '","'+ df['dms_ids_extend.7.db'] + ':' + df['dms_ids_extend.7.id'] +'"]')
    ids = df['ids'].values
    for index, i in enumerate(ids):
        templist = eval(i)
        templist = list(set(templist))
        if ':' in templist:
            templist.remove(':')
        tempchar = '["""'
        for j in templist:
            tempchar = tempchar + j + '""","""'
        tempchar = tempchar[:-4] + ']'
        ids[index] = tempchar
    ids = ids.reshape(-1, 1)

    df['name'] = df['dms_name']
    name = df['name'].values.reshape(-1, 1)

    df['syn']= '["' + df['dms_synonym.0'] + '","' + df['dms_synonym.1'] + '","' + df['dms_synonym.2']+ \
                '","' + df['dms_synonym.3']+ '","' + df['dms_synonym.4']+'","'+ df['dms_synonym_extend.0']+\
               '","'+df['dms_synonym_extend.1']+'","'+df['dms_synonym_extend.2']+ '","' + df['dms_synonym_extend.3']+\
               '","' + df['dms_synonym_extend.4']+'"]'
    syn = df['syn'].values
    for index, i in enumerate(syn):
        templist = eval(i)
        templist = list(set(templist))
        if '' in templist:
            templist.remove('')
        tempchar = '["""'
        for j in templist:
            tempchar = tempchar + j + '""","""'
        tempchar = tempchar[:-4] + ']'
        syn[index] = tempchar
    syn = syn.reshape(-1, 1)

    sum = np.concatenate((id, ids, name, syn), axis=1)
    df = pd.DataFrame(sum)
    df.columns = ['id', 'ids', 'name', 'syn']
    df.to_excel('DO.xlsx', index=False)
    return df

#ICD10
def ICD1toEXCEL(path):
    df = pd.read_csv(path, dtype='str')  # use_cols=[] low_memory
    df = df.fillna('')
    print(df.columns)
    df['id'] = 'ICD10_CM:'+df['dms_id']
    id=df['id'].values.reshape(-1,1)

    df['ids'] = ('["' + df['dms_ids.0.db']+':'+df['dms_ids.0.id'] + '","' + df['dms_ids_extend.0.db'] + ':' + df['dms_ids_extend.0.id']+\
           '","' + df['dms_ids_extend.1.db'] + ':' + df['dms_ids_extend.1.id']+\
        '","' + df['dms_ids_extend.2.db'] + ':' + df['dms_ids_extend.2.db'] + '"]')
    ids=df['ids'].values
    for index,i in enumerate(ids):
        templist=eval(i)
        templist=list(set(templist))
        if ':' in templist:
            templist.remove(':')
        tempchar='["""'
        for j in templist:
            tempchar=tempchar+j+'""","""'
        tempchar=tempchar[:-4]+']'
        ids[index] = tempchar

    ids = ids.reshape(-1, 1)

    df['name'] = df['dms_name']
    name=df['name'].values.reshape(-1,1)
    #print(name)

    df['syn']= '["""' + df['dms_synonym.0'] + '""","""' + df['dms_synonym.1'] + '""","""' + df['dms_synonym.2']+\
          df['dms_synonym_extend.0']+'""","""'+df['dms_synonym_extend.1']+'""","""'+df['dms_synonym_extend.2']+'"""]'
    #print(df['syn'])
    syn=df['syn'].values
    for index,i in enumerate(syn):
        templist=eval(i)
        templist=list(set(templist))
        if '' in templist:
            templist.remove('')
        tempchar='["""'
        for j in templist:
            tempchar = tempchar + j + '""","""'
        tempchar = tempchar[:-4] + ']'
        syn[index]=tempchar
    syn=syn.reshape(-1,1)

    sum=np.concatenate((id,ids,name,syn),axis=1)
    df=pd.DataFrame(sum)
    df.columns=['id','ids','name','syn']
    df.to_excel('ICD10CM.xlsx',index=False)
    return df

def ICD2toEXCEL(path):
    df = pd.read_csv(path, dtype='str')  # use_cols=[] low_memory
    df = df.fillna('')
    print(df.columns)
    df['id'] = 'ICD10:'+df['dms_id']
    id=df['id'].values.reshape(-1,1)

    df['ids'] = ('["' + df['dms_ids.0.db']+':'+df['dms_ids.0.id'] + '","' +\
                 df['dms_ids_extend.0.db'] + ':' + df['dms_ids_extend.0.id']+ '"]')
    ids=df['ids'].values
    for index,i in enumerate(ids):
        templist=eval(i)
        templist=list(set(templist))
        if ':' in templist:
            templist.remove(':')
        tempchar='["""'
        for j in templist:
            tempchar=tempchar+j+'""","""'
        tempchar=tempchar[:-4]+']'
        ids[index] = tempchar
    ids = ids.reshape(-1, 1)

    df['name'] = df['dms_name']
    name=df['name'].values.reshape(-1,1)
    #print(name)

    df['syn']= "['''" + df['dms_synonym.0'] + "''','''" + df['dms_synonym.1'] + "''','''"+ df['dms_synonym.2']+\
          "''','''" + df['dms_synonym.3']+"''','''" + df['dms_synonym.4']+"''','''"+ df['dms_synonym.5']+\
        "''','''"+df['dms_synonym_extend.0']+"''','''"+df['dms_synonym_extend.1']+"''','''"+df['dms_synonym_extend.2']+\
               "''','''" + df['dms_synonym_extend.3']+"''','''" + df['dms_synonym_extend.4']+"''','''" +\
               df['dms_synonym_extend.5']+"''']"
    #print(df['syn'])
    syn=df['syn'].values
    for index,i in enumerate(syn):
        templist=eval(i)
        templist=list(set(templist))
        if '' in templist:
            templist.remove('')
        tempchar="['''"
        for j in templist:
            tempchar = tempchar + j +"''','''"
        tempchar = tempchar[:-4] + ']'
        syn[index]=tempchar
    syn=syn.reshape(-1,1)

    sum=np.concatenate((id,ids,name,syn),axis=1)
    df=pd.DataFrame(sum)
    df.columns=['id','ids','name','syn']
    df.to_excel('ICD10.xlsx',index=False)
    return df

def MeSHtoEXCEL(path):
    df = pd.read_csv(path, dtype='str')  # use_cols=[] low_memory
    df = df.fillna('')
    print(df.columns)
    df['id'] = 'MeSH:'+df['dms_id']
    id=df['id'].values.reshape(-1,1)

    df['ids'] = ('["""' + df['dms_ids.0.db']+':'+df['dms_ids.0.id'] + '""","""' +\
                 df['dms_ids_extend.0.db'] + ':' + df['dms_ids_extend.0.id']+ '"""]')
    ids=df['ids'].values
    for index,i in enumerate(ids):
        templist=eval(i)
        templist=list(set(templist))
        if ':' in templist:
            templist.remove(':')
        tempchar='["""'
        for j in templist:
            tempchar=tempchar+j+'""","""'
        tempchar=tempchar[:-4]+']'
        ids[index] = tempchar
    ids = ids.reshape(-1, 1)

    df['name'] = df['dms_name']
    name=df['name'].values.reshape(-1,1)
    #print(name)

    df['syn']= '["""' + df['dms_synonym.0'] + '""","""' + df['dms_synonym.1'] + '""","""'+ df['dms_synonym.2']+\
          '""","""' + df['dms_synonym.3']+'""","""' + df['dms_synonym.4']+'""","""'+ df['dms_synonym.5']+ \
               '""","""' + df['dms_synonym.6'] + '""","""' + df['dms_synonym.7'] + '""","""' + df['dms_synonym.8'] + \
               '""","""' + df['dms_synonym.9'] + '""","""' + df['dms_synonym.10'] + '""","""'+ df['dms_synonym.11'] + \
               '""","""' + df['dms_synonym.12'] + '""","""' + df['dms_synonym.13'] + '""","""' + df['dms_synonym.14'] + \
               '""","""' + df['dms_synonym.15']+\
               '""","""'+df['dms_synonym_extend.0']+'""","""'+df['dms_synonym_extend.1']+'""","""'+df['dms_synonym_extend.2']+ \
               '""","""'+ df['dms_synonym_extend.3'] + '""","""' + df['dms_synonym_extend.4'] + \
               '""","""' + df['dms_synonym_extend.5'] + '""","""' + df['dms_synonym_extend.6']+ \
               '""","""'+ df['dms_synonym_extend.7'] +'""","""'+ df['dms_synonym_extend.8'] + \
               '""","""'+ df['dms_synonym_extend.9'] + '""","""'+ df['dms_synonym_extend.10'] + \
               '""","""' + df['dms_synonym_extend.11'] + '""","""' + df['dms_synonym_extend.12'] + \
               '""","""' + df['dms_synonym_extend.13'] + '""","""' + df['dms_synonym_extend.14'] + \
               '""","""'+ df['dms_synonym_extend.15'] +'"""]'
    #print(df['syn'])
    syn=df['syn'].values
    for index,i in enumerate(syn):
        templist=eval(i)
        templist=list(set(templist))
        if '' in templist:
            templist.remove('')
        tempchar='["""'
        for j in templist:
            tempchar = tempchar + j + '""","""'
        tempchar = tempchar[:-4] + ']'
        syn[index]=tempchar
    syn=syn.reshape(-1,1)

    sum=np.concatenate((id,ids,name,syn),axis=1)
    df=pd.DataFrame(sum)
    df.columns=['id','ids','name','syn']
    df.to_excel('MeSH.xlsx',index=False)
    return df
def filesToExcel():
    pathDO = "DiseaseOntology_20190627.csv"
    pathICD1 = "ICD10CM2019_20180626-USA.csv"
    pathICD2 = "ICD102016_20180704-WHO.csv"
    pathMeSH = "MeSH2018_20180713.csv"
    a = DOtoEXCEL(pathDO)
    b = ICD1toEXCEL(pathICD1)
    c = ICD2toEXCEL(pathICD2)
    d = MeSHtoEXCEL(pathMeSH)

    pdWriter = pd.ExcelWriter("base.xlsx")
    a.to_excel(pdWriter, sheet_name="DO", index=False)
    b.to_excel(pdWriter, sheet_name="ICD10CM", index=False)
    c.to_excel(pdWriter, sheet_name="ICD10", index=False)
    d.to_excel(pdWriter, sheet_name="MeSH", index=False)
    pdWriter.save()
    pdWriter.close()