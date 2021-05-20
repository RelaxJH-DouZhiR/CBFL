'''
Author: your name
Date: 2021-05-20 14:47:36
LastEditTime: 2021-05-20 21:07:15
Description: file content
'''
import json
import copy
GLOBAL_VAR = {
    "AST_KEYWORD_LIST": ["identifier", "value", "keyword", "escapedValue", "operator"],
    "JAVA_PATH": "/Users/lvlaxjh/code/CBFL/AST/testjava/App.java",
    "JSON_PATH": "/Users/lvlaxjh/code/CBFL/AST/EclipseAST/resultJson/result.json",  # json文件路径
    "TARGET_CODE": "            System.out.println(\"helloworld\");",
    "ASTDict": {},  # AST树-json转为字典
    "resultDict": [],  # 结果字典

}


def get_code_element(targetCodeLine):
    global GLOBAL_VAR
    file = open(GLOBAL_VAR['JSON_PATH'], 'r')
    ASTDict = json.loads(file.read())
    for key, val in ASTDict.items():
        # 包-start
        if key == "package":  # 包-AST
            packageItem = val
            get_code_recursion(packageItem, [], targetCodeLine)
        # 包-end
        # 类-start
        if key == "types":  # 类-AST
            typeItem = val
            for i in typeItem:
                get_code_recursion(i, [], targetCodeLine)
        # 类-end
    print(GLOBAL_VAR['resultDict'])


def get_code_recursion(recItem, nodeStack, targetCodeLine):
    global GLOBAL_VAR
    if type(recItem) is dict:  # 字典递归
        if 'node' in recItem.keys():
            nodeStack.append(recItem['node'])
            # print(nodeStack)
        # 判断-当前节点是否包含node-start
        # 需要入栈
        if 'node' in recItem.keys() and recItem['node_line'] == targetCodeLine:
            for i in GLOBAL_VAR['AST_KEYWORD_LIST']:
                if i in recItem.keys() and recItem[i] in GLOBAL_VAR['TARGET_CODE']:
                    nodeDice_TEM = {
                        "code": recItem[i],
                        "code_line": recItem['node_line'],
                        "father_node": copy.deepcopy(nodeStack),
                    }
                    # print(nodeDice_TEM)
                    GLOBAL_VAR['resultDict'].append(nodeDice_TEM)
        # 判断-当前节点是否包含node-end
        for key, val in recItem.items():
            if type(val) is dict or type(val) is list:
                get_code_recursion(val, nodeStack, targetCodeLine)
        if 'node' in recItem.keys():  # 需要出栈
            nodeStack.pop()
    if type(recItem) is list:  # 列表递归
        for i in recItem:
            get_code_recursion(i, nodeStack, targetCodeLine)


def judge_include_list_dict(item):  # 判断当前元素内部是否包含列表或事字典
    if type(item) is dict:
        for i in item.values():
            if type(i) is dict or type(i) is list:
                return True
    elif type(item) is list:
        for i in item:
            if type(i) is dict or type(i) is list:
                return True
    return False


if __name__ == "__main__":
    get_code_element(24)