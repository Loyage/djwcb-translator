#!/usr/bin/python
# -*- coding: UTF-8 -*-

import csv
import re
from urllib.request import urlopen

from bs4 import BeautifulSoup

word_dict = {}
html_doc = urlopen('http://xh.5156edu.com/pinyi.html')
soup = BeautifulSoup(html_doc, 'lxml')
pinyin_all = soup.find_all('a')

# 遍历 a, an, ......
for pinyin in pinyin_all[6:-8]:
    # 打开拼音对应的网站
    url = pinyin.attrs['href']
    pinyin_doc = urlopen('http://xh.5156edu.com/' + url)

    # 提取关键内容
    word_line = pinyin_doc.readline()
    while not re.match(b'</table><', word_line):
        word_line = pinyin_doc.readline()
    word_line = word_line.decode('GBK', errors='ignore')  # bytes to str
    word_line = word_line[8:]

    # 构造字典
    py_soup = BeautifulSoup(word_line, 'lxml')
    py_tone_list = py_soup.findAll('tr', {'bgcolor': '#ffffff'})

    # 遍历不同声调
    for py_tone in py_tone_list:
        if '未分类' not in py_tone.text:
            tone = py_tone.td.p.text
            word = list(py_tone.td.next_sibling.children)[-1].next ### 这里采用的是笔画最多的汉字
            word_dict[tone] = word

# 写入csv
with open('word_dict.csv', "w", encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in word_dict.items():
        writer.writerow([key, value])
