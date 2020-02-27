# -*- coding: utf-8 -*-
import csv
import numpy as np


"""
step1;处理表，使表变为一个以车牌号为键的字典
输入：表S
输出：字典sheet：{车牌号 ： [时间戳，线路，刷卡人数] }
变量说明：
    reader： 读入的表S
    sheet ： sheet[ line[4] ][0] :这辆车第一次刷卡的时间戳， sheet[ line[4]][2] ：刷卡人数
    head :   表S头（日期，时间戳(当天的秒数)，站点编号，线路名称，车牌号）应该忽略
    flag： # 如果这车两小时内出现两次，需要用flag另外标识。 flag = 0 当前车辆不是出现两次
                flag = 1，出现两次，需要修改车牌号统计
    last_num：上一辆车的车牌号，用于统计出现两次的车
    line[4] = 车牌号； line[1] = 时间戳; line[3] = 线路
    line[4] + '_' ；同一辆车第二趟 时存入字典的车牌号
"""
M = []

with open(r"C:\Users\草明\Desktop\项目组\塘边站相关数据\线路数据\所有天数所有线路.csv", 'r') as f:
    reader = csv.reader(f)
    # {车牌号：[时间戳,线路,刷卡人数]}
    sheet = {}
    last_day  = "20181005"
    print(last_day)
    for line in reader:
            # if not the small day ,work out the correlaton.
            if line[0] != last_day:
                M.append( corr(sheet))
                sheet.clear()
                last_day = line[0]

             # 如果该车不在字典中（从未出现），将其加入。
            if line[5] not in sheet:
                # line[4]车牌号 , line[3]线路
                sheet.setdefault(line[5], []).append(line[1])
                sheet.setdefault(line[5], []).append(line[4])
                sheet.setdefault(line[5], []).append(1)
                # 该车第一次出现
                sheet.setdefault(line[5], []).append(1)
                # 该车最后一次出现的时间戳
                sheet.setdefault(line[5], []).append(line[1])
                last_day = line[0]
            # 特别地，第n趟首次刷卡。此时flag=0 && 与上一次车时间戳相隔超过1000
            elif (eval(line[1]) - eval(sheet[line[5]][4])) > 1000:
                sheet[line[5]][4] = line[1]
                # times++;
                sheet[line[5]][3] += 1
                # 修改当前车辆车牌号 = 车牌号 + 出现次数
                line[5] = line[5] + str(sheet[line[5]][3])
                sheet.setdefault(line[5], []).append(line[1])
                sheet.setdefault(line[5], []).append(line[4])
                sheet.setdefault(line[5], []).append(1)
                sheet.setdefault(line[5], []).append(1)
                last_day = line[0]
            # 平凡的情况
            elif (line[5] + str(sheet[line[5]][3])) in sheet:
                line[5] = line[5] + str(sheet[line[5]][3])
                sheet[line[5]][2] += 1
                last_day = line[0]
            # 统计第一趟车的刷卡人数
            else:
                sheet[line[5]][2] += 1
                last_day = line[0]

print(sheet)
def corr(sheet):
# 统计同一线路刷卡数据，并汇总成二维列表
List = {}
Lines = []
i = 0
for key in sheet.keys():
    # 路线刷卡数据不存在，写入List
        if sheet[key][1] not in List:
            Lines.append([])
            Lines[i].append(sheet[key][2])
            List.setdefault(sheet[key][1], i)
            i += 1
            flag = sheet[key][1]
            # 两个相邻的同路线刷卡数据合并
        elif sheet[key][1] in List and flag == sheet[key][1]:
            Lines[List.get(flag)][-1] = Lines[List.get(flag)][-1] + sheet[key][2]
        elif sheet[key][1] in List and flag != sheet[key][1]:
            Lines[List.get(sheet[key][1])].append(sheet[key][2])
            flag = sheet[key][1]
# 将线路与相应刷卡数序列匹配成列表形式打印出来
a = list(zip(List.keys(), Lines))
for i in a:
        print(i)
# 两两之间计算相关度并写入一个矩阵
for m in range(len(a) - 1):
    for n in range(m + 1, len(a)):
         # 删除元素使列表长度相等
         if len(a[m][1]) > len(a[n][1]):
              L1 = a[m][1][0:len(a[n][1])]
              L2 = a[n][1]
         else:
                L2 = a[n][1][0:len(a[m][1])]
                L1 = a[m][1]
    # 计算标准差
    A = np.array([L1, L2])
    var = np.corrcoef(A)
    print(var)

"""
a1 = [1, 6, 3, 1, 11, 9, 8, 7, 4, 3, 5, 2, 1, 4]
a2 = [6, 4, 4, 4, 2, 7, 5, 4, 5, 1, 2]
if len(a1) > len(a2):
     a1 = a1[0:len(a2)]
     print(a1)
     print(a2)
else:
    a2 = a2[0:len(a1)]
    print(a1)
    print(a2)
# 利用Series将列表转换成新的,pandas可处理的数据
a1s = pd.Series(a1)
a2s = pd.Series(a2)
A = np.array([a1s,a2s])
var = np.corrcoef(A)
print(var)
"""

"""
step2:
输入：字典sheet：{车牌号 ： [时间戳，线路，刷卡人数] }
输出两个列表L1,L2


Line_num=[]
Line = [[]]
last_line = 0
for k in sheet:
    if
len1 = len(L1)
len2 = len(L2)
if len1 > len2 :
    L1 = L1[0:len2]
else:
    L2 = L2[0:len1]
print(L1,L2,len1,len2)
A = np.array([L1,L2])
var = np.corrcoef(A)
print(var)
"""