# -*- coding: cp936 -*-
import trees
import json
import pymysql
from collections import Counter
import pandas
import os
import sys
path = os.getcwd().replace("\\","/")
#path = path+"/target/classes/algorithm/decision_tree"
# ��ȡ�������ݵı�ǩ

if __name__ == '__main__':
    use_label = []
    use_label_value = []
    temp_name = sys.argv[1].split(",")
    temp_value = list(sys.argv[2])

    for i in range(len(temp_value)):
        if temp_value[i] != '0':
            use_label.append(temp_name[i])
            use_label_value.append(temp_value[i])


    # д�����ñ�ǩ
    with open(path+'/job_predict.txt', "w+") as fil:
        for use in range(len(use_label)):
            fil.write(use_label[use]+'  ')
            # use_label_value[use]
        fil.write('\n')
    fil.close()
    # д������
    with open(path+'/job_predict.txt', "a+") as fil2:
        for use_value in range(len(use_label_value)):
            fil2.write(use_label_value[use_value]+' ')
    fil.close()

    # ����MySQL���ݿ�
    conn = pymysql.connect(host='121.36.44.148', user='root', password='83ec64005ba39e58', db='recruitment', charset='utf8')
    cursor = pymysql.cursors.SSCursor(conn)

    # ��ȡ�ĸ�����ǩ�����ݿ��е�����ͳ��
    sort_count = []
    for k in use_label:
        sql = """select count(*) from job_tech_demand where `%s` = '1' or `%s` = '2' or `%s` = '3' or `%s` ='4'""" %(k, k, k, k)
        cursor.execute(sql)
        count_num = cursor.fetchall()
        # count_num_link = str(count_num[0][0])+str(k)
        sort_count.append(count_num[0][0])

    # �Ա�ǩ����ͳ�Ƶ�����
    # print(sorted(sort_count))

    # ����ǩ�������ڵ���3ʱ��ѡȡ��������������С��3ʱ����Ϊ2ʱ����ȫ��ѡȡ��Ҳ����˵�����������������������ݿ���л�ȡ����д������ļ��С�


    # �����������õı�ǩ
    create_tree_lab = []
    create_tree_lab2 = []
    create_tree_lab_value = []
    def num_label(input_number_label):
        if len(input_number_label) >= 3:    # ��ǩ�������ڵ���3ʱ
            # print(sorted(sort_count)[-1], sorted(sort_count)[-2], sorted(sort_count)[-3])
            # print(input_number_label[sort_count.index(sorted(sort_count)[-1])],input_number_label[sort_count.index(sorted(sort_count)[-2])],input_number_label[sort_count.index(sorted(sort_count)[-3])])
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
            # print('��ǩ��������ʱ����������num', num)
            if num < 10:    # ��ǩ��������3ʱ����ѯ����������С��10������ѡ������������ǩ���в�ѯд��job_test.txt��
                # print(sorted(sort_count)[-1], sorted(sort_count)[-2])
                # print(use_label[sort_count.index(sorted(sort_count)[-1])], use_label[sort_count.index(sorted(sort_count)[-2])])
                # print('num<10')
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
                with open(path+'/job_test.txt', "w+") as file3:
                    for j in range(num3):
                        file3.write(str(data3[j])+'\n')
                file3.close()

                create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-1])])
                create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-2])])


            else:   # �������ڵ���10��ʱ��ֱ��д��job_test.txt��
                create_tree_lab.append(input_number_label[sort_count.index(sorted(sort_count)[-1])])
                create_tree_lab.append(input_number_label[sort_count.index(sorted(sort_count)[-2])])
                create_tree_lab.append(input_number_label[sort_count.index(sorted(sort_count)[-3])])
                create_tree_lab2.append(input_number_label[sort_count.index(sorted(sort_count)[-1])])
                create_tree_lab2.append(input_number_label[sort_count.index(sorted(sort_count)[-2])])
                create_tree_lab2.append(input_number_label[sort_count.index(sorted(sort_count)[-3])])


                with open(path+'/job_test.txt', "w+") as file:
                    for m in range(num):
                        file.write(str(data[m])+'\n')
                file.close()

                create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-1])])
                create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-2])])
                create_tree_lab_value.append(use_label_value[sort_count.index(sorted(sort_count)[-3])])


        else:   # ��ǩ��������2ʱ��������Ϊ2
            # print('��ǩ����2ʱ��')
            # print('input_number_label[0]', input_number_label[0])
            # print('input_number_label[1]', input_number_label[1])
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
            with open(path+'/job_test.txt', "w+") as file2:
                for key in range(num2):
                    file2.write(str(data2[key])+'\n')
            file2.close()
            # print('use_label_value', use_label_value[0])
            # print('use_label_value', use_label_value[1])
            create_tree_lab_value.append(use_label_value[0])
            create_tree_lab_value.append(use_label_value[1])



    # д��job_text.txt����
    num_label(use_label)

    f = open(path+'/job_test.txt')

    listWm2 = [inst.replace("'", '').replace('(', '').replace(')', '').strip().split(',') for inst in f.readlines()]

    # ȡ���쳣����
    for err in listWm2:
        if len(err) < len(listWm2[0]):
            listWm2.remove(err)
            # print("�쳣����Ϊ��", err)
    Trees = trees.createTree(listWm2, create_tree_lab)

    # print("��������")
    # print(json.dumps(Trees, ensure_ascii=False))


    # ����������Ԥ��

    # д���ٶ�����ֻ��Ϊ��ת�����ݸ�ʽ
    # print('create_tree_lab_value', create_tree_lab_value)
    with open(path+'/job_tree.txt', "w+") as fil:
        fil.write('(')
        for use in range(len(create_tree_lab_value)):
            fil.write("'"+create_tree_lab_value[use]+"',")
        fil.write(')')
        fil.write('\n')
    fil.close()

    ft = open(path+'/job_tree.txt')
    listWmsss = [inst.replace("'", '').replace('(', '').replace(')', '').strip().split(',') for inst in ft.readlines()]
    # print(listWmsss)
    testClass = trees.classifyAll(Trees, create_tree_lab2, listWmsss)
    position_name = (json.dumps(testClass, ensure_ascii=False)).replace('[', '').replace(']', '').replace('"', '').replace("'", '')

    # print(len(position_name))

    import codecs

    if len(position_name) == 0:
        f = codecs.open(path+'/job_test.txt')
        line = f.readline()
        list1 = []
        while line:
            a = line.split()
            b = a[-1]   # ��ȡ���һ�и�λ����
            list1.append(b)
            line = f.readline()
        f.close()
        result = []
        for i in range(len(list1)):
            s = list1[i].replace(')', '').replace('"', '').replace("'", '').replace(',', '')
            result.append(s)
        # print(result)

        list_unique = list(result)
        # print(list_unique)

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
        print('���������������ʺ����ĸ�λ�ǣ�', position_name)

