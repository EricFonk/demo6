# -*- coding: utf-8 -*-
import scrapy
from Lagou.items import LagouItem
import bs4
import requests


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['https://www.lagou.com/']
    # start_urls = ['http://https://www.lagou.com//']
    start_urls = [
        'https://www.lagou.com/chengdu-zhaopin/Java/{}/?filterOption=4&sid=f54ef8f5a92d468f9bd952b653e6f7d3'.format(i)
        for i in range(1,31)]
    login_url = "https://passport.lagou.com/login/login.html"

    headers = {
        'User-Agent': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    def parse(self, response):
        # chrome = webdriver.Chrome
        # datas = response.xpath('//ul[@class="item_con_list"]/li')
        # for data in datas:
        #     item = LagouItem()
        #     item['title'] = data.xpath('//div//div/a/h3[1]/text()').get()
        #     yield item
        soup = bs4.BeautifulSoup(response.text,features='lxml')
        for i in soup.find_all('a', class_='position_link'):
            link = i['href']
            s = requests.Session()
            s.get(link, headers=self.headers, timeout=3)
            cookie = s.cookies
            res = requests.get(link, headers=self.headers, cookies=cookie, timeout=5)
            bs = bs4.BeautifulSoup(res.text, 'lxml')
            # print(res.text)
            positionname = bs.find(class_='name').string
            salary = bs.select('.job_request h3 span:nth-child(1)')[0].get_text()
            location = bs.select('.job_request h3 span:nth-child(2)')[0].get_text()
            experience = bs.select('.job_request h3 span:nth-child(3)')[0].get_text()
            education = bs.select('.job_request h3 span:nth-child(4)')[0].get_text()
            detail = bs.select('.job-detail')[0].get_text()
            item = LagouItem()
            item['positionname'] = positionname
            item['salary'] = salary
            item['location'] = location
            item['experience'] = experience
            item['education'] = education
            item['detail'] = detail
            yield item

            # yield scrapy.Request(href, headers=self.headers, callback=self.parse_info)

    # def parse_info(self, response):
    #     print('------------------------------------jiexi-------------------------------------')
    #     print(response.text)
    #     with open('respoms.txt','wb') as f:
    #         f.write(response.text)

    # def __init__(self):
    #     self.login()

    # def login(self):
    #     chrome = webdriver.Chrome()
    #     chrome.minimize_window()
    #     username = '18080121376'
    #     password = 'lyh151982'
    #     chrome.find_element_by_css_selector("div:nth-child(2) > form > div:nth-child(1) > input").send_keys(username)
    #     chrome.find_element_by_css_selector("div:nth-child(2) > form > div:nth-child(2) > input").send_keys(password)
    #     chrome.find_element_by_css_selector(
    #         "div:nth-child(2) > form > div.input_item.btn_group.clearfix > input").click()
    #     return chrome