'''
Author: your name
Date: 2021-05-25 18:47:20
LastEditTime: 2021-06-03 21:12:46
Description: 决策🌲
████████╗██████╗ ███████╗███████╗
╚══██╔══╝██╔══██╗██╔════╝██╔════╝
   ██║   ██████╔╝█████╗  █████╗
   ██║   ██╔══██╗██╔══╝  ██╔══╝
   ██║   ██║  ██║███████╗███████╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝
'''
# from numpy import result_type
import pandas as pd
from sklearn.model_selection import train_test_split  # 分割验证集和训练集
from sklearn import tree  # 树
from sklearn.model_selection import KFold  # k折交叉验证
import graphviz  # 绘图
from sklearn.tree import DecisionTreeClassifier  # 决策树
from collections import Counter
from imblearn.over_sampling import SMOTE
from joblib import dump, load
import csv

# GLOBAL_VAR = {
#     'TRAIN_CSV_PATH': "/Users/lvlaxjh/code/CBFL/data/lang/lang_data_train.csv",  # 训练集csv路径
#     'TEST_CSV_PATH': "/Users/lvlaxjh/code/CBFL/data/lang/lang_data_test.csv",  # 测试集csv路径
#     'MODEL_SAVE_PATH': 'DecisionTree/res/',  # 模型保存路径
#     'TREE_PDF_SAVE_PATH': 'DecisionTree/res/',  # 绘图保存路径
#     'MODEL_PATH': '/Users/lvlaxjh/code/CBFL/DecisionTree/res/tree.joblib',  # 模型路径
# }


def draw_tree(treeModel, feature_names, class_names, savePath):
    dot_data = tree.export_graphviz(
        treeModel, out_file=None, feature_names=feature_names, class_names=class_names, filled=True, rounded=True, special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render(savePath)


def tree(project, id):  # 训练决策树
    TEST_PATH = '/Users/lvlaxjh/code/CBFL/data/%s/csv/traintest/%s-test-%s.csv' % (
        project, project, id)  # 测试集路径
    TRAIN_PATH = '/Users/lvlaxjh/code/CBFL/data/%s/csv/traintest/%s-train-%s.csv' % (
        project, project, id)  # 训练集路径
    # 测试集-start
    test_data = pd.read_csv(TEST_PATH)
    test_x = test_data.iloc[:, [6, 7, 8, 9,
                                10, 11, 12, 13, 14, 15, 17]]  # 取测试数据
    test_y = test_data['accuracy']  # 取样本类标签
    # 测试集-end
    # 训练集-start
    train_data = pd.read_csv(TRAIN_PATH)
    train_x = train_data.iloc[:, [6, 7, 8, 9,
                                  10, 11, 12, 13, 14, 15, 17]]  # 取训练数据
    train_y = train_data['accuracy']  # 取样本类标签
    # 训练集-end
    smo = SMOTE(random_state=1)  # MOTE
    x, y = smo.fit_resample(train_x, train_y)  # 平衡训练数据集
    decTreeClass = DecisionTreeClassifier(
        criterion='gini', splitter='best', max_depth=3)  # 决策树模型初始化
    decTreeClass.fit(x, y)  # 拟合模型
    res = decTreeClass.score(test_x, test_y)  # 预测评分
    predictRes = decTreeClass.predict(test_x)  # 预测结果，返回列表
    # predictResList = decTreeClass.predict_proba(test_x)  # 预测结果，返回概率
    predictRes = list(predictRes)  # numpy.array 类型转 list
    return predictRes  # list


def write_res_in_csv(project, version, resList):  # 用于将预测结果写入数据集
    CSV_PATH = f'/Users/lvlaxjh/code/CBFL/data/{project}/csv/traintest/{project}-test-{str(version)}.csv'
    csvLine = 0  # csv行
    csvHead = []#存储csv文件头
    saveResList = []#存储所有文件
    with open(CSV_PATH) as f:
        csvFile = csv.reader(f)
        for row in csvFile:
            if csvLine == 0:
                csvHead = row
            else:
                row.append(resList[csvLine-1])
                saveResList.append(row)
            csvLine+=1
    csvFile = open(CSV_PATH, 'w', encoding="utf-8", newline="")
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(csvHead)
    for i in saveResList:
        csvWriter.writerow(i)
    csvFile.close()


if __name__ == "__main__":
    project = 'chart'
    for i in range(8):
        res = tree(project, i)
        write_res_in_csv(project, i, res)
    # get_best_tree()
    # predictRes, predictResList = predict_model()
    # resList = []
    # TEM_num = 1
    # predictResList = list(predictResList)
    # for i in predictResList:
    #     resList.append({
    #         'id': TEM_num,
    #         '0': float(list(i)[0]),
    #         '1': float(list(i)[1]),
    #     })
    #     TEM_num+=1
    # resList.sort(key= lambda x:x['1'],reverse=True)
    # for i in resList:
    #     print(i)
