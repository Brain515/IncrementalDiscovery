##原始日志属性处理，输入原始日志csv，输出属性标签csv作为特征选择的输入文件
#caseID、数值属性不动，字符属性转为序号，时间属性进行转换

from numpy import loadtxt
import copy
import time
from datetime import datetime
from scipy.io import savemat

import csv

#读取文件
def readcsv(eventlog):
    csvfile = open(eventlog, 'r')
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    sequence = []
    header = next(spamreader)
    # next(spamreader, None)  # skip the headers
    for line in spamreader:
        sequence.append(line)
    return sequence, header

#对字符属性进行标号
def makeVocabulary(data, index, co=None):
    temp = list()
    for line in data:
        temp.append(line[index])#原去掉int()
    temp_temp = set(temp)#删除重复数据
    if 'null' in temp_temp:
        temp_temp.remove('null')
    if co == None:
        vocabulary = {str(sorted(list(temp_temp))[i]): i + 1 for i in range(len(temp_temp))}
        vocabulary['null'] = 0
    else:
        vocabulary = {co[i]: i for i in range(len(co))}
        for line in temp_temp:
            if line not in vocabulary.keys():
                vocabulary[line] = len(vocabulary)
    for i in range(len(data)):
        data[i][index] = vocabulary[data[i][index]]
    voc = {vocabulary[i]: i for i in vocabulary.keys()}
    return voc


#计算时间特征
def makeTime(data, index):
    ind = 0
    front = data[ind]
    t = time.strptime(front[index], "%Y/%m/%d %H:%M")
    data[ind].append(t.tm_mon) #月/12
    data[ind].append(t.tm_year-2000) #年-2000 增量
    for line in data[1:]:
        ind += 1
        t = time.strptime(line[index], "%Y/%m/%d %H:%M")
        data[ind].append(t.tm_mon)
        data[ind].append(t.tm_year - 2000)

#计算标签
def makeLable(data, ti, ei, maxA, maxR):
    ind = 0
    front = data[ind]
    for line in data[1:]:
        if line[0] == front[0]:
            data[ind].append(line[ei]) #下一事件
            data[ind].append(line[ti]) #下一事件持续时间*maxR
        else:
            data[ind].append(0)
            data[ind].append(0.)
        front = line
        ind += 1
    data[ind].append(0)
    data[ind].append(0.)
    data[ind].append(0.) #剩余时间
    count = 0.
    for line in reversed(data[0:-1]):
        ind -= 1
        if line[0] == front[0]:
            count += front[ti]#*maxR
        else:
            count = 0.
        front = line
        data[ind].append(count)  # 剩余时间

def LogC(eventlog):
    data, header = readcsv('D:/BPI-Month/BPIC_2015_5/'+eventlog+'.csv')


    #时间特征，总执行时间，当前事件的执行时间，月日周时
    header.append('month')
    header.append('year')#增量更新
    makeTime(data, 2)

    return data
    #文件保存
    # f = open(eventlog+'F.csv', 'w', newline='', encoding='utf-8')
    # f_csv = csv.writer(f)
    # # f_csv.writerow(header)
    # f_csv.writerows(data)
    # f.close()
    #
    # mdict = {'header': header, 'vocab_3': vocab_3, 'vocab_5': vocab_5}#
    # savemat('data/'+eventlog+'F.mat', mdict)

    # f1 = open('hdf.fmap', "w")
    # for i, feat in enumerate(header):
    #     f1.write('{0}\t{1}\tq\n'.format(i, feat))
    # f1.close()