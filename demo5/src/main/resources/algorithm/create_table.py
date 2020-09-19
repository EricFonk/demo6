#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:MIAO
@file: create_table.py
@time: 2020/07/25
"""
import numpy as np
import pandas as pd
import re
import random
#首先导入PyMySQL库
import pymysql
#连接数据库，创建连接对象connection
import os

path = os.getcwd()
DBHOST='121.36.44.148'#host属性
DBUSER='root' #用户名
DBPASS='83ec64005ba39e58'#此处填登录数据库的密码
DBNAME='recruitment' #数据库名

class CreateTable():
    def get_data(self):
        try:
            connection = pymysql.connect(DBHOST, DBUSER, DBPASS, DBNAME)
            print("数据库连接成功!")
            sql = "select * from job_segmentation"
            print("数据查询成功！")
            # 转换为DataFrame格式
            return pd.read_sql(sql, connection)
        except pymysql.Error as e:
            print("数据查询失败:" + str(e))
            connection.rollback()
        connection.close()

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
        # print(s)
        result = ''.join(re.split(r'[^A-Za-z0-9]', s))
        result = result.lower()
        # print(result)
        return result

    def transfer_txt(self,data):
        file = open(path+"\\data\job_pos2.txt", 'w', encoding="utf-8")
        length = len(data["content"])
        position = data["title"]
        content_list = []
        for i in range(0, length):
            content = data["content"][i]
            # if (len(content.split('/')) > 12):
            #     content_list.append(content.split('/'))
            content_list.append(content.split('/'))
        for i in range(0, len(content_list)):
            result = ""
            for j in range(0, len(content_list[i])):
                olds = ["使用", "语言", "运用", "应用", "至少",
                        "方法", "技术", "一种", "和", "以上", "技巧", "工具", "相关", "开发", "流程",
                        "等", "进行", "编程", "其", "一门", "实践", "经验", "常用的", "常用", "和",
                        "基本的", "程序设计", "思想", "主流", "的", "设计", "算法", "系统", "原理", "框架",
                        "知识", "编写", "模式", "常见", "操作", "机制", "管理", "与", "及", "构建",
                        "项目", "各种", "模块化", "生产", "调试", "发展", "多种", "工程化", "产品", "处理",
                        "分析", "优化", "或", "基本", "原则", "大型", '过程', '资料', "用户", "表",
                        "性能", "阅读", "各类", "平台", "说明", "行业", "业务", "基础", "概念", "理论",
                        "接口", "软件程序", "自动化", "最新", "体系", "结构", "实现", "各项", "以", "用例",
                        "配置", "一些", "当前", "实施", "流行", "开源", "搭建", "需求获取", "模型", "调优",
                        "有关", "非", "客户需求", "运动控制", "正则达式", "能力", "工程", "特性", "实时", "各自",
                        "优缺点", "设施中", "第三方", "大容量", "地页面", "步进电机", "软件全", "书写", "面向对象软件", "测试测试",
                        "需求规划", "上位机", "有限元", "多任务", "各", "软件学", "webhtml", "stm32", "uefi", "can",
                        "plc", "winform", "uart", "wpf", "mssql", "kafka", "fpga", "iar", "cjava", "x86"
                        ]

                news = ["", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", "", "", "", "", "", "",
                        "", "", "", "", ""
                        ]
                result = self.replaceMulti(content_list[i][j], olds, news)
                result = result.replace("熟练掌握", "1")
                result = result.replace("熟练", "1")
                result = result.replace("掌握", "1")
                result = result.replace("精通", "2")
                result = result.replace("熟悉", "3")
                result = result.replace("了解", "4")
                pattern = re.compile('[A-Za-z]')
                match = pattern.findall(result)

                # print(match)
                if match != []:
                    result = self.get_alpha(result)
                # print("进行了替换:%d" % len(result))
                if (result != '' and len(result) >= 3 and len(result) <= 7 or result.find('c') != -1):
                    file.write(result + " ")
            if (result != "" and len(result) >= 3 and len(result) <= 7 or result.find('c') != -1):
                file.write(position[i] + "\n")
        file.close()
    def get_labels(self):
        '''
        获取属性
        :return:
        '''
        with open(path+'\data\labels.txt', 'r', encoding="utf-8") as f:
            content = f.read().splitlines()
        labels = []
        for i in range(len(content)):
            labels.append(content[i])
        labels.append("position")
        return labels
    def get_pos(self):
        '''
        得到职位-熟练度-技能的列表
        :return:
        '''
        list1 = []
        with open(path+"\\data\job_pos2.txt", 'r', encoding="utf-8") as f:
            for line in f.readlines():
                linestr = line.strip()
                linestrlist = linestr.split(" ")
                list1.append(linestrlist)
        return list1
    def creat_result(self, data, labels):
        '''
        获取熟练度-技能-岗位的映射表
        :param data:
        :param labels:
        :return:
        '''
        dict_list = []
        for j in range(len(data)):
            dict_data = {}
            count = 0
            for k in range(len(data[j]) - 1):
                for i in labels:
                    # print(k.find(i))
                    if data[j][k].find(i) != -1:
                        dict_data[i] = data[j][k][0]
                        count += int(dict_data[i])
                    # if i in data[j][k]:
                    #     dict_data[i] = data[j][k][0]
                    #     count += int(dict_data[i])
                    else:
                        dict_data[i] = '0'
            print(data[j][k + 1])
            if (data[j][k+1].find('前端')) != -1 or \
                    bool(re.findall('vue',data[j][k+1] , flags=re.IGNORECASE))or\
                    bool(re.findall('html',data[j][k+1] , flags=re.IGNORECASE))or\
                    bool(re.findall('css',data[j][k+1] , flags=re.IGNORECASE))or\
                    bool(re.findall('javascript',data[j][k+1] , flags=re.IGNORECASE)):
                data[j][k+1] = '前端工程师'
            elif bool(re.findall('java',data[j][k+1] , flags=re.IGNORECASE)):
                data[j][k + 1] = 'java开发工程师'
            elif data[j][k+1].find('后端') != -1 or\
                    bool(re.findall('node',data[j][k+1] , flags=re.IGNORECASE)) or\
                    bool(re.findall('net',data[j][k+1] , flags=re.IGNORECASE)):
                data[j][k + 1] = '后端工程师'
            elif data[j][k+1].find('测试') != -1:
                data[j][k + 1] = '测试工程师'
            elif data[j][k+1].find('运维') != -1:
                data[j][k + 1] = '运维工程师'
            elif data[j][k+1].find('算法') != -1:
                data[j][k + 1] = '算法工程师'
            elif data[j][k+1].find('数据') != -1:
                data[j][k + 1] = '数据分析师'
            elif bool(re.findall('ios',data[j][k+1] , flags=re.IGNORECASE)) or \
                    bool(re.findall('Android',data[j][k+1] , flags=re.IGNORECASE))\
                    or data[j][k+1].find('移动') != -1:
                data[j][k + 1] = '移动开发工程师'
            elif bool(re.findall('c#',data[j][k+1] , flags=re.IGNORECASE)):
                data[j][k + 1] = 'C#语言开发工程师'
            elif bool(re.findall('c',data[j][k+1] , flags=re.IGNORECASE)):
                data[j][k + 1] = 'C语言开发工程师'
            elif bool(re.findall('python',data[j][k+1] , flags=re.IGNORECASE)):
                data[j][k + 1] = 'Python开发工程师'
            elif data[j][k + 1].find('嵌入式') != -1:
                data[j][k + 1] = '嵌入式开发工程师'
            elif data[j][k + 1].find('图像') != -1:
                data[j][k + 1] = '图像工程师'
            elif data[j][k + 1].find('数据库') != -1 or \
                bool(re.findall('sql',data[j][k+1] , flags=re.IGNORECASE)):
                data[j][k + 1] = '数据库工程师'
            elif data[j][k + 1].find('软件') != -1 or data[j][k + 1].find('系统') != -1:
                data[j][k + 1] = '软件开发工程师'
            print('修改后'+ data[j][k + 1])
            dict_data['position'] = data[j][k + 1]
            print(dict_data)
            if (count > 20):
                print("count",count)
            dict_list.append(dict_data)
        print(dict_list)
        arr = pd.DataFrame(dict_list)
        # print(arr)
        # print(arr.shape[1])

        # arr = arr.sample(n=300, random_state=random.randint(0,10), axis=0)
        arr = arr.sample(n=500, random_state=119, axis=0)
        arr_test = arr.drop('position', axis=1)
        arr_test = arr_test.sample(n=152, random_state=119, axis=0)
        #生成训练集
        arr.to_csv(path+"\\data\job_test.csv", sep="\t", header=False, index=False)
        #生成测试集
        arr_test.to_csv(path+"\\data\job_predict.csv", sep="\t", header=False, index=False)

