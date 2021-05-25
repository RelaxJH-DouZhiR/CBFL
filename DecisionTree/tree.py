'''
Author: your name
Date: 2021-05-25 18:47:20
LastEditTime: 2021-05-25 19:45:24
Description: file content
'''
from numpy import result_type
import pandas as pd
from sklearn.model_selection import train_test_split  # 分割验证集和训练集
from sklearn import tree
import graphviz 
from sklearn.tree import DecisionTreeClassifier  # 决策树
CSV_PATH = "/Users/lvlaxjh/code/CBFL/AST/testdata.csv"
data = pd.read_csv(CSV_PATH)
x = data.iloc[:, [4,6,7,8,9,10,11,12,13,14,15,16,17]]
y = data['accuracy']

# x = data.iloc[:, data.columns != 'dataset' and data.columns !=
                #   'project' and data.columns != 'pPath' and data.columns != 'pId' and data.columns != 'codeLine' and data.columns != 'suspicious']
# print(y.head(5))
x_train,x_test,y_train,y_test  = train_test_split(x,y,test_size = 0.4)
# print(x_train)

decTreeClass = DecisionTreeClassifier()
decTreeClass = decTreeClass.fit(x_train,y_train)
result = decTreeClass.score(x_test,y_test)
# print(result)
# tree.plot_tree(decTreeClass)
dot_data = tree.export_graphviz(decTreeClass, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("iris")
