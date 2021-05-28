'''
Author: your name
Date: 2021-05-28 16:26:26
LastEditTime: 2021-05-28 16:44:10
Description: file content
'''
import pandas as pd
from collections import Counter
from imblearn.over_sampling import SMOTE
GLOBAL_VAR = {
    'TRAIN_CSV_PATH': "/Users/lvlaxjh/code/CBFL/data/chart/chart_data1.csv",  # 训练集csv路径
    'TEST_CSV_PATH': "/Users/lvlaxjh/code/CBFL/data/chart/chart_data_test.csv",  # 测试集csv路径
    'MODEL_SAVE_PATH': 'DecisionTree/res/',  # 模型保存路径
    'TREE_PDF_SAVE_PATH': 'DecisionTree/res/',  # 绘图保存路径
    'MODEL_PATH': '/Users/lvlaxjh/code/CBFL/DecisionTree/res/tree.joblib',  # 模型路径
}
data = pd.read_csv(GLOBAL_VAR['TRAIN_CSV_PATH'])  # 读取csv
x = data.iloc[:, [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17]]  # 取训练数据
y = data['accuracy']  # 取样本类标签
print(Counter(y))

smo = SMOTE(random_state=42)

x_smo, y_smo = smo.fit_resample(x, y)

print(Counter(y_smo))
print(y_smo.head(10))
# x_train , x_test, y_train, y_test = train_test_split(
#     x, y, test_size=0.2)  # 数据集划分，生成训练集和测试集
