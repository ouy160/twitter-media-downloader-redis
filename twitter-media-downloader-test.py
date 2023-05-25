'''
Author: mengzonefire
Date: 2021-09-21 15:48:35
LastEditTime: 2023-03-09 23:31:12
LastEditors: mengzonefire
Description: 主函数入口
'''
import os

from common.console import read_data
from common.redisCli import getConnection

if __name__ == '__main__':
    r = getConnection()
    for i in read_data('data.hot'):
        print(r.delete(i.replace("https://twitter.com/", "twitter:user:").replace("/media", "")))


