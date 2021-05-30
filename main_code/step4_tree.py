'''
Author: your name
Date: 2021-05-25 18:47:20
LastEditTime: 2021-05-30 22:00:24
Description: 决策🌲
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

GLOBAL_VAR = {
    'TRAIN_CSV_PATH': "/Users/lvlaxjh/code/CBFL/data/chart/chart_data_nodup_train.csv",  # 训练集csv路径
    'TEST_CSV_PATH': "/Users/lvlaxjh/code/CBFL/data/chart/chart_data_nodup_test.csv",  # 测试集csv路径
    'MODEL_SAVE_PATH': 'DecisionTree/res/',  # 模型保存路径
    'TREE_PDF_SAVE_PATH': 'DecisionTree/res/',  # 绘图保存路径
    'MODEL_PATH': '/Users/lvlaxjh/code/CBFL/DecisionTree/res/tree.joblib',  # 模型路径
}


def draw_tree(treeModel, feature_names, class_names, savePath):
    dot_data = tree.export_graphviz(
        treeModel, out_file=None, feature_names=feature_names, class_names=class_names, filled=True, rounded=True, special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render(savePath)


def get_best_tree():  # 训练决策树
    global GLOBAL_VAR
    data = pd.read_csv(GLOBAL_VAR['TRAIN_CSV_PATH'])  # 读取csv
    x = data.iloc[:, [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17]]  # 取训练数据
    y = data['accuracy']  # 取样本类标签
    # SMOTE
    smo = SMOTE(random_state=5)
    x, y = smo.fit_resample(x, y)
    print(Counter(y))
    #
    scoreList = []
    bestNum = 0
    bestScore = 0
    for i in range(10):
        # 实例化决策树
        decTreeClass = DecisionTreeClassifier(
            criterion='gini', splitter='best', max_depth=5)
        # decTreeClass = DecisionTreeClassifier()
        # x_train , x_test, y_train, y_test = train_test_split(
        #     x, y, test_size=0.2)  # 数据集划分，生成训练集和测试集
        kf = KFold(n_splits=10, shuffle=True)  # k折交叉验证
        for train_index, test_index in kf.split(x):
            x_train = x[x.index.isin(train_index)]
            x_test = x[x.index.isin(test_index)]
            y_train = y[y.index.isin(train_index)]
            y_test = y[y.index.isin(test_index)]
            #
            decTreeClass = decTreeClass.fit(x_train, y_train)  # 输入训练集
        decTreeClass = decTreeClass.fit(x_train, y_train)  # 输入训练集
        result = decTreeClass.score(x_test, y_test)  # 测试集
        print('%s score : %s' % (str(i), str(result)))
        scoreList.append({
            'score': str(result),
            'tree': decTreeClass,
        })
        if result > bestScore:
            bestScore = result
            bestNum = i
    # print(scoreList)
    dump(scoreList[bestNum]['tree'],
         GLOBAL_VAR['MODEL_SAVE_PATH']+"tree.joblib")
    draw_tree(scoreList[bestNum]['tree'], ['varTotal', 'optTotal', 'array', 'bracketDepth', 'bracketTotal',
                                           'keywordTotal', 'methodTotal', 'typeTotal', 'logic', 'lengthEle', 'depth'], ['0', '1'], GLOBAL_VAR['TREE_PDF_SAVE_PATH']+"tree")
    print('bestNumber : ' + str(bestNum))
    print('bestScore : ' + str(bestScore))
    return result


def predict_model():  # 预测
    global GLOBAL_VAR
    data = pd.read_csv(GLOBAL_VAR['TEST_CSV_PATH'])  # 读取csv
    x = data.iloc[:, [6, 7, 8, 9, 10, 11, 12, 13, 14, 15,  17]]  # 测试数据
    # print(x.head(10))
    decTreeClass = load(GLOBAL_VAR['MODEL_PATH'])
    predictRes = decTreeClass.predict(x)
    predictResList = decTreeClass.predict_proba(x)
    print(predictRes)
    print(predictResList)
    for i in range(len(predictRes)):
        if predictRes[i] == 1:
            print(i+1)
            print(predictResList[i])
    # print(predictResList)
    return predictRes, predictResList


if __name__ == "__main__":
    get_best_tree()

    predict_model()
