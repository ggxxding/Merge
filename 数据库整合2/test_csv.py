import numpy as np
import pandas as pd



filename='merged190815_0_ID_LCS.csv'

df=pd.read_csv(filename)
'''dfDO=pd.read_excel(filename,sheet_name='DO')
dfICD10CM=pd.read_excel(filename,sheet_name='ICD10CM')
dfICD10=pd.read_excel(filename,sheet_name='ICD10')
dfMeSH=pd.read_excel(filename,sheet_name='MeSH')
dfxref=pd.read_excel(filename,sheet_name='xref')'''
list1=df['ID'].values
print(list1)
lenMerged=len(df)
#lenDO=len(dfDO)
#lenICD10CM=len(dfICD10CM)
#lenICD10=len(dfICD10)
#lenMeSH=len(dfMeSH)
#lenxref=len(dfxref)

DO_=0
ICD10CM_=0
ICD10_=0
MeSH_=0

DO_ICD10CM=0
DO_ICD10=0
DO_MeSH=0
ICD10CM_ICD10=0
ICD10CM_MeSH=0
ICD10_MeSH=0

noDO=0
noICD10CM=0
noICD10=0
noMeSH=0

allbase=0
numlist=[]
unmergedlist=[]
for i in list1:
    j=i.split(',')
    if len(j)>2:
        numlist.append(int(j[0]))
    else:
        unmergedlist.append(j[1].split(':')[0])

    j = i.split(',')
    bases = []
    while len(j) > 2:
        k = j[-1].split(':')
        j.pop()
        bases.append(k[0])
    if 'DOID' in bases and 'ICD10_CM' in bases and 'ICD10' in bases and 'MeSH' in bases:
        allbase += 1
    elif 'DOID' in bases and 'ICD10_CM' in bases and 'ICD10' in bases:
        noMeSH += 1
    elif 'DOID' in bases and 'ICD10_CM' in bases and 'MeSH' in bases:
        noICD10 += 1
    elif 'DOID' in bases and 'ICD10' in bases and 'MeSH' in bases:
        noICD10CM += 1
    elif 'ICD10_CM' in bases and 'ICD10' in bases and 'MeSH' in bases:
        noDO += 1
    elif 'DOID' in bases and 'ICD10_CM' in bases:
        DO_ICD10CM += 1
    elif 'DOID' in bases and 'ICD10' in bases:
        DO_ICD10 += 1
    elif 'DOID' in bases and 'MeSH' in bases:
        DO_MeSH += 1
    elif 'ICD10_CM' in bases and 'ICD10' in bases:
        ICD10CM_ICD10 += 1
    elif 'ICD10_CM' in bases and 'MeSH' in bases:
        ICD10CM_MeSH += 1
    elif 'ICD10' in bases and 'MeSH' in bases:
        ICD10_MeSH += 1
    elif 'DOID' in bases:
        DO_ += 1
    elif 'ICD10_CM' in bases:
        ICD10CM_ += 1
    elif 'ICD10' in bases:
        ICD10_ += 1
    elif 'MeSH' in bases:
        MeSH_ += 1
#print('xref   %d  %.2f'%(lenxref,lenxref/lenMerged))
#print('DO       unmerged  %-6d %.2f'%(unmergedlist.count('DOID'),unmergedlist.count('DOID')/lenDO))
#print('ICD10_CM unmerged  %-6d %.2f'%(unmergedlist.count('ICD10_CM'),unmergedlist.count('ICD10_CM')/lenICD10CM))
#print('ICD10    unmerged  %-6d %.2f'%(unmergedlist.count('ICD10'),unmergedlist.count('ICD10')/lenICD10))
#print('MeSH     unmerged  %-6d %.2f'%(unmergedlist.count('MeSH'),unmergedlist.count('MeSH')/lenMeSH))
lenMerge=lenMerged-(unmergedlist.count('DOID')+
      unmergedlist.count('ICD10_CM')+
      unmergedlist.count('ICD10')+
      unmergedlist.count('MeSH'))
print('sum: %d merged %d unmerged %d'%(lenMerged,lenMerge,unmergedlist.count('DOID')+
      unmergedlist.count('ICD10_CM')+
      unmergedlist.count('ICD10')+
      unmergedlist.count('MeSH')))
print('DO_',DO_,DO_/lenMerge)
print('ICD10CM_',ICD10CM_,ICD10CM_/lenMerge)
print('ICD10_ ',ICD10_,ICD10_/lenMerge)
print('MeSH_ ',MeSH_,MeSH_/lenMerge)
print('DO_ICD10CM',DO_ICD10CM,DO_ICD10CM/lenMerge)
print('DO_ICD10',DO_ICD10,DO_ICD10/lenMerge)
print('DO_MeSH',DO_MeSH,DO_MeSH/lenMerge)
print('ICD10CM_ICD10 ',ICD10CM_ICD10,ICD10CM_ICD10/lenMerge)
print('ICD10CM_MeSH',ICD10CM_MeSH,ICD10CM_MeSH/lenMerge)
print('ICD10_MeSH ',ICD10_MeSH,ICD10_MeSH/lenMerge)
print('noDO',noDO,noDO/lenMerge)
print('noICD10CM',noICD10CM,noICD10CM/lenMerge)
print('noICD10',noICD10,noICD10/lenMerge)
print('noMeSH',noMeSH,noMeSH/lenMerge)
print('allbase',allbase,allbase/lenMerge)

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

'''
list2=dfxref['ID'].values
DO_=0
ICD10CM_=0
ICD10_=0
MeSH_=0

DO_ICD10CM=0
DO_ICD10=0
DO_MeSH=0
ICD10CM_ICD10=0
ICD10CM_MeSH=0
ICD10_MeSH=0

noDO=0
noICD10CM=0
noICD10=0
noMeSH=0

allbase=0
for i in list2:
    j=i.split(',')
    bases=[]
    while len(j)>2:
        k=j[-1].split(':')
        j.pop()
        bases.append(k[0])
    if 'DOID' in bases and 'ICD10_CM' in bases and 'ICD10' in bases and 'MeSH' in bases:
        allbase+=1
    elif 'DOID' in bases and 'ICD10_CM' in bases and 'ICD10' in bases :
        noMeSH+=1
    elif 'DOID' in bases and 'ICD10_CM' in bases and 'MeSH' in bases:
        noICD10+=1
    elif 'DOID' in bases and 'ICD10' in bases and 'MeSH' in bases:
        noICD10CM+=1
    elif 'ICD10_CM' in bases and 'ICD10' in bases and 'MeSH' in bases:
        noDO+=1
    elif 'DOID' in bases and 'ICD10_CM' in bases :
        DO_ICD10CM+=1
    elif 'DOID' in bases and 'ICD10' in bases:
        DO_ICD10+=1
    elif 'DOID' in bases and 'MeSH' in bases:
        DO_MeSH+=1
    elif 'ICD10_CM' in bases and 'ICD10' in bases :
        ICD10CM_ICD10+=1
    elif 'ICD10_CM' in bases and 'MeSH' in bases:
        ICD10CM_MeSH+=1
    elif 'ICD10' in bases and 'MeSH' in bases:
        ICD10_MeSH+=1
    elif 'DOID' in bases:
        DO_+=1
    elif 'ICD10_CM' in bases:
        ICD10CM_+=1
    elif 'ICD10' in bases:
        ICD10_+=1
    elif 'MeSH' in bases:
        MeSH_+=1

print('DO_',DO_,DO_/lenxref)
print('ICD10CM_',ICD10CM_,ICD10CM_/lenxref)
print('ICD10_ ',ICD10_,ICD10_/lenxref)
print('MeSH_ ',MeSH_,MeSH_/lenxref)
print('DO_ICD10CM',DO_ICD10CM,DO_ICD10CM/lenxref)
print('DO_ICD10',DO_ICD10,DO_ICD10/lenxref)
print('DO_MeSH',DO_MeSH,DO_MeSH/lenxref)
print('ICD10CM_ICD10 ',ICD10CM_ICD10,ICD10CM_ICD10/lenxref)
print('ICD10CM_MeSH',ICD10CM_MeSH,ICD10CM_MeSH/lenxref)
print('ICD10_MeSH ',ICD10_MeSH,ICD10_MeSH/lenxref)
print('noDO',noDO,noDO/lenxref)
print('noICD10CM',noICD10CM,noICD10CM/lenxref)
print('noICD10',noICD10,noICD10/lenxref)
print('noMeSH',noMeSH,noMeSH/lenxref)
print('allbase',allbase,allbase/lenxref)
'''