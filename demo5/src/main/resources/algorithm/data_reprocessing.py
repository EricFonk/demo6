"""
@author:MIAO
@file: data_reprocessing.py
@time: 2020/07/23
"""
import numpy as np
import pandas as pd
#首先导入PyMySQL库
import pymysql
#连接数据库，创建连接对象connection
DBHOST='121.36.44.148'#host属性
DBUSER='root' #用户名
DBPASS='83ec64005ba39e58'#此处填登录数据库的密码
DBNAME='recruitment' #数据库名

#对数据进行清洗与预处理
class DataClean():
    def __init__(self):
        pass
    def get_data(self):
        try:
            connection = pymysql.connect(DBHOST, DBUSER, DBPASS, DBNAME)
            print("数据库连接成功!")
            sql = "select * from job"
            print("数据查询成功！")
            #转换为DataFrame格式
            return pd.read_sql(sql, connection)
        except pymysql.Error as e:
            print("数据查询失败:" + str(e))
            connection.rollback()
        connection.close()
    def clean_operation(self):
        data_employee = self.get_data()
        data_employee = data_employee.dropna()
        # 数据清理，缺失值处理，异常值处理
        data_employee = data_employee[~ data_employee['salary'].str.contains('万/年')]
        data_employee = data_employee[~data_employee['salary'].str.contains('千/月')]
        data_employee = data_employee[~data_employee['salary'].str.contains('元/天')]
        data_employee = data_employee[~data_employee['salary'].str.contains('元/小时')]
        data_employee = data_employee[~data_employee['salary'].str.contains('以下')]
        data_employee = data_employee[~data_employee['salary'].str.contains('以上')]
        data_employee = data_employee[~data_employee['title'].str.contains('Engineer|�|Developer|职位编号')]
        data_employee = data_employee[~data_employee['place'].str.contains('�')]
        data_employee = data_employee[~data_employee['content'].str.contains('�|Responsibilities|Required|responsibilities|working|Description|experience|geek_spirit')]
        data_employee = data_employee[~data_employee['experience'].str.contains('�')]
        data_employee = data_employee[~data_employee['company'].str.contains('�')]
        data_employee = data_employee[data_employee['content'].str.len()>=30]
        data_employee = data_employee[
            data_employee['size'].str.contains('50-150人|150-500人|少于50人|500-1000人|1000-5000人|10000人以上|5000-10000人')]
        data_employee = data_employee[
            data_employee['experience'].str.contains('经验|本科|在校生/应届生|硕士|大专|无需经验|中专|高中|初中及以下')]
        data_employee = data_employee[data_employee['education'].str.contains('本科|硕士|大专|中技|中专|高中|初中及以下')]
        data_employee = data_employee[
            data_employee['title'].str.contains('师')]
        data_employee = data_employee[~data_employee['title'].str.contains('高级|中级|技术|/|（|-|\+|\(|\s|―|、')]
        data_list = data_employee['title'].index.tolist()
        for index in data_list:
            if len(data_employee['title'][index]) > 12:
                data_employee.drop(index,axis=0,inplace=True)
        data_employee = data_employee.reset_index(drop=True)
        data_employee = data_employee.drop('id', axis=1)

        for i, j in enumerate(data_employee["salary"]):
            j = j.replace("万/月", "")
            j1 = float(j.split('-')[0])
            j2 = float(j.split('-')[1])
            j3 = 1 / 2 * (j1 + j2)  # 求的是平均工资
            data_employee["salary"][i] = j3 * 10000
        data_employee["salary"] = data_employee["salary"].astype("int64")
        return data_employee

