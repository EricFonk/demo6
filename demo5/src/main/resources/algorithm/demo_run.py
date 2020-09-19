#!usr/bin/env python
# -*- coding:utf-8 _*-
"""
@author:MIAO
@file: demo_run.py
@time: 2020/07/23
"""

from sqlalchemy.types import VARCHAR, Float, Integer
from data_reprocessing import DataClean
from data_segmentation import DataSegmentation
from feature_extraction import FeatureExtraction
from create_table import CreateTable
from sqlalchemy import create_engine
import time
import trees
import json
import csv
import pymysql
import pandas as pd
import os

path = os.getcwd()
path = os.getcwd().replace("\\","/")
path = path+"/target/classes/algorithm"
def mapping_df_types(df):
    '''
    将pandas.DataFrame中列名和预指定的类型映射起来
    :param df:
    :return:
    '''
    dtypedict = {}
    for i, j in zip(df.columns, df.dtypes):
        print(i)
        if "object" in str(j) and i in ['title', 'place', 'experience', 'education', 'company', 'size',
                                        'kind',"skillname"]:
            dtypedict.update({i: VARCHAR(length=255)})
        if "int" in str(j) and i in ['id','salary','skillId']:
            dtypedict.update({i: Integer()})
    return dtypedict
def data_clean():
    '''
    对数据进行预处理和清洗
    :return:
    '''
    opt = DataClean()
    data = opt.clean_operation()
    # 建立连接，username替换为用户名，passwd替换为密码，test替换为数据库名
    conn = create_engine('mysql+pymysql://root:83ec64005ba39e58@121.36.44.148:3306/recruitment', encoding='utf8')
    dtypedict = mapping_df_types(data)
    # 写入数据，table_name为表名，‘replace’表示如果同名表存在就替换掉
    data.to_sql(name='job_preprocessing', con=conn, if_exists='replace', index=False, dtype=dtypedict)
    return data
def data_segmentation(data):
    '''
    对数据进行中文分词
    :param data:
    :return:
    '''
    seg = DataSegmentation()
    seg_result = seg.segmentation(data)
    # 建立连接，username替换为用户名，passwd替换为密码，test替换为数据库名
    conn = create_engine('mysql+pymysql://root:83ec64005ba39e58@121.36.44.148:3306/recruitment', encoding='utf8')
    dtypedict = mapping_df_types(seg_result)
    # 写入数据，table_name为表名，‘replace’表示如果同名表存在就替换掉
    # print(seg_result['content'][2]=='')
    seg_result = seg_result.drop(seg_result[seg_result['content']== ''].index)
    seg_result.to_sql(name='job_segmentation', con=conn, index=False,if_exists='replace', dtype=dtypedict)
    return seg_result
def feature_extraction(data):
    '''
    对数据进行特征提取
    :return:
    '''
    feature_data = FeatureExtraction()
    feature_data.transfer_txt(data)
    data_list, label_list = feature_data.loadDataSet()  # 加载数据
    features = feature_data.feature_select(data_list)  # 所有词的TF-IDF值
    data = open(path+"\\data\aut.txt", 'w', encoding="utf-8")
    data2 = open(path+"\\data\aut2.txt", 'w', encoding="utf-8")
    for i in range(len(features)):
        # count = count + 1
        # print(count)
        if features[i][1] > 0.0006:
            # print(features[i][1])
            data2.write(features[i][0] + " " + str(features[i][1] * 100) + "%" + "\n")
            data.write(str(i+1)+" "+features[i][0] + "\n")
            # data3.write(features[i][0] + "\n")
            # print(features[i][0], features[i][1])
    data.close()
    data2.close()
# def set_labels():
#     data = open("data/labels.txt", 'w', encoding="utf-8")
#     data1 = open("data/labels1.txt", 'w', encoding="utf-8")
#     with open('data/JobLastSelectNatures.csv', encoding='utf-8') as f:
#         reader = csv.reader(f)
#         new_reader = list(reader)
#     # 选择技能
#     skills = []
#     # ft = open('F:/untitled/test/jobHandle/jobData/JobNatures.csv', 'w', encoding='utf-8', newline='')
#     # csv_writer = csv.writer(ft)
#     count = 0
#     for i in range(1, len(new_reader)):
#         print(new_reader[i][0])
#         count_num = int(new_reader[i][1])
#         if count_num > 5:
#             if (len(new_reader[i][0]) > 2 or new_reader[i][0] in['c','c#','ui']):
#                 count += 1
#                 data.write(new_reader[i][0]+"\n")
#                 data1.write(str(count) + " " + new_reader[i][0] + "\n")
#                 skills.append(new_reader[i][0])
#             # csv_writer.writerow(new_reader[i][0])
#     print(skills)
def creat_table():
    '''
    创建算法所需要的熟练度-技能-职位的映射表
    :return:
    '''
    creat_data = CreateTable()
    # table_data = pd.read_csv('data/JobFenCi.csv',encoding="utf-8")
    # print(table_data)
    creat_data.transfer_txt(creat_data.get_data())
    labels = creat_data.get_labels()
    # labels = ['C', 'Spring', 'mysql', 'Oracle', 'Linux', 'TCP', 'HTML', 'C#', 'Android', 'js', 'C++', '分布式', '数据库', '设计模式', 'Redis', 'tomcat', 'python', '多线程', '软件开发', 'php', '网络编程', 'hadoop', 'vue.js', 'web', '数据结构和算法', '.net', 'IO', 'Git', 'Jquery', '面向对象', 'JSP', 'Eclipse', 'OpenCV', 'MVC', 'SVN', 'J2EE', 'XML', 'shell', 'Maven', 'http', '存储过程', 'React', 'struts', 'Photoshop', 'SpringBoot', '微服务', '单片机', 'SpringMVC', 'QT', 'UML', 'docker', 'Objective-C', 'Axure', 'ARM', '页面架构和布局', 'nginx', 'CSS', 'Ajax', '大数据', 'UART', '框架', 'SAP', 'Matlab', 'NoSQL', 'SpringCloud', 'VS', 'OpenGL', '前端', '小程序', 'Apache', 'MongoDB', 'Dubbo', 'bootstrap', 'SSH', '软件技术文档的编写', '办公软件', 'socket', '操作系统', 'IAR', '计算机网络', '阅读英文技术文档', '图像处理', 'CI', '机器视觉', '机器学习', '缓存技术', 'MS', '消息中间间', 'VC', 'SPI', '一种编程语言', 'Unity', '软件测试流程', 'memcached', 'Xcode', '示波器', 'ST', 'VB', '常用算法', 'MQ', 'SOA', '网络协议', 'I2C', 'sqlserver', '深度学习', '软件工程理论', 'word', '正则表达式', 'Labview', '嵌入式', 'ARM架构', 'CAN', '汇编语言', 'Swift', '项目管理', '网络通信', 'LAMP', 'RabbitMQ', '软件架构', 'Kafka', 'Servlet', 'Jenkins', 'UI', 'JVM', 'USB', 'lua', '计算机', 'AngularJS', 'Kubernetes', 'DSP', 'CA', '一门脚本语言', '浏览器兼容性', 'Tensorflow', '前后端分离', '开发工具', '负载均衡', '数字图像处理', '三层架构', 'OOP', 'Django', 'Spark', 'WinForm', 'GO', '模拟电路', '计算机图形学', '串口通讯', 'angular', 'ROS', 'PC', 'STM8', 'Visio', 'VisualStudio', '网页抓取', '内存管理', '网络架构', '数据分析', '密码学', '以太网', '软件设计', 'GIS', 'node', '并发编程', 'MTK', '网络基础知识', 'STM32', '网络设备', '移动网络通信机制', '需求调研', 'AWS', '网站', 'Framework', 'ETL', '数字信号', 'OpenStack', 'VMware', 'PowerDesigner', 'ElasticSearch', '软件测试', '物联网技术', 'Golang', 'Mybatis', 'zookeeper', 'halcon', 'Hibernate', 'MES', 'keil', '移动端开发', 'WCF', 'TCPIP协议', '业务抽象数据模型设计', '敏捷开发流程', 'iOS', 'Slite', 'GCC', 'FreeRTOS', '响应式设计', '交换机', 'JSDK', '底层原理', 'RS232', '3D图形学', 'AutoCAD', '自然语言处理', 'TI', 'cocos', 'ActiveMQ', 'CSR', 'SPSS', 'Internet基本协议', 'Netty', 'Ext', '盒模型', 'RS485', 'ADO.NET', 'ffmpeg', 'LCD', 'Asp.net', 'jboss', 'EXCEL', '数据仓库', '项目', 'Postgresql', 'APP', 'Sketch', '视图', '云平台', 'makefile', '微信平台接口', 'laravel', 'wifi', 'CUDA', '常用的第三方库', 'JSON', '人工智能', '容器技术', 'UCOS', 'Unity3D', 'Swoole', '类库', 'MCU', '接口', 'idea', 'T-SQL', '版本管理', 'JDK', 'VHDL', '企业管理', '浏览器渲染原理', '模块的业务流程', 'EF', 'ELK', '自动化运维', '质量管理体系', 'JDBC', 'w3c', 'flex', '图表及函数功能', 'RPC', '常用的电子元器件', 'Kotlin', 'NDK', '编写各类技术文档', '微信公众号开发', 'openlayers', 'WPF', 'MVVM', 'sass', '用户交互设计', '蓝牙', 'Devops', '共识算法或一致性算法', '电力系统', '国内主流机型的特点', 'CRM', 'Shader', 'TypeScript', 'Hive', '各种硬件接口', '研发流程', '3D几何', '驱动开发', '视频编解码', 'UBOOT', 'OS', 'JNI', 'CCD', 'BLE', 'ONVIF', '无线网络', '制图软件', 'Scrum', 'grunt', '监控系统', 'Perl', '互联网技术', '集成工具', 'K8S', 'TP', 'Echarts', '数理统计', 'MBD', 'STL', 'ERP', 'CMMI', '网络相关设备的配置技术', 'ES5', '反爬虫技术', 'RESIN', 'Hbase', 'CEF', 'OpenGLES', 'Yii', 'UE4', '爬虫技术', '3A统计值', 'VxWorks', 'JUnit', '总线协议', 'Dreamweaver', 'db2', '加密算法', 'UEFI', 'DirectX', '组件化开发', 'Bitcoin', '进程间通信', 'LoadRunner', 'gulp', 'Glide', 'RHEL', '控件开发', '产品发布流程', 'PID', '上位机编程', '事务控制及相关技术', 'datasheet', '信息安全', 'QML', 'FPGA', '各类电子测试仪表', '交互设计', 'PLC', 'restful', 'MFC', '虚拟化技术', 'npm', 'ES6', 'lnmp']
    data = creat_data.get_pos()
    creat_data.creat_result(data,labels)
def get_labels2():
    with open(path+'\\data\labels.txt', 'r', encoding="utf-8") as f:
        content = f.read().splitlines()
    labels = []
    for i in range(len(content)):
        labels.append(content[i])
    return labels
def get_labels():
    '''
    获取属性
    :return:
    '''
    with open(path+'\\data\labels1.txt', 'r', encoding="utf-8") as f:
        content = f.read().splitlines()
    labels = []
    for i in range(len(content)):
        labels.append(content[i].split(" "))
    # 建立连接，username替换为用户名，passwd替换为密码，test替换为数据库名
    conn = create_engine('mysql+pymysql://root:83ec64005ba39e58@121.36.44.148:3306/recruitment', encoding='utf8')
    data_labels = pd.DataFrame(labels,columns=["skillId","skillname"])
    dtypedict = mapping_df_types(data_labels)
    data_labels.index += 1
    # 写入数据，table_name为表名，‘replace’表示如果同名表存在就替换掉
    data_labels.to_sql(name='job_labels', con=conn, if_exists='replace', index=False,dtype=dtypedict)
    with open(path+'\\data\aut2.txt', 'r', encoding="utf-8") as f:
        content = f.read().splitlines()
    labels2 = []
    for i in range(len(content)):
        labels2.append(content[i].split(" "))
    print(labels2)
    # 建立连接，username替换为用户名，passwd替换为密码，test替换为数据库名
    conn = create_engine('mysql+pymysql://root:83ec64005ba39e58@121.36.44.148:3306/recruitment', encoding='utf8')
    data_labels2 = pd.DataFrame(labels2,columns=["labels","weight"])
    dtypedict = mapping_df_types(data_labels2)
    # 写入数据，table_name为表名，‘replace’表示如果同名表存在就替换掉
    data_labels2.to_sql(name='job_labels_weight', con=conn, if_exists='replace', index=False, dtype=dtypedict)



def job_tree():
    '''
    重新建进行预测的决策树
    :param labels:
    :return:
    '''
    fr = open(r'data/job_test.csv', encoding='UTF-8')

    listWm = [inst.strip().split('\t') for inst in fr.readlines()]
    labels = get_labels2()
    Trees = trees.createTree(listWm, labels)
    print("决策树：")
    print(json.dumps(Trees, ensure_ascii=False))
    #保存树
    fileName = r'data/tree.txt'
    trees.storeTree(Trees, fileName)

if __name__ == "__main__":
    time_start = time.time()
    #对数据进行预处理和清洗
    # data = data_clean()
    # print(data)
    #对数据进行分词
    # seg = DataSegmentation()
    # result=data_segmentation(seg.get_data())
    # print(result)
    #对数据进行特征提取
    # result = FeatureExtraction()
    # result.segmentation_2()
    # result.transfer_csv()
    # result.select_nature()
    # set_labels()
    # result = resu lt.get_data()
    # feature_extraction(result)
    # 更新技能属性表和特征提取之后的表
    # get_labels()
    #建立决策树所需的表
    # creat_table()
    #决策树
    job_tree()
    time_end = time.time()
    print('程序所花费时间为:', time_end - time_start, 's')
