"""
@author:MIAO
@file: data_reprocessing.py
@time: 2020/07/23
"""
import jieba
import pandas as pd
import csv
# 首先导入PyMySQL库
import pymysql
import os

path = os.getcwd()
path = os.getcwd().replace("\\","/")
path = path+"/target/classes/algorithm"

# 连接数据库，创建连接对象connection
DBHOST='121.36.44.148'#host属性
DBUSER='root' #用户名
DBPASS='83ec64005ba39e58'#此处填登录数据库的密码
DBNAME='recruitment' #数据库名
# 导入自定义的词典
jieba.load_userdict(path+"\\data\word_fengci.txt")


class DataSegmentation():
    def __init__(self):
        pass

    def get_data(self):
        '''
        从mysql数据库中获取数据
        :param self: 
        :return: 
        '''
        try:
            connection = pymysql.connect(DBHOST, DBUSER, DBPASS, DBNAME)
            print("数据库连接成功!")
            sql = "select * from job_preprocessing"
            print("数据查询成功！")
            # 转换为DataFrame格式
            return pd.read_sql(sql, connection)
        except pymysql.Error as e:
            print("数据查询失败:" + str(e))
            connection.rollback()
        connection.close()

    def stop_words(self, path):
        '''
        :param path: 停用词表的路径
        :return: 停用词表的列表
        '''
        with open(path, encoding="utf-8") as f:
            return [l.strip() for l in f]

    def test_right(self, x):
        '''
        :param x:进行分词的语句
        :return: 分词后的语句长度是否大于2的布尔标志
        '''
        if x.find("熟练") != -1 or x.find("掌握") != -1 or x.find("了解") != -1 or x.find("熟悉") != -1 or x.find("精通") != -1:
            if len(x) > 2:
                return True
            print(len(x))
            return False
        return False

    # 进行遍历，分词
    def segmentation(self,data):
        '''
        对数据进行遍历和分词
        :return: 
        '''
        length = len(data["content"])
        for i in range(0, length):
            content = data["content"][i]

            result_fengci = [x for x in jieba.cut(content) if
                             x not in self.stop_words(path+"\\data/stopwords.txt") and self.test_right(x) == True]
            data["content"][i] = "/".join(result_fengci)
        return data

