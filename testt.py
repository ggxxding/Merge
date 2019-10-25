import pandas as pd
#import numpy as np
a=pd.read_csv('relationships.tsv',sep='\t')
b=a['Evidence'].values
c=b.tolist()
print(set(c))