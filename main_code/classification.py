'''
Author: your name
Date: 2021-05-25 18:47:20
LastEditTime: 2021-06-08 16:08:31
Description: classification
 ██████╗██╗      █████╗ ███████╗███████╗██╗███████╗██╗ ██████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
██╔════╝██║     ██╔══██╗██╔════╝██╔════╝██║██╔════╝██║██╔════╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
██║     ██║     ███████║███████╗███████╗██║█████╗  ██║██║     ███████║   ██║   ██║██║   ██║██╔██╗ ██║
██║     ██║     ██╔══██║╚════██║╚════██║██║██╔══╝  ██║██║     ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
╚██████╗███████╗██║  ██║███████║███████║██║██║     ██║╚██████╗██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
 ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝     ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
'''
# from numpy import result_type
import pandas as pd
# from sklearn.model_selection import train_test_split  # 分割验证集和训练集
# from sklearn import tree  # 树
# from sklearn.model_selection import KFold  # k折交叉验证
import graphviz  # 绘图
#
from sklearn.tree import DecisionTreeClassifier  # 决策树
from sklearn import naive_bayes  # 贝叶斯
#
# from collections import Counter
from imblearn.over_sampling import SMOTE
from joblib import dump, load
# import numpy as np
import csv


def draw_tree(treeModel, feature_names, class_names, savePath):
    dot_data = tree.export_graphviz(
        treeModel, out_file=None, feature_names=feature_names, class_names=class_names, filled=True, rounded=True, special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render(savePath)

# 决策树-start


def tree(project, id, tree_depth, trainOrModel):  # 训练决策树
    TEST_PATH = '/Users/lvlaxjh/code/CBFL/data/%s/csv/traintest/%s-test-%s.csv' % (
        project, project, id)  # 测试集路径
    TRAIN_PATH = '/Users/lvlaxjh/code/CBFL/data/%s/csv/traintest/%s-train-%s.csv' % (
        project, project, id)  # 训练集路径
    # 模型存储父路径
    joblib_SAVE_PATH = f'/Users/lvlaxjh/code/CBFL/data/{project}/csv/traintest/model/'
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
    # smo = SMOTE(random_state=1,k_neighbors=1)  # MOTE
    smo = SMOTE(random_state=1)  # MOTE
    train_x, train_y = smo.fit_resample(train_x, train_y)  # 平衡训练数据集
    if trainOrModel == 'train':
        decTreeClass = DecisionTreeClassifier(
            criterion='gini', splitter='best', max_depth=tree_depth)  # 决策树模型初始化
    elif trainOrModel == 'model':
        decTreeClass = load(joblib_SAVE_PATH+f'tree{str(id)}.tree')
    decTreeClass.fit(train_x, train_y)  # 拟合模型
    dump(decTreeClass, joblib_SAVE_PATH+f'tree{str(id)}.tree')  # 存储模型
    resScore = decTreeClass.score(test_x, test_y)  # 预测评分
    # predictRes = decTreeClass.predict(test_x)  # 预测结果，返回列表
    predictRes = decTreeClass.predict(test_x)  # 预测结果，返回列表
    # predictResList = decTreeClass.predict_proba(test_x)  # 预测结果，返回概率
    predictRes = list(predictRes)  # numpy.array 类型转 list
    # print(predictRes)
    return predictRes  # list
# 决策树-end


# 贝叶斯-start
def bayes(project, id, trainOrModel):  # 训练决策树
    TEST_PATH = '/Users/lvlaxjh/code/CBFL/data/%s/csv/traintest/%s-test-%s.csv' % (
        project, project, id)  # 测试集路径
    TRAIN_PATH = '/Users/lvlaxjh/code/CBFL/data/%s/csv/traintest/%s-train-%s.csv' % (
        project, project, id)  # 训练集路径
    # 模型存储父路径
    joblib_SAVE_PATH = f'/Users/lvlaxjh/code/CBFL/data/{project}/csv/traintest/model/'
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
    train_x, train_y = smo.fit_resample(train_x, train_y)  # 平衡训练数据集
    if trainOrModel == 'train':
        bayes = naive_bayes.GaussianNB()  # 贝叶斯模型初始化
    elif trainOrModel == 'model':
        bayes = load(joblib_SAVE_PATH+f'bayes{str(id)}.tree')
    bayes.fit(train_x, train_y)  # 拟合模型
    dump(bayes, joblib_SAVE_PATH+f'bayes{str(id)}.tree')  # 存储模型
    resScore = bayes.score(test_x, test_y)  # 预测评分
    predictRes = bayes.predict(test_x)  # 预测结果，返回列表
    # predictResList = decTreeClass.predict_proba(test_x)  # 预测结果，返回概率
    predictRes = list(predictRes)  # numpy.array 类型转 list
    return predictRes  # list
# 贝叶斯-end


# 将预测结果写入数据集 -start
def write_res_in_csv(project, id, resList):
    CSV_PATH = f'/Users/lvlaxjh/code/CBFL/data/{project}/csv/traintest/{project}-test-{str(id)}.csv'
    csvLine = 0  # csv行
    csvHead = []  # 存储csv文件头
    saveResList = []  # 存储所有文件
    with open(CSV_PATH) as f:
        csvFile = csv.reader(f)
        for row in csvFile:
            if csvLine == 0:
                csvHead = row
            else:
                row[20] = resList[csvLine-1]
                saveResList.append(row)
            csvLine += 1
    csvFile = open(CSV_PATH, 'w', encoding="utf-8", newline="")
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(csvHead)
    for i in saveResList:
        csvWriter.writerow(i)
    csvFile.close()
# 将预测结果写入数据集 -end


# 取得真实结果-start
def get_true_results(project, version):
    CSV_PATH = f'/Users/lvlaxjh/code/CBFL/data/{project}/csv/traintest/{project}-test-{str(version)}.csv'
    csvLine = 0  # csv行
    resList = []
    with open(CSV_PATH) as f:
        csvFile = csv.reader(f)
        for row in csvFile:
            if csvLine != 0:
                resList.append(int(row[19]))
            csvLine += 1
    return resList
# 取得真实结果-end


def get_tp_tn_fp_fn(project, id, predictRes, trueRes):
    # TP-start
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    for i in range(len(predictRes)):
        if predictRes[i] == trueRes[i] == 1:
            TP += 1
        if predictRes[i] == trueRes[i] == 0:
            TN += 1
        if predictRes[i] == 1 and trueRes[i] == 0:
            FP += 1
        if predictRes[i] == 0 and trueRes[i] == 1:
            FN += 1
    # precesion = 0
    precesion = TP/(TP+FP)
    recall = TP/(TP+FN)
    # recall = 0
    print(f'{project}{id} TP : {TP} TN : {TN} FP : {FP} FN : {FN} precesion : {precesion} recall : {recall}')
    return TP, TN, FP, FN, precesion, recall
    # TP-end


if __name__ == "__main__":
    k = 10  # 数据集切割的大小，k折交叉验证
    project = 'time'
    tree_depth = 3  # 决策树深
    totalTP = 0
    totalTn = 0
    totalFP = 0
    totalFN = 0
    totalprecesion = 0
    totalrecall = 0
    for i in range(k):  # *
        predictRes = tree(project, i, tree_depth, trainOrModel='train')
        # predictRes = bayes(project, i, trainOrModel='train')
        trueRes = get_true_results(project, i)
        write_res_in_csv(project, i, predictRes)
        TP, TN, FP, FN, precesion, recall = get_tp_tn_fp_fn(
            project, i, predictRes, trueRes)
        totalTP += TP
        totalTn += TN
        totalFP += FP
        totalFN += FN
    totalprecesion = totalTP/(totalTP+totalFP)
    totalrecall = recall = totalTP/(totalTP+totalFN)
    F1 = 2*totalTP/(2*totalTP+totalFP+totalFN)
    print(f'{project}total TP : {totalTP} TN : {totalTn} FP : {totalFP} FN : {totalFN} precesion : {totalprecesion} recall : {totalrecall} F1 : {F1}')
