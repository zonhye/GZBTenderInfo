#!/usr/bin
# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup

hds = [{'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}, \
       {
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'}, \
       {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}]


# 根据月份和序列号，判断url链接是否有效
def verify_web(month, seq_no):
    url_pre = 'http://www.gzcb.com.cn/article/shgk/ggfb/'
    url_post = '.shtml'
    url_sep = '/'
    # url = 'http://www.gzcb.com.cn/article/shgk/ggfb/12/162413.shtml'
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
        get_fileinfo(soup)
        return month + ',' + str(seq_no) + ',' + url + ',' + soup.title.string
    else:
        return '404'


# 从url中获取文件下载链接和文件名
def get_fileinfo(in_soup):
    fileinfo_all = in_soup.find_all("a", href=re.compile("(\.doc)|(\.pdf)"), target="_blank")
    for fileinfo in fileinfo_all:
        url = 'http://www.gzcb.com.cn' + fileinfo['href']
        print(url)
        filename = fileinfo.string
        download_file(url, filename)


# 通过stream模式下载文件
def download_file(url, filename):
    res = requests.get(url)
    f = open(filename + '.doc', "wb")
    for chunk in res.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)
    f.flush()
    f.close()


print(verify_web('01', 164517))

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
