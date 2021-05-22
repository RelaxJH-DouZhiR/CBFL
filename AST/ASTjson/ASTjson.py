'''
Author: your name
Date: 2021-05-20 14:47:36
LastEditTime: 2021-05-22 10:43:23
Description: file Statement
'''
import json
import copy
import re
import csv

GLOBAL_VAR = {
    "AST_KEYWORD_LIST": ["identifier", "value", "keyword", "escapedValue", "operator"],
    "JAVA_PATH": "/Users/lvlaxjh/code/dataset/d4j/lang_1_buggy/src/main/java/org/apache/commons/lang3/StringUtils.java",
    "JSON_PATH": "/Users/lvlaxjh/code/CBFL/AST/EclipseAST/resultJson/result.json",  # json文件路径
    "CSV_PATH": "/Users/lvlaxjh/code/CBFL/AST/test.csv",
    "ASTDict": {},  # AST树-json转为字典
    "resultDict": [],  # 结果字典
}


# AST包，库，类遍历-start
def get_code_element(targetCodeLine, codeStatement):  # 目标代码行数，代码内容
    global GLOBAL_VAR
    file = open(GLOBAL_VAR['JSON_PATH'], 'r')
    ASTDict = json.loads(file.read())
    for key, val in ASTDict.items():
        # 包-start
        if key == "package":  # 包-AST
            packageItem = val
            get_code_recursion(packageItem, [], targetCodeLine, codeStatement)
        # 包-end
        # 库-start
        if key == "imports":
            importItem = val
            for i in importItem:
                get_code_recursion(i, [], targetCodeLine, codeStatement)
        # 库-end
        # 类-start
        if key == "types":  # 类-AST
            typeItem = val
            for i in typeItem:
                get_code_recursion(i, [], targetCodeLine, codeStatement)
        # 类-end
    print(GLOBAL_VAR['resultDict'])
# AST包，库，类遍历-end


# 递归遍历AST树-start
def get_code_recursion(recItem, nodeStack, targetCodeLine, codeStatement):  # 树，节点栈，目标代码行数，代码内容
    global GLOBAL_VAR
    if type(recItem) is dict:  # 字典递归
        if 'node' in recItem.keys():
            nodeStack.append(recItem['node'])  # 父节点入栈
        if 'node' in recItem.keys() and recItem['node_line'] == targetCodeLine:
            for i in GLOBAL_VAR['AST_KEYWORD_LIST']:
                if i in recItem.keys() and recItem[i] in codeStatement:
                    nodeDice_TEM = {
                        "code": recItem[i],
                        "code_line": recItem['node_line'],
                        "father_node": copy.deepcopy(nodeStack),
                    }
                    GLOBAL_VAR['resultDict'].append(nodeDice_TEM)
        for key, val in recItem.items():
            if type(val) is dict or type(val) is list:  # 深层递归
                get_code_recursion(
                    val, nodeStack, targetCodeLine, codeStatement)
        if 'node' in recItem.keys():  # 父节点出栈
            nodeStack.pop()
    if type(recItem) is list:  # 列表递归
        for i in recItem:
            get_code_recursion(i, nodeStack, targetCodeLine, codeStatement)
# 递归遍历AST树-end


# 获取括号数量、嵌套层数-start
def get_brackets_nesting(codeStatement):  # 代码内容（返回：括号嵌套层数，括号总数）
    bracketsStack = []  # 括号栈
    depth = 0  # 括号深度
    total = 0  # 括号数量
    for i in codeStatement:
        if i == '(':
            bracketsStack.append(')')
        elif i == '[':
            bracketsStack.append(']')
        elif i == '{':
            bracketsStack.append('}')
        if len(bracketsStack) != 0 and (i == ')' or i == ']' or i == '}'):  # 栈不为空
            bracketsStack.pop()
            depth += 1
        # 计算总数
        if i == '(' or i == ')' or i == '[' or i == ']' or i == '{' or i == '}':
            total += 1
    return depth, total
# 获取括号数量、嵌套层数-end


# 逻辑-start
def get_logic_word(codeStatement):  # 代码内容（返回：bool是否包含逻辑）
    logicList = ['if', 'else if', 'else', 'switch', 'case', 'while', 'for']
    for n in logicList:
        pattern = re.compile(n)   # 模式
        for i in pattern.finditer(codeStatement):
            if i.start() > 0 and (codeStatement[i.start()-1].isdigit() or codeStatement[i.start()-1].isalpha() or codeStatement[i.start()+len(n)].isdigit() or codeStatement[i.start()+len(n)].isalpha()):
                return False
            elif codeStatement[i.start()+len(n)].isdigit() or codeStatement[i.start()+len(n)].isalpha():
                return False
            else:
                return True
# 逻辑-end


# 关键字-start
def get_keyword(codeStatement):  # 代码内容（返回：关键字数量）
    keywordList = ['return']
    total = 0
    for n in keywordList:
        pattern = re.compile(n)   # 模式
        for i in pattern.finditer(codeStatement):
            if i.start() > 0 and (codeStatement[i.start()-1].isdigit() or codeStatement[i.start()-1].isalpha() or codeStatement[i.start()+len(n)].isdigit() or codeStatement[i.start()+len(n)].isalpha()):
                pass
            elif codeStatement[i.start()+len(n)].isdigit() or codeStatement[i.start()+len(n)].isalpha():
                pass
            else:
                total += 1
    return total
# 关键字-end

# csv存储结构-start


def get_data_for_csv(resultDict, targetCodeLine, codeStatement):  # resultDict,目标代码行数，代码内容
    csvRes = {
        'varTotal': 0,  # 变量+
        'optTotal': 0,  # 运算符+
        'array': 0,  # 数组-01+
        'bracketDepth': 0,  # 括号深度+
        'bracketTotal': 0,  # 括号总数+
        'keywordTotal': 0,  # 关键字+
        'methodTotal': 0,  # 函数+
        'typeTotal': 0,  # 类+
        'logic': 0,  # 逻辑，01+
        'lengthEle': 0,  # 元素数+
        'lengthWord': 0,  # 字数+
        'depth': 0,  # 深度+
    }
    csvRes['lengthWord'] = len(codeStatement.strip())  # 字数
    csvRes['lengthEle'] = len(resultDict)  # 元素数
    # 深度计算-start
    depth_TEM = 0
    depth_TEM = len(resultDict[0]['father_node'])
    for i in resultDict:
        if len(i['father_node']) < depth_TEM:
            depth_TEM = len(i['father_node'])
    flag_TEM = 0
    while True:
        compareFlag_TEM = ''
        canBreak_TEM = False
        for i in range(len(resultDict)):
            if i == 0:
                compareFlag_TEM = resultDict[i]['father_node'][flag_TEM]
            else:
                if resultDict[i]['father_node'][flag_TEM] != compareFlag_TEM:
                    canBreak_TEM = True
        if flag_TEM == depth_TEM-1:
            canBreak_TEM = True
        flag_TEM += 1
        if canBreak_TEM:
            csvRes['depth'] = flag_TEM-1#存储深度
            break
    # 深度计算-end
    if get_logic_word(codeStatement):  # 逻辑
        csvRes['logic'] = 1
    csvRes['bracketDepth'], csvRes['bracketTotal'] = get_brackets_nesting(
        codeStatement)
    csvRes['keywordTotal'] += get_keyword(codeStatement)
    for i in resultDict:
        if i['father_node'][len(i['father_node'])-1] == 'InfixExpression':  # 运算符
            csvRes['optTotal'] += 1
            continue
        if i['father_node'][len(i['father_node'])-1] == 'Modifier':  # 关键字
            csvRes['keywordTotal'] += 1
            continue
        if i['father_node'][len(i['father_node'])-1] == 'SimpleName' and i['father_node'][len(i['father_node'])-2] == 'SimpleType':  # 类
            csvRes['typeTotal'] += 1
            continue
        if i['father_node'][len(i['father_node'])-1] == 'SimpleName' and i['father_node'][len(i['father_node'])-2] == 'MethodInvocation':  # 函数
            csvRes['methodTotal'] += 1
            continue
        if i['father_node'][len(i['father_node'])-1] == 'SimpleName' and (i['father_node'][len(i['father_node'])-2] == 'ArrayCreation' or i['father_node'][len(i['father_node'])-2] == 'ArrayAccess'):  # 数组
            csvRes['array'] = 1
            continue
        if i['father_node'][len(i['father_node'])-1] == 'SimpleName':  # 变量,优先级最低
            csvRes['varTotal'] += 1
    return csvRes
# csv存储结构-end


if __name__ == "__main__":
    codeLine = 171
    codeStatement = "    private static final int PAD_LIMIT = 8192;"
    suspicious = 0.707106781
    accuracy = 1
    get_code_element(codeLine, codeStatement)
    print('codeLine : ' + str(codeLine))
    print('codeStatement : ' + codeStatement)
    astResultDict = get_data_for_csv(
        GLOBAL_VAR['resultDict'], codeLine, codeStatement)
    csvFile = open(GLOBAL_VAR['CSV_PATH'], 'a', encoding="utf-8", newline="")
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['defect4j', 'Lang', 'org.apache.commons.lang3.ClassUtils', '1', codeLine, codeStatement, astResultDict['varTotal'], astResultDict['optTotal'], astResultDict['array'], astResultDict['bracketDepth'],
                       astResultDict['bracketTotal'], astResultDict['keywordTotal'], astResultDict['methodTotal'], astResultDict['typeTotal'], astResultDict['logic'], astResultDict['lengthEle'], astResultDict['lengthWord'], astResultDict['depth'], suspicious, accuracy])
    csvFile.close()