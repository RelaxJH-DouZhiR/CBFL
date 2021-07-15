"""
Author: jhc
Date: 2021-06-02 16:15:11
LastEditTime: 2021-06-29 00:59:02
Description: 根据excel解析复杂度存储至csv
 █████╗ ███╗   ██╗ █████╗ ██╗  ██╗   ██╗████████╗██╗ ██████╗
██╔══██╗████╗  ██║██╔══██╗██║  ╚██╗ ██╔╝╚══██╔══╝██║██╔════╝
███████║██╔██╗ ██║███████║██║   ╚████╔╝    ██║   ██║██║
██╔══██║██║╚██╗██║██╔══██║██║    ╚██╔╝     ██║   ██║██║
██║  ██║██║ ╚████║██║  ██║███████╗██║      ██║   ██║╚██████╗
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝      ╚═╝   ╚═╝ ╚═════╝
 ██████╗ ██████╗ ███╗   ███╗██████╗ ██╗     ███████╗██╗  ██╗██╗████████╗██╗   ██╗
██╔════╝██╔═══██╗████╗ ████║██╔══██╗██║     ██╔════╝╚██╗██╔╝██║╚══██╔══╝╚██╗ ██╔╝
██║     ██║   ██║██╔████╔██║██████╔╝██║     █████╗   ╚███╔╝ ██║   ██║    ╚████╔╝
██║     ██║   ██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝   ██╔██╗ ██║   ██║     ╚██╔╝
╚██████╗╚██████╔╝██║ ╚═╝ ██║██║     ███████╗███████╗██╔╝ ██╗██║   ██║      ██║
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝
"""
import json
import copy
import openpyxl
import shutil
import csv
import re


resultList = []  # 结果列表
JSON_PATH = "E:/DSatr/chart-direct/chart-5/source/org/jfree/data/xy/XYSeries.json"
# JSON_PATH = ''

# AST包，库，类遍历-start


def get_code_element(targetCodeLine, codeStatement):  # 目标代码行数，代码内容
    global JSON_PATH
    file = open(JSON_PATH, "r")
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


# AST包，库，类遍历-end


# 递归遍历AST树-start
def get_code_recursion(recItem, nodeStack, targetCodeLine, codeStatement):  # 树，节点栈，目标代码行数，代码内容
    global resultList
    AST_KEYWORD_LIST = ["identifier", "value", "keyword", "escapedValue", "operator", "booleanValue", "expression"]
    if type(recItem) is dict:  # 字典递归
        if "node" in recItem.keys():
            nodeStack.append(recItem["node"])  # 父节点入栈
        if "node" in recItem.keys() and str(recItem["node_line"]) == str(targetCodeLine):
            for keyword in AST_KEYWORD_LIST:
                if keyword in recItem.keys() and type(recItem[keyword]) is str:
                    nodeDice_TEM = {
                        "code": recItem[keyword],
                        "code_line": recItem["node_line"],
                        "father_node": copy.deepcopy(nodeStack),
                    }
                    resultList.append(copy.deepcopy(nodeDice_TEM))
        for key, val in recItem.items():
            if type(val) is dict or type(val) is list:  # 深层递归
                get_code_recursion(val, nodeStack, targetCodeLine, codeStatement)
        if "node" in recItem.keys():  # 父节点出栈
            nodeStack.pop()
    if type(recItem) is list:  # 列表递归
        for i in recItem:
            get_code_recursion(i, nodeStack, targetCodeLine, codeStatement)


# 递归遍历AST树-end


# 获取括号数量、嵌套层数-start
def get_brackets_nesting(codeStatement):  # 代码内容（返回：括号嵌套层数，括号总数）
    bracketsStack = []  # 括号栈
    depthList = []  # 括号深度列表
    depth = 0
    total = 0  # 括号数量
    if codeStatement is not None:
        for i in codeStatement:
            if i == "(":
                bracketsStack.append(")")
            elif i == "[":
                bracketsStack.append("]")
            elif i == "{":
                bracketsStack.append("}")
            if len(bracketsStack) != 0 and (i == ")" or i == "]" or i == "}"):  # 栈不为空
                bracketsStack.pop()
                depth += 1
                if bracketsStack == []:
                    depthList.append(depth)
                    depth = 0
            # 计算总数
            if i == "(" or i == ")" or i == "[" or i == "]" or i == "{" or i == "}":
                total += 1
    #
    codeStatement = re.sub("[^(,)]", "", codeStatement)
    depth = 0
    # 循环替换(),没循环一次，深度加1
    while "()" in codeStatement:
        codeStatement = codeStatement.replace("()", "")
        depth += 1
    # 如果clean_s不为空，则为非有效括号字符串，返回-1，否则为有效括号字符串，返回depth
    return depth, total


# 获取括号数量、嵌套层数-end


# 逻辑-start
# def get_logic_word(codeStatement):  # 代码内容（返回：bool是否包含逻辑）
#     logicList = ["if", "else if", "else", "switch", "case", "while", "for"]
#     for n in logicList:
#         pattern = re.compile(n)  # 模式
#         if codeStatement is not None:
#             for i in pattern.finditer(codeStatement):
#                 if i.start() > 0 and (codeStatement[i.start() - 1].isdigit() or codeStatement[i.start() - 1].isalpha()):  # 前一个字符为字母或数字
#                     return False
#                 elif (i.start() + len(n)) >= len(codeStatement) or ((i.start() + len(n)) < len(codeStatement) and codeStatement[i.start() + len(n)].isdigit() or codeStatement[i.start() + len(n)].isalpha()):
#                     return False
#                 else:
#                     return True
#         else:
#             return False


# 逻辑-end


# 关键字-start
def get_keyword(codeStatement):  # 代码内容（返回：关键字数量）
    keywordList = ['abstract', 'continue', 'for', 'new', 'switch', 'assert', 'default', 'goto', 'package', 'synchronized', 'boolean', 'do', 'if', 'private', 'this', 'break', 'double', 'implements', 'protected', 'throw', 'byte', 'else', 'import', 'public', 'throws', 'case',
                   'enum', 'instanceof', 'return', 'transient', 'catch', 'extends', 'int', 'short', 'try', 'char', 'final', 'interface', 'static', 'void', 'class', 'finally', 'long', 'strictfp', 'volatile', 'const', 'float', 'native', 'super', 'while', 'forever']
    total = 0
    for n in keywordList:
        pattern = re.compile(n)  # 模式
        if codeStatement is not None:
            for i in pattern.finditer(str(codeStatement)):
                if i.start() > 0 and (codeStatement[i.start() - 1].isdigit() or codeStatement[i.start() - 1].isalpha()):  # 关键字前是字母或数字，不为关键字
                    pass
                elif (i.start() + len(n)) >= len(codeStatement) or ((i.start() + len(n)) < len(codeStatement) and codeStatement[i.start() + len(n)].isdigit() or codeStatement[i.start() + len(n)].isalpha()):
                    pass
                #    return
                else:
                    total += 1
    return total


# 关键字-end


# csv存储结构-start
def get_data_for_csv(resultList, targetCodeLine, codeStatement):  # resultList,目标代码行数，代码内容
    csvRes = {
        "varTotal": 0,  # 变量+
        "optTotal": 0,  # 运算符+
        "array": 0,  # 数组-01+
        "bracketDepth": 0,  # 括号深度+
        "bracketTotal": 0,  # 括号总数+
        "keywordTotal": 0,  # 关键字+
        "methodTotal": 0,  # 函数+
        "typeTotal": 0,  # 类+
        "other": 0,  # 其他
        "lengthEle": 0,  # 元素数+
        "lengthWord": 0,  # 字数+
        "depth": 0,  # 深度+
    }
    csvRes["lengthWord"] = len(codeStatement.strip())  # 字数
    # 深度计算-start
    depth_TEM = 0
    depth_TEM = len(resultList[0]["father_node"])
    for i in resultList:
        if len(i["father_node"]) < depth_TEM:
            depth_TEM = len(i["father_node"])
    flag_TEM = 0
    while True:
        compareFlag_TEM = ""
        canBreak_TEM = False
        for i in range(len(resultList)):
            if i == 0:
                compareFlag_TEM = resultList[i]["father_node"][flag_TEM]
            else:
                if resultList[i]["father_node"][flag_TEM] != compareFlag_TEM:
                    canBreak_TEM = True
        if flag_TEM == depth_TEM - 1:
            canBreak_TEM = True
        flag_TEM += 1
        if canBreak_TEM:
            csvRes["depth"] = flag_TEM - 1  # 存储深度
            break
    # 深度计算-end
    csvRes["bracketDepth"], csvRes["bracketTotal"] = get_brackets_nesting(codeStatement)
    csvRes["keywordTotal"] += get_keyword(codeStatement)
    for i in resultList:
        if i["father_node"][len(i["father_node"]) - 1] == "InfixExpression":  # 运算符
            csvRes["optTotal"] += 1
            continue
        if i["father_node"][len(i["father_node"]) - 1] == "SimpleName" and i["father_node"][len(i["father_node"]) - 2] == "SimpleType":  # 类
            csvRes["typeTotal"] += 1
            continue
        if i["father_node"][len(i["father_node"]) - 1] == "SimpleName" and i["father_node"][len(i["father_node"]) - 2] == "MethodInvocation":  # 函数
            csvRes["methodTotal"] += 1
            continue
        if i["father_node"][len(i["father_node"]) - 1] == "SimpleName" and (i["father_node"][len(i["father_node"]) - 2] == "ArrayCreation" or i["father_node"][len(i["father_node"]) - 2] == "ArrayAccess"):  # 数组
            csvRes["array"] = 1
            continue
        if i["father_node"][len(i["father_node"]) - 1] == "SimpleName":  # 变量
            csvRes["varTotal"] += 1
            continue
        if i["father_node"][len(i["father_node"]) - 1] != "SimpleName":  # 其他,优先级最低
            csvRes["other"] += 1
    lengthEle = 0
    for key, val in csvRes.items():
        if val != 0 and key != 'lengthEle' and key != 'lengthWord' and key != 'depth':
            lengthEle += 1
    csvRes["lengthEle"] = lengthEle
    return csvRes


# csv存储结构-end


# 计算复杂度并存储csv-start-------------------------------------------------------------------
def save_as_csv(CSV_PATH, CSV_FATHER_PATH, CODE_FILE_PATH, version, project):
    global resultList, JSON_PATH
    """
    EXCEL_PATH - excel路径
    CSV_FATHER_PATH - 存储文件csv的父路径
    JSON_PATH - ASTJSON的父路径，同代码父路径
    """
    #
    codeLine = 0  # 代码行数
    codeStatement = ""  # 代码
    suspicious = 0  # 可疑度
    accuracy = 0  # 是否为真实缺陷
    #
    saveCsvFile = open(CSV_FATHER_PATH + f"{project}-{version}.csv", "w", encoding="utf-8", newline="")
    csvWriter = csv.writer(saveCsvFile)
    csvWriter.writerow(["dataset", "project", "path", "version", "codeLine", "statement", "varTotal", "optTotal", "array", "bracketDepth", "bracketTotal",
                       "keywordTotal", "methodTotal", "typeTotal", "other", "lengthEle", "lengthWord", "depth", "suspicious", "accuracy", "miss_line"])  # csv文件头
    with open(CSV_PATH) as f:
        csvFile = csv.reader(f)
        for row in csvFile:
            if row[0] != "project_path":
                version = row[1]
                codeLine = row[2]
                codeStatement = row[3]
                suspicious = row[4]
                accuracy = row[5]
                JSON_PATH = CODE_FILE_PATH + row[0] + ".json"  # AST json文件路径
                #
                if codeStatement is not None:
                    get_code_element(codeLine, codeStatement)  # 解析
                    # AST无法解析 - start
                    if resultList == []:
                        keywordTotal = get_keyword(codeStatement)  # 总数
                        bracketDepth, bracketTotal = get_brackets_nesting(codeStatement)  # 括号深度，总数
                        lengthEle = 0
                        if keywordTotal != 0:
                            lengthEle += 1
                        if bracketDepth != 0:
                            lengthEle += 1
                        if bracketTotal != 0:
                            lengthEle += 1
                        csvWriter.writerow(["defect4j", project, row[0], version, codeLine, codeStatement, 0, 0, 0, bracketDepth, bracketTotal, keywordTotal, 0, 0, 0, lengthEle, len(codeStatement.strip()), 2, suspicious, accuracy, row[7]])
                    else:
                        astresultList = get_data_for_csv(resultList, codeLine, codeStatement)
                        csvWriter.writerow(
                            [
                                "defect4j",
                                project,
                                row[0],
                                version,
                                codeLine,
                                codeStatement,
                                astresultList["varTotal"],
                                astresultList["optTotal"],
                                astresultList["array"],
                                astresultList["bracketDepth"],
                                astresultList["bracketTotal"],
                                astresultList["keywordTotal"],
                                astresultList["methodTotal"],
                                astresultList["typeTotal"],
                                astresultList["other"],
                                astresultList["lengthEle"],
                                astresultList["lengthWord"],
                                astresultList["depth"],
                                suspicious,
                                accuracy,
                                row[7],
                            ]
                        )
                        resultList = []
                    #
                    print(f"{project}-{version} - {row[0]} -  {codeLine} -> ok")
    #
    saveCsvFile.close()
    print(f"\033[1;36m analytic_complexity >{project}< >{version}< \033[0m")


# 计算复杂度并存储csv-end-------------------------------------------------------------------
# if __name__ == "__main__":
