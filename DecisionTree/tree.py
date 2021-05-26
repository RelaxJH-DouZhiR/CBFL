'''
Author: your name
Date: 2021-05-25 18:47:20
LastEditTime: 2021-05-26 09:43:34
Description: 决策🌲
'''
# from numpy import result_type
import pandas as pd
from sklearn.model_selection import train_test_split  # 分割验证集和训练集
from sklearn import tree
import graphviz
from sklearn.tree import DecisionTreeClassifier  # 决策树
CSV_PATH = "/Users/lvlaxjh/code/CBFL/AST/data.csv"  # csv路径
data = pd.read_csv(CSV_PATH)  # 读取csv
x = data.iloc[:, [4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]]  # 取训练数据
y = data['accuracy']  # 取样本类标签
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.1)  # 数据集划分，生成训练集和测试集

decTreeClass = DecisionTreeClassifier()  # 实例话决策树
decTreeClass = decTreeClass.fit(x_train, y_train)  # 输入训练集
result = decTreeClass.score(x_test, y_test)  # 测试集
print('score : ' + str(result))
print(decTreeClass.predict(x_test))
# 绘图-start
# iris = load_iris()
dot_data = tree.export_graphviz(
    decTreeClass, out_file=None, feature_names=["codeLine", 'varTotal', 'optTotal', 'array', 'bracketDepth', 'bracketTotal', 'keywordTotal', 'methodTotal', 'typeTotal', 'logic', 'lengthEle', 'lengthWord', 'depth'], class_names=['T', 'F'], filled=True, rounded=True, special_characters=True)
graph = graphviz.Source(dot_data)
graph.render("decTreeClass")
# 绘图-end
