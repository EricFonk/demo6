# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import csv
# class LagouPipeline(object):
#     def __init__(self):
#         self.db = pymysql.connect(host='localhost', user='root', password='root', port=3306, db='article_spider')
#         self.cursor = self.db.cursor()
#         self.sql = 'insert into lagou values (%s,%s,%s,%s,%s,%s)'
#
#     def process_item(self, item, spider):
#         # title = item['title']
#         # fname = 'data.txt'
#         # with open(fname,mode='a') as f:
#         #     f.write(title + '\n')
#         # f.close()
#         positionname = item['positionname']
#         salary = item['salary']
#         location = item['location']
#         experience = item['experience']
#         education = item['education']
#         detail = item['detail']
#         self.cursor.execute(self.sql,
#                        (str(positionname), str(salary), str(location), str(experience), str(education), str(detail)))
#         self.db.commit()
#         return item
#
#     def close_spider(self,spider):
#         self.cursor.close()
#         self.db.close()

# 改为存入csv文件
class LagouPipeline(object):
    def __init__(self):
        self.file = open("F:\\大创\\算法\\article_jobs.csv","w",encoding="utf-8",newline='')
        self.csv_writer = csv.writer(self.file)
        self.csv_writer.writerow(["岗位名","薪资","地址","经验要求","学历要求","岗位要求"])

    def process_item(self, item, spider):
        # title = item['title']
        # fname = 'data.txt'
        # with open(fname,mode='a') as f:
        #     f.write(title + '\n')
        # f.close()
        positionname = item['positionname']
        salary = item['salary']
        location = item['location']
        experience = item['experience']
        education = item['education']
        detail = item['detail']
        self.csv_writer.writerow([positionname,salary,location,experience,education,detail])
        return item

    def close_spider(self):
        self.file.close()