#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup

r = requests.get(
    'https://book.douban.com/latest?icn=index-latestbook-all')  # 构建requests请求
# print(r.encoding, r.status_code)
soup = BeautifulSoup(r.text, 'lxml')
# 查找标签 ,find() find_all()


def datacrawler(urli):
    ri = requests.get(url=urli)
    soupi = BeautifulSoup(ri.text, 'lxml')
    # print(soup.prettify())  # 检查输出结果

    # 获取书名、作者、出版信息等，并对数据格式进行处理
    # title：书名
    # infor1:包含作者、出版信息的列表

    title = soupi.find('h1').text.replace('\n', '')
    infor1 = soupi.find('div', id='info').text.replace(' ', '')
    infor1 = re.split('[\n:]', infor1)
    # print(infor1)

    # 遍历列表infor1，把不需要的空格删去
    for item in infor1[:]:
        if item == '':
            infor1.remove(item)

    # 将书名和出版信息存储在一个字典中
    dic1 = dict(zip(infor1[::2], infor1[1::2]))

    # 同样的方式处理左侧的豆瓣评论
    infor2 = soupi.find('div', id='interest_sectl').text
    # print(infor2)  # 查看infor2的列表信息，发现很多\n
    infor2 = re.split('[\n]', infor2)  # 用正则删去多余的\n
    for item in infor2[:]:
        if item == '':
            infor2.remove(item)

    # 对是否存在评论数量做判断，若不存在评论，显示暂无数据
    if len(infor2) > 2:
        commentd_number = infor2.pop(2)  # list.pop删除列表项
        dic2 = dict(zip(infor2[::2], infor2[1::2]))
        # 新建一个字典整合所有信息
        dic = {
            '书名': title,
            '书籍信息': dic1,
            '相关评价': dic2,
            '评论数量': commentd_number
        }
    else:
        dic2 = dict(zip(infor2[::2], infor2[1::2]))
        dic = {'书名': title, '书籍信息': dic1, '相关评价': dic2, '评论数量': '暂无数据'}
    return dic


# 采集信息 包括采集网页地址、采集次数
urls = soup.find('ul', class_='cover-col-4 clearfix').find_all('a')
url_lst = []
for url in urls[::2]:
    url_lst.append(url['href'])
data = []
n = 0
for u in url_lst:
    print('采集网页：', u)
    n += 1
    data.append(datacrawler(u))
    print('该网页成功采集%i次' % n)
    print(datacrawler(u))
