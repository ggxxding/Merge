#
import pandas as pd
import numpy as np
data = pd.read_excel('test.xls',None)
#Mesh DOID ICD
for i in range(6):
    print(np.array(data['merged'])[0][i])
print('===============')
array=np.array(data['merged'])

dict={}
for i in range(array.shape[0]):
    dict[str(array[i][0])]=str(array[i][2])
    dict[str(array[i][3])]=str(array[i][5])
print(dict)

data2=pd.DataFrame({"aID":[],"aName":[],"aSyn":[],
                    "bID":[],"bName":[],"bSyn":[],
                    "cID":[],"cName":[],"cSyn":[]})
data3=pd.DataFrame({"aID":[],"aName":[],"aSyn":[],
                    "bID":[],"bName":[],"bSyn":[],
                    "cID":[],"cName":[],"cSyn":[]})
data4=pd.DataFrame({"ID":[],"Syn":[]})
diseases=[]
flags=[0 for i in range(array.shape[0])]
for i in range(array.shape[0]):
    #print(array[i][0],array[i][3])
    #flag=0
    if flags[i]==0:
        diseases.append([str(array[i][0]),str(array[i][3])])
    else:
        continue
    for j in range(i+1,array.shape[0]):
        if flags[j]==0:
            if(array[j][0] in diseases[-1]):
                flags[j]=1
                diseases[-1].append(array[j][3])
            if(array[j][3] in diseases[-1]):
                flags[j]=1
                diseases[-1].append(array[j][0])
print(len(diseases))
for i in diseases:
    IDList=list(set(i))
    str1=','.join(IDList)
    SynList=[]
    for id in IDList:
        SynList.append(dict[id])

    str2=','.join(SynList)
    print(str2)
    str3=pd.DataFrame({"ID":[str1],"Syn":[str2]})
    data4=data4.append(str3)

print(data4)






data4.to_csv('testsets.csv')
OriginalFile = pd.read_excel("digestive_system.xls", None)
pdWriter = pd.ExcelWriter("merged.xls")
OriginalFile['ICD'].to_excel(pdWriter, sheet_name="ICD", index=False)
OriginalFile['DOID'].to_excel(pdWriter, sheet_name="DOID", index=False)
OriginalFile['Mesh'].to_excel(pdWriter, sheet_name="Mesh", index=False)
data4.to_excel(pdWriter, sheet_name="merged", index=False)
pdWriter.close()
