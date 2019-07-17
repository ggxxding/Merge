from py2neo import Graph,Node,Relationship
import pandas as pd

df=pd.read_csv('C://Users//ggxxding//Documents//train2id.txt',sep='\t',dtype=str,error_bad_lines=False)
#print(len(df['s']))
#df=df.fillna('unknown')
#print(len(df['s']))

new=df['s'].str.strip()
df['s']=new
new=df['p'].str.strip()
df['p']=new
new=df['o'].str.strip()
df['o']=new


##连接neo4j数据库，输入地址、用户名、密码
#graph = Graph('http://localhost:7474',username='neo4j',password='ggxxding2')
graph = Graph('http://localhost:7474',auth=('neo4j','ggxxding2'))
#graph.delete_all()
#graph.begin()
##
for i in range(len(df['s'])):
    '''node1=Node('e',name=df['s'][i])
    graph.merge(node1,'e','name')
    node2=Node('e',name=df['o'][i])o
    graph.merge(node2,'e','name')
    rel=Relationship(node1,df['p'][i],node2)
    graph.merge(rel)'''
    graph.run("MERGE (n1:entity{name:'" + df['s'][i] + "'}) MERGE (n2:entity{name:'" + df['o'][i] + "'}) MERGE (n1)-[r:r"+df['p'][i]+"]->(n2)")


    if i%100==0:
        print(i,'/',len(df['s']))
#以下语句可以输出100个数据库中的三元组，去掉limit可以输出整个数据库，以列表返回，可以用来导出数据库
#print(graph.run('MATCH (n)-[r]->(p) return n,r,p limit 100').data())
#737 13617
#match (na:company)-[re]->(nb:company) where na.id = '12399145' WITH na,re,nb match (nb:company)-[re2]->(nc:company) return na,re,nb,re2,nc
#MATCH (n{name:'737'})-[r]->(o)-[y]-(t{name:'2307'})  return n,o,t
##创建关系
#分别建立了test_node_1指向test_node_2和test_node_2指向test_node_1两条关系，关系的类型为"丈夫、妻子"，两条关系都有属性count，且值为1。
'''node_1_zhangfu_node_1 = Relationship(test_node_1,'t1',test_node_2)
node_1_zhangfu_node_1['count'] = 1
node_2_qizi_node_1 = Relationship(test_node_2,'t2',test_node_1)
node_2_munv_node_1 = Relationship(test_node_2,'t3',test_node_3)

test=Relationship(test_node_1,'rel')
graph.create(test)
node_2_qizi_node_1['count'] = 1

graph.create(node_1_zhangfu_node_1)
graph.create(node_2_qizi_node_1)
graph.create(node_2_munv_node_1)'''

#print(graph)
