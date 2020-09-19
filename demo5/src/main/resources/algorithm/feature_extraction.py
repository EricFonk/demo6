"""
@author:MIAO
@file: feature_extraction.py
@time: 2020/07/23
"""
from collections import defaultdict
import csv
import re
import math
import operator
import pandas as pd
#首先导入PyMySQL库
import pymysql
#连接数据库，创建连接对象connection
DBHOST='121.36.44.148'#host属性
DBUSER='root' #用户名
DBPASS='83ec64005ba39e58'#此处填登录数据库的密码
DBNAME='recruitment' #数据库名

import os

path = os.getcwd()
path = os.getcwd().replace("\\","/")
path = path+"/target/classes/algorithm"

class FeatureExtraction():
    def __init__(self):
        pass
    def get_data(self):
        try:
            connection = pymysql.connect(DBHOST, DBUSER, DBPASS, DBNAME)
            print("数据库连接成功!")
            sql = "select * from job_segmentation"
            print("数据查询成功！")
            #转换为DataFrame格式
            return pd.read_sql(sql, connection)
        except pymysql.Error as e:
            print("数据查询失败:" + str(e))
            connection.rollback()
        connection.close()
    def segmentation_2(self):
        '''
        对数据再度分词
        :return:
        '''
        data = self.get_data()
        x = [1,2,3,4,6,7,8]
        data.drop(data.columns[x], axis=1, inplace=True)
        data.to_csv(path+'\\data\JobOriginal.csv',encoding="utf-8")
        print(data)
        with open(path+'\\data\JobOriginal.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            print(reader)
            new_reader = list(reader)
        print(new_reader)
        # 分词并存进JobFenCi.csv文件
        f = open(path+'\\data\JobFenCi.csv', 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(["title", "content"])
        for i in range(1, len(new_reader)):
            new_reader_split = new_reader[i][2].split('/')
            print(new_reader_split)
            for j in range(len(new_reader_split)):
                if "精通" in new_reader_split[j]:
                    s1 = "精通" + new_reader_split[j].replace("精通", "")
                    if (new_reader[i][1] != ''):
                        csv_writer.writerow([new_reader[i][1], s1])
                elif "熟悉" in new_reader_split[j]:
                    s2 = "熟悉" +  new_reader_split[j].replace("熟悉", "")
                    print(new_reader[i][0], new_reader[i][1], s2)
                    csv_writer.writerow([new_reader[i][1],s2])
                elif "了解" in new_reader_split[j]:
                    s3 = "了解" +  new_reader_split[j].replace("了解", "")
                    print(new_reader[i][0], new_reader[i][1], s3)
                    csv_writer.writerow([new_reader[i][1],s3])
                elif "熟练" in new_reader_split[j]:
                    if "熟练掌握" in new_reader_split[j]:
                        s4 = "熟练掌握" + new_reader_split[j].replace("熟练掌握", "")
                        print(new_reader[i][0], new_reader[i][1], s4)
                        csv_writer.writerow([new_reader[i][1],s4])
                    else:
                        s5 = "熟练掌握" +  new_reader_split[j].replace("熟练", "").replace("掌握", "")
                        print(new_reader[i][0], new_reader[i][1], s5)
                        csv_writer.writerow([new_reader[i][1],s5])
                elif "掌握" in new_reader_split[j]:
                    if "熟练掌握" in new_reader_split[j]:
                        s6 = "熟练掌握" +  new_reader_split[j].replace("熟练掌握", "")
                        print(new_reader[i][0], new_reader[i][1], s6)
                        csv_writer.writerow([new_reader[i][1],s6])
                    else:
                        s7 = "熟练掌握" +  new_reader_split[j].replace("熟练", "").replace("掌握", "")
                        print(new_reader[i][0], new_reader[i][1], s7)
                        csv_writer.writerow([new_reader[i][1],s7])
        f.close()
    def transfer_csv(self):
        # 获取数据文件
        with open(path+'\data\JobFenCi.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            new_reader = list(reader)
        # 分词Skills并存进JobFenCiSkills.csv文件
        f = open(path+'\\data\JobFenCiSkills.csv', 'w', encoding='utf-8', newline='')
        csv_writer = csv.writer(f)
        csv_writer.writerow(["skills"])
        for i in range(1, len(new_reader)):
            # print(new_reader[i][2])
            new_reader_split = new_reader[i][1].split('/')
            print(new_reader_split[1])
            csv_writer.writerow([new_reader_split[1]])
        f.close()
    def select_nature(self):
        # 获取数据文件
        with open(path+'\\data\JobFenCiSkills.csv', encoding='utf-8') as f:
            reader = csv.reader(f)
            new_reader = list(reader)
        s_nature = []
        # 替换并保存到JobNature.csv文件中

        for i in range(1, len(new_reader)):  # 技能分词后的文件

            sign = re.compile(r'[0-9a-zA-Z.#]+')
            compare_sign = sign.findall(new_reader[i][0])

            # upper_compare_sign = compare_sign[i][0].upper()
            if len(compare_sign) != 0:
                # print(compare_sign[0])

                s_nature.append(compare_sign[0].lower())
        print(s_nature)
        f.close()

        result_count = pd.value_counts(s_nature)
        print(result_count)

        # 统计词频后存入JobLastSelectNatures.csv文件中
        # ft = open('data/JobLastSelectNatures.csv', 'w', encoding='utf-8', newline='')
        # csv_writer = csv.writer(ft)
        a = pd.DataFrame(result_count)
        a.to_csv(path+'\\data\JobLastSelectNatures.csv')
        # ft.close()
        # ft.close()
    def replaceFomat(self,text: str, word: str, n: int, reverse=False):
        '''对文本中的指定单词进行格式化的替换/替回
        Params:
        ---
        text
            要替换的文本
        word
            目标单词
        n
            目标单词的序号
        reverse
            是否进行替回
        Return:
        ---
        new_text
            替换后的文本
        '''
        # 构造【中间变量】
        new_text = text[:]
        fmt = "<{}>".format(n)
        # 替换
        if reverse is False:
            new_text = new_text.replace(word, fmt)  # 格式化替换
            return new_text
        # 替回
        elif reverse is True:
            new_text = new_text.replace(fmt, word)  # 去格式化替换
            return new_text
        # 要求非法，引发异常
        else:
            raise TypeError

    def replaceMulti(self,text: str, olds: list, news: list):
        '''一次替换多组字符串
        Params:
        ---
        text
            要替换的文本
        olds
            旧字符串列表
        news
            新字符串列表
        Return:
        ---
        new_text: str
            替换后的文本
        '''
        if len(olds) != len(news):
            raise IndexError
        else:
            new_text = text[:]
            # 格式化替换
            i = 0  # 单词计数器
            for word in olds:
                i += 1
                new_text = self.replaceFomat(new_text, word, i)
            # 去格式化替回
            i = 0  # 归零
            for word in news:
                i += 1
                new_text = self.replaceFomat(new_text, word, i, True)
            # 返回替换好的文本
            return new_text

    def get_alpha(self,s):
        print(s)
        result = ''.join(re.split(r'[^A-Za-z0-9]', s))
        result = result.lower()
        # print(result)
        return result
    def transfer_txt(self,data):
        file = open(path+'\\data\job_pos.txt','w',encoding="utf-8")
        length = len(data["content"])
        content_list =[]
        for i in range(0, length):
            content = data["content"][i]
            content_list.append(content.split('/'))
        for i in range(0,len(content_list)):
            result = ""
            for j in range(0,len(content_list[i])):
                olds = ["精通", "熟练","掌握","了解","熟悉","使用","语言","运用","应用","至少",
                        "方法","技术","一种","和","以上","技巧","工具","相关","开发","流程",
                        "等","进行","编程","其","一门","实践","经验","常用的","常用","和",
                        "基本的","程序设计","思想","主流","的","设计","算法","系统","原理","框架",
                        "知识","编写","模式","常见","操作","机制","管理","与","及","构建",
                        "项目","各种","模块化","生产","调试","发展","多种","工程化","产品","处理",
                        "分析","优化","或","基本","原则","大型",'过程','资料',"用户","表",
                        "性能","阅读","各类","平台","说明","行业","业务","基础","概念","理论",
                        "接口","软件程序","自动化","最新","体系","结构","实现","各项","以","用例",
                        "配置","一些","当前","实施","流行","开源","搭建","需求获取","模型","调优",
                        "有关","非","客户需求","运动控制","正则达式","能力","工程","特性","实时","各自",
                        "优缺点","设施中","第三方","大容量","地页面","步进电机","软件全","书写","面向对象软件","测试测试",
                        "需求规划","上位机","有限元","多任务","各","软件学","webhtml","stm32","uefi","can",
                        "plc","winform","uart","wpf","mssql","kafka","fpga","iar","cjava","x86"
                        ]

                news = ["","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","","",
                        "","","","","","","","","",""
                        ]
                result = self.replaceMulti(content_list[i][j], olds, news)
                pattern = re.compile('[A-Za-z]')
                match = pattern.findall(result)
                print(match)
                if match != []:
                    result = self.get_alpha(result)
                if(result != '' and len(result) >= 3 and len(result) <= 7 or result == 'c'):
                    file.write(result+"\n")
        file.close()
    def Read_list(self,filename):
        file1 = open(path+'\\data\job_pos.txt', "r", encoding ="utf-8")
        list_row =file1.readlines()
        list_source = []
        for i in range(len(list_row)):
            column_list = list_row[i].strip().split("\t")  # 每一行split后是一个列表
            list_source.append(column_list)
            # print(len(list_row)) # 输出总共多少条数据
            # 在末尾追加到list_source
        file1.close()
        return list_source
    #保存二维列表到文件
    def Save_list(self,list1,filename):
        file2 = open(filename + '.txt', 'w')
        for i in range(len(list1)):
            for j in range(len(list1[i])):
                file2.write(str(list1[i][j]))              # write函数不能写int类型的参数，所以使用str()转化
                file2.write('\t')                          # 相当于Tab一下，换一个单元格
            file2.write('\n')
        print(file2)# 写完一行立马换行
        file2.close()
    
    #加载数据集的函数
    #postingList：存放词条列表
    #classVec：存放每个词条的所属类别
    def loadDataSet(self):
        dataset = self.Read_list("job_pos")
    
        classVec = [0, 1]  # 类别标签向量，1代表好，0代表不好
        return dataset, classVec
    
    def feature_select(self,list_words):
        # 总词频统计
        doc_frequency = defaultdict(int)
        for word_list in list_words:
            for i in word_list:
                doc_frequency[i] += 1
    
        # 计算每个词的TF值
        word_tf = {}  # 存储没个词的tf值
        for i in doc_frequency:
            word_tf[i] = doc_frequency[i] / sum(doc_frequency.values())
    
        # 计算每个词的IDF值
        doc_num = len(list_words)
        word_idf = {}  # 存储每个词的idf值
        word_doc = defaultdict(int)  # 存储包含该词的文档数
        for i in doc_frequency:
            for j in list_words:
                if i in j:
                    word_doc[i] += 1
        for i in doc_frequency:
            word_idf[i] = math.log(doc_num / (word_doc[i] + 1))
    
        # 计算每个词的TF*IDF的值
        word_tf_idf = {}
        for i in doc_frequency:
            word_tf_idf[i] = word_tf[i] * word_idf[i]
    
        # 对字典按值由大到小排序
        dict_feature_select = sorted(word_tf_idf.items(), key=operator.itemgetter(1), reverse=True)
        return dict_feature_select
   
