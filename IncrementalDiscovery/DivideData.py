import csv
import datetime
import math


def sortByTime(elem):
    return elem[0][1]

def sortByM(elem):
    return elem[-1][-2]

def sortByY(elem):
    return elem[-1][-1]

def DiviData(dataset):
    # 按轨迹分开
    orginal_trace = list()
    trace_temp = list()
    flag = dataset[0][0]
    for line in dataset:
        if flag == line[0]:
            trace_temp.append(line)
        else:
            orginal_trace.append(trace_temp)
            trace_temp = list()
            trace_temp.append(line)
        flag = line[0]
    # 轨迹按时间排序,去掉日期属性列
    # orginal_trace.sort(key=sortByTime)
    # for line1 in orginal_trace:
    #     for line2 in line1:
    #         line2.remove(line2[0])
    #         line2.remove(line2[0])
    #         line2.remove(line2[0])


    return orginal_trace

def DiviDataByTime(AllData): #给轨迹排序
    # 轨迹按时间排序,去掉日期属性列
    AllData.sort(key=sortByM)
    AllData.sort(key=sortByY) #此时时间为年月日
    # 确定周期数
    month = str(AllData[0][-1][-1]) + '-' + str(AllData[0][-1][-2])
    Datas = {month:[]}
    for line in AllData:
        if month == str(line[-1][-1]) + '-' + str(line[-1][-2]):
            Datas[month].append(line)
        else:
            month = str(line[-1][-1]) + '-' + str(line[-1][-2])
            Datas[month] = []
            Datas[month].append(line)
    for name in Datas.keys():
        f = open(name + '.csv', 'w', newline='', encoding='utf-8')
        f_csv = csv.writer(f)
        # f_csv.writerow(header)
        for line1 in Datas[name]:
            for line in line1:
                f_csv.writerow([line[0],line[3],line[1],line[2]])
        f.close()
    return Datas
    # 按比例划分训练集和测试集
    # timeNum = len(Datas)
    # trainNum = math.floor(timeNum*proportion)
    # Train = []
    # Test = []
    # Tests = {}
    # for line in Datas:
    #     if trainNum == 0:
    #         for line2 in Datas[line]:
    #             Test.append(line2)
    #         Tests[line] = Datas[line]
    #     else:
    #         for line2 in Datas[line]:
    #             Train.append(line2)
    #         trainNum -= 1
    # return Train, Test, Tests
