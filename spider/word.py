import docx
import re
import os
from win32com import client as wc
word = wc.Dispatch("Word.Application")

def content():
    a=[]
    #获取文档对象
    ul = r"D:\\a罗\\爬虫project\\word1"  # 需要处理的文件所在文件夹目录
    PROJECT_DIR_PATH = os.path.dirname(os.path.abspath(os.path.abspath(__file__)))
    DIR_PATH = os.path.join(PROJECT_DIR_PATH, ul)
    files = os.listdir(DIR_PATH)
    for fi in files:
        name,su=os.path.splitext(fi)
        file=docx.Document('D:\\a罗\\爬虫project\\word1\\'+name+'.docx')
        #段落数为13，每个回车隔离一段
        #输出每一段的内容
        for para in file.paragraphs:
            a.append(para.text)#输出段落编号及段落内容
    print(str(a))
    return a

def comp(a):
    a=str(a)
    name = re.findall('被告人(.{2,3})，.*?，现住.*?', a)
    sex=re.findall('被告.*?某，(.*?)，现住',a)
    adder=re.findall('被告.*?某，.*?，现住(.*?)。.*?年\d月\d日',a)

    answer=re.findall('因涉嫌犯(.*?)被.*?拘留',a)

    time=re.findall('被告人.*?现住.*?。(.*?)因.*?',a)
    it=[]
    for i in range(len(name)):
        items={
            '姓名':name[i],
            '性别':sex[i],
            '所住省市':adder[i],
            '犯罪时间':time[i],
            '案由':answer[i]
        }
        it.append(items)
    print(it)
    return it

from openpyxl import Workbook
Lable = ['A','B','C','D','E','F','H']
'''
inputData: 列表，含有多个字典;例如：[{'key_a':'123'},{'key_b':'456'}]
outPutFile：输出文件名，例如：'data.xlsx'
'''
def writeDataToExcleFile(inputData,outPutFile):
    wb = Workbook()
    sheet = wb.active
    sheet.title = "Sheet1"
    item_0 = inputData[0]
    i = 0
    for key in item_0.keys():
        sheet[Lable[i]+str(1)].value = key
        i = i+1
    j = 1
    for item in inputData:
        k = 0
        for key in item:
            sheet[Lable[k]+str(j+1)].value = item[key]
            k = k+1
        j = j+1
    wb.save(outPutFile)
    print('数据写入完毕!')


def main():
    a=content()
    it=comp(a)
    writeDataToExcleFile(it,r'D:\a罗\a.xlsx')
    # with open(r'D:\a罗\a.xlsx', 'w', encoding='utf-8') as f:
    #     f.write(df)
if __name__ == '__main__':
    main()
# print(a)