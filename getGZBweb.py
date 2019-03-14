#!/usr/bin
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

# 根据月份和序列号，判断url链接是否有效。如果链接有效，则提取链接信息并下载文件
def verify_web(month, seq_no):
    # url示例
    # url = 'http://www.gzcb.com.cn/article/shgk/ggfb/12/162413.shtml'

    # 组装url
    url_pre = 'http://www.gzcb.com.cn/article/shgk/ggfb/'
    url_post = '.shtml'
    url_sep = '/'
    url = url_pre + month + url_sep + str(seq_no) + url_post
    print('url:' + url)

    req = requests.get(url)
    req.encoding = 'gb2312'

    # 以下语句用于排查中文显示乱码问题
    # print(sys.getdefaultencoding())
    # print(req.encoding)
    # print(req.headers['content-type'])
    # print(req.apparent_encoding)
    # print(requests.utils.get_encodings_from_content(req.text))
    # print(req.text)

    plain_text = req.text
    soup = BeautifulSoup(plain_text, "html5lib")
    if soup.title.string != '404 Not Found':
        # 如果链接有效，则提取链接信息并下载文件
        get_fileinfo(soup, seq_no)
        return month + ',' + str(seq_no) + ',' + url + ',' + soup.title.string
    else:
        return '404'


# 从url响应报文中获取文件下载链接，并组装文件名
def get_fileinfo(in_soup, seq_no):
    # 匹配href中含有文件后缀的链接标签
    fileinfo_all = in_soup.find_all("a", href=re.compile(r'(\.doc|\.pdf|\.xls)'), target="_blank")

    for fileinfo in fileinfo_all:
        # 组装文件下载链接
        file_url = 'http://www.gzcb.com.cn' + fileinfo['href']
        print(file_url)

        # 获取文件后缀
        file_post_pattern = re.compile(r'(\.doc|\.pdf|\.xls)')
        file_post = file_post_pattern.findall(fileinfo['href'])
        print(file_post)

        # 组装文件名
        if len(file_post) > 0:
            file_name = str(seq_no) + '_' + fileinfo.string + file_post[0]
        else:
            file_name = str(seq_no) + '_' + fileinfo.string

        # 下载文件到当前目录
        download_file(file_url, file_name)


# 通过stream模式下载文件，并关闭文件
def download_file(file_url, file_name):
    res = requests.get(file_url)
    f = open(file_name, "wb")
    for chunk in res.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
    f.flush()
    f.close()

# 测试单个有效url的处理
# print(verify_web('01', 164517))

# 按月根据seq_no范围遍历url，将有效url列表存储到文件
# getMonth = '01'
# f = open('GZBweb.txt', mode='a')
# for i in range(130000, 135614):
#     try:
#         result = verify_web(getMonth, i)
#         if result != '404':
#             f.write(result + '\n')
#             f.flush()
#     except UnicodeEncodeError:
#         print('UnicodeEncodeError')
#         f.write(getMonth + ',' + str(i) + '\n')
#         f.flush()
#
# f.close()


# 根据已经获取到的url列表下载链接文件
# 定义源文件的路径和名称
try:
    f_r_001 = open('GZBweb.txt', 'r', encoding='GBK')
    allLines = f_r_001.readlines()
    f_r_001.close()
except FileNotFoundError as e:
    print(e)
else:
    ###从源文件中装载已经采集到的item清单
    i = 0
    for eachLine in allLines:
        eachLine = eachLine.strip('\n')
        lineList = eachLine.split(",")
        i = i + 1
        verify_web(lineList[0], lineList[1])
        print('第' + str(i) + '条有效url记录处理完成：' + lineList[0] + ',' + lineList[1])
