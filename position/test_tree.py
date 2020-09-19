# -*- coding: cp936 -*-
import trees
import json
import pymysql
from collections import Counter
import pandas

# 获取输入数据的标签
use_label = []
use_label_value = []
frt = open(r'job_predict.txt')
listWm = [inst.strip().split('\t') for inst in frt.readlines()]
print('listWm', len(listWm[0]), len(listWm[1]))

for i in range(len(listWm[0])):
    if listWm[1][i] != '0':
        use_label.append(listWm[0][i])
        use_label_value.append(listWm[1][i])


# 写入有用标签
with open('F:\\untitled\decision_tree\job_predict.txt', "w+") as fil:
    for use in range(len(use_label)):
        fil.write(use_label[use]+'  ')
        # use_label_value[use]
    fil.write('\n')
fil.close()
# 写入数据
with open('F:\\untitled\decision_tree\job_predict.txt', "a+") as fil2:
    for use_value in range(len(use_label_value)):
        fil2.write(use_label_value[use_value]+' ')
fil.close()

# 连接MySQL数据库
conn = pymysql.connect(host='localhost', user='root', password='521125', db='test', charset='utf8')
cursor = pymysql.cursors.SSCursor(conn)

# 获取的各个标签在数据库中的数量统计
sort_count = []
for k in use_label:
    sql = """select count(*) from job_tech_demand where `%s` = '1' or `%s` = '2' or `%s` = '3' or `%s` ='4'""" %(k, k, k, k)
    cursor.execute(sql)
    count_num = cursor.fetchall()
    # count_num_link = str(count_num[0][0])+str(k)
    sort_count.append(count_num[0][0])

# 对标签数量统计的排序
# print(sorted(sort_count))

# 当标签数量大于等于3时，选取数量最多的三个。小于3时，即为2时，则全部选取（也就是说至少输入两个），并从数据库表中获取数据写入测试文件中。


# 创建决策树用的标签
create_tree_lab = []
create_tree_lab2 = []
create_tree_lab_value = []
def num_label(input_number_label):
    if len(input_number_label) >= 3:    # 标签数量大于等于3时
        print(sorted(sort_count)[-1], sorted(sort_count)[-2], sorted(sort_count)[-3])
        print(input_number_label[sort_count.index(sorted(sort_count)[-1])],input_number_label[sort_count.index(sorted(sort_count)[-2])],input_number_label[sort_count.index(sorted(sort_count)[-3])])
        sql1 = """select `%s`, `%s`, `%s`,position_name from job_tech_demand where  (`%s` = '1' or `%s` = '2' or `%s` = '3' or `%s` ='4') and (`%s` = '1' or `%s` = '2' or `%s` = '3' or `%s` ='4') and (`%s` = '1' or `%s` = '2' or `%s` = '3' or `%s` ='4')""" % (
        input_number_label[sort_count.index(sorted(sort_count)[-1])], use_label[sort_count.index(sorted(sort_count)[-2])], use_label[sort_count.index(sorted(sort_count)[-3])],
        input_number_label[sort_count.index(sorted(sort_count)[-1])], input_number_label[sort_count.index(sorted(sort_count)[-1])],
        input_number_label[sort_count.index(sorted(sort_count)[-1])], input_number_label[sort_count.index(sorted(sort_count)[-1])],
        input_number_label[sort_count.index(sorted(sort_count)[-2])], input_number_label[sort_count.index(sorted(sort_count)[-2])],
        input_number_label[sort_count.index(sorted(sort_count)[-2])], input_number_label[sort_count.index(sorted(sort_count)[-2])],
        input_number_label[sort_count.index(sorted(sort_count)[-3])], input_number_label[sort_count.index(sorted(sort_count)[-3])],
        input_number_label[sort_count.index(sorted(sort_count)[-3])], input_number_label[sort_count.index(sorted(sort_count)[-3])])
        cursor.execute(sql1)
        data = cursor.fetchall()
        num = len(data)
        print('标签大于三个时的数据数量num', num)
        if num < 10:    # 标签数量大于3时，查询出来的数据小于10条，则选择最多的两个标签进行查询写入job_test.txt中
            # print(sorted(sort_count)[-1], sorted(sort_count)[-2])
            # print(use_label[sort_count.index(sorted(sort_count)[-1])], use_label[sort_count.index(sorted(sort_count)[-2])])
            print('num<10')
            create_tree_lab.append(input_number_label[sort_count.index(sorted(sort_count)[-1])])
            create_tree_lab.append(input_number_label[sort_count.index(sorted(sort_count)[-2])])
            create_tree_lab2.append(input_number_label[sort_count.index(sorted(sort_count)[-1])])
            create_tree_lab2.append(input_number_label[sort_count.index(sorted(sort_count)[-2])])
            sql3 = """select `%s`, `%s`,position_name from job_tech_demand where  (`%s` = '1' or `%s` = '2' or `%s` = '3' or `%s` ='4') and (`%s` = '1' or `%s` = '2' or `%s` = '3' or `%s` ='4')""" % (
            input_number_label[sort_count.index(sorted(sort_count)[-1])], input_number_label[sort_count.index(sorted(sort_count)[-2])],
            input_number_label[sort_count.index(sorted(sort_count)[-1])], input_number_label[sort_count.index(sorted(sort_count)[-1])],
            input_number_label[sort_count.index(sorted(sort_count)[-1])], input_number_label[sort_count.index(sorted(sort_count)[-1])],
            input_number_label[sort_count.index(sorted(sort_count)[-2])], input_number_label[sort_count.index(sorted(sort_count)[-2])],
            input_number_label[sort_count.index(sorted(sort_count)[-2])], input_number_label[sort_count.index(sorted(sort_count)[-2])])
            cursor.execute(sql3)
            data3 = cursor.fetchall()
            num3 = len(data3)
            with open('F:\\untitled\decision_tree\job_test.txt', "w+") as file3:
                for j in range(num3):
                    file3.write(str(data3[j])+'\n')
            file3.close()

            create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-1])])
            create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-2])])


        else:   # 数量大于等于10条时，直接写入job_test.txt中
            create_tree_lab.append(input_number_label[sort_count.index(sorted(sort_count)[-1])])
            create_tree_lab.append(input_number_label[sort_count.index(sorted(sort_count)[-2])])
            create_tree_lab.append(input_number_label[sort_count.index(sorted(sort_count)[-3])])
            create_tree_lab2.append(input_number_label[sort_count.index(sorted(sort_count)[-1])])
            create_tree_lab2.append(input_number_label[sort_count.index(sorted(sort_count)[-2])])
            create_tree_lab2.append(input_number_label[sort_count.index(sorted(sort_count)[-3])])


            with open('F:\\untitled\decision_tree\job_test.txt', "w+") as file:
                for m in range(num):
                    file.write(str(data[m])+'\n')
            file.close()

            create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-1])])
            create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-2])])
            create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-3])])


    else:   # 标签数量等于2时，且至少为2
        print('标签大于2时：')
        print('input_number_label[0]', input_number_label[0])
        print('input_number_label[1]', input_number_label[1])
        create_tree_lab.append(input_number_label[0])
        create_tree_lab.append(input_number_label[1])
        create_tree_lab2.append(input_number_label[0])
        create_tree_lab2.append(input_number_label[1])
        sql2 = """select `%s`, `%s`,position_name from job_tech_demand where  (`%s` = '1' or `%s` = '2' or `%s` = '3' or `%s` ='4') and (`%s` = '1' or `%s` = '2' or `%s` = '3' or `%s` ='4')""" % (
        input_number_label[0], input_number_label[1],
        input_number_label[0], input_number_label[0],
        input_number_label[0], input_number_label[0],
        input_number_label[1], input_number_label[1],
        input_number_label[1], input_number_label[1])
        cursor.execute(sql2)
        data2 = cursor.fetchall()
        num2 = len(data2)
        with open('F:\\untitled\decision_tree\job_test.txt', "w+") as file2:
            for key in range(num2):
                file2.write(str(data2[key])+'\n')
        file2.close()
        print('use_label_value', use_label_value[0])
        print('use_label_value', use_label_value[1])
        create_tree_lab_value.append(use_label_value[0])
        create_tree_lab_value.append(use_label_value[1])



# 写入job_text.txt数据
num_label(use_label)

f = open(r'job_test.txt')

listWm2 = [inst.replace("'", '').replace('(', '').replace(')', '').strip().split(',') for inst in f.readlines()]

# 取出异常数据
for err in listWm2:
    if len(err) < len(listWm2[0]):
        listWm2.remove(err)
        print("异常数据为：", err)
Trees = trees.createTree(listWm2, create_tree_lab)

print("决策树：")
print(json.dumps(Trees, ensure_ascii=False))


# 决策树数据预测

# 写入再读出，只是为了转换数据格式
print('create_tree_lab_value', create_tree_lab_value)
with open('F:\\untitled\decision_tree\job_tree.txt', "w+") as fil:
    fil.write('(')
    for use in range(len(create_tree_lab_value)):
        fil.write("'"+create_tree_lab_value[use]+"',")
    fil.write(')')
    fil.write('\n')
fil.close()

ft = open(r'job_tree.txt')
listWmsss = [inst.replace("'", '').replace('(', '').replace(')', '').strip().split(',') for inst in ft.readlines()]
print(listWmsss)
testClass = trees.classifyAll(Trees, create_tree_lab2, listWmsss)
position_name = (json.dumps(testClass, ensure_ascii=False)).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

print(len(position_name))

import codecs

if len(position_name) == 0:
    f = codecs.open(r'job_test.txt')
    line = f.readline()
    list1 = []
    while line:
        a = line.split()
        b = a[-1]   # 读取最后一列岗位名称
        list1.append(b)
        line = f.readline()
    f.close()
    result = []
    for i in range(len(list1)):
        s = list1[i].replace(')', '').replace('"', '').replace("'", '').replace(',', '')
        result.append(s)
    print(result)

    list_unique = list(result)
    print('list_unique', list_unique)

    result = []
    for i in list_unique:
        if len(i) > 0:
            result.append(i)
    sort_result = Counter(result)
    end_result = sort_result.most_common(len(sort_result))
    result = []
    if len(end_result) > 5:
        for i in range(5):
           result.append(end_result[i][0])
    else:
        for i in range(len(end_result)):
           result.append(end_result[i][0])
    print(result)
else:
    print('根据您的条件，适合您的岗位是：', position_name)

