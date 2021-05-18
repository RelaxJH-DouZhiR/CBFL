'''
Author: your name
Date: 2021-05-18 09:51:21
LastEditTime: 2021-05-18 10:11:23
Description: file content
'''
import linecache
import openpyxl
CODE_FILE_PATH = '/Users/lvlaxjh/code/CBFL/AST/EclipseAST/App.java'
EXCEL_FILE_PATH = '/Users/lvlaxjh/code/CBFL/FileProcessing/123.xlsx'
excel = openpyxl.load_workbook(EXCEL_FILE_PATH)
sheet = excel.worksheets[0]
line = 2
codeLineList = []
while True:
    if sheet.cell(line, 2).value != None:
        codeLineList.append(sheet.cell(line, 2).value)
    else:
        break
    line+=1
line = 2
for i in codeLineList:
    the_line = linecache.getline(CODE_FILE_PATH, i)
    sheet.cell(line, 3).value = the_line
    line +=1
# line = 5
excel.save(EXCEL_FILE_PATH)
