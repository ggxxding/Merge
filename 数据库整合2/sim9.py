import toExcel
toExcel.filesToExcel(nameDO="DiseaseOntology_20190627.csv",nameICDCM="ICD10CM2019_20180626-USA.csv",
nameICD= "ICD102016_20180704-WHO.csv",nameMeSH= "MeSH2018_20180713.csv")


import sim7
import time
import sim6_csv

start=time.perf_counter()
dur=[]
for i in [0,3,5,6,7,8,9,10]:
    sim7.contrast(i)
    dur.append(time.perf_counter())

print("time:",dur[0]-start,'\n',
      dur[1]-dur[0],'\n',
      dur[2]-dur[1],'\n',
      dur[3]-dur[2],'\n',
      dur[4]-dur[3],'\n',
      dur[5]-dur[4],'\n',
      dur[6]-dur[5],'\n',
      dur[7]-dur[6])

for i in [0,3,5,6,7,8,9,10]:
    print(i)
    sim6_csv.idProcess('merged190821_'+str(i)+'.csv')

for iii in [0,3,5,6,7,8,9,10]:
    print(iii)
    sim8.idProcess('merged190821_'+str(iii)+'_ID.csv')