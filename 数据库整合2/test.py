import numpy as np
import pandas as pd
b=[1,2,3]
for i in range(len(b)):
    print(i)
a=['abc']
a=','.join(a)
print(a)

df=pd.read_excel('Merged10.xlsx',sheet_name='merged')
dfDO=pd.read_excel('Merged10.xlsx',sheet_name='DO')
dfICD10CM=pd.read_excel('Merged10.xlsx',sheet_name='ICD10CM')
dfICD10=pd.read_excel('Merged10.xlsx',sheet_name='ICD10')
dfMeSH=pd.read_excel('Merged10.xlsx',sheet_name='MeSH')
list1=df['ID'].values
lenDO=len(dfDO)
lenICD10CM=len(dfICD10CM)
lenICD10=len(dfICD10)
lenMeSH=len(dfMeSH)

numlist=[]
unmergedlist=[]
for i in list1:
    j=i.split(':')
    if len(j)!=2:
        numlist.append(int(j[0]))
    else:
        unmergedlist.append(j[0])

print('DO unmerged       %-6d %.2f'%(unmergedlist.count('DOID'),unmergedlist.count('DOID')/lenDO))
print('ICD10_CM unmerged %-6d %.2f'%(unmergedlist.count('ICD10_CM'),unmergedlist.count('ICD10_CM')/lenICD10CM))
print('ICD10 unmerged    %-6d %.2f'%(unmergedlist.count('ICD10'),unmergedlist.count('ICD10')/lenICD10))
print('MeSH unmerged     %-6d %.2f'%(unmergedlist.count('MeSH'),unmergedlist.count('MeSH')/lenMeSH))

numset=list(set(numlist))
countlist=[]
sum=0
for i in numset:
    countlist.append(numlist.count(i))
    sum+=numlist.count(i)

print('max size: %d'%(max(numset)))

index=countlist.index(max(countlist))
print(numset[index],countlist[index]/sum)
numset.pop(index)
countlist.pop(index)

index=countlist.index(max(countlist))
print(numset[index],countlist[index]/sum)
numset.pop(index)
countlist.pop(index)

index=countlist.index(max(countlist))
print(numset[index],countlist[index]/sum)
numset.pop(index)
countlist.pop(index)

index=countlist.index(max(countlist))
print(numset[index],countlist[index]/sum)
numset.pop(index)
countlist.pop(index)

index=countlist.index(max(countlist))
print(numset[index],countlist[index]/sum)
numset.pop(index)
countlist.pop(index)