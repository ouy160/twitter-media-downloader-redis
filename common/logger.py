'''
Author: mengzonefire
Date: 2021-09-21 09:23:35
LastEditTime: 2023-03-10 06:53:08
LastEditors: mengzonefire
Description: 日志模块
'''

import os
import re
from common.const import getContext
from common.text import log_warning


def writeLog(log_name, log_content):
    log_path = os.path.normpath(getContext('log_path'))
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    file_path = re.sub(
        r'[:*?"<>|]', '', '{}/{}.log'.format(log_path, log_name))  # 去除路径内的非法字符
    exists = os.path.exists(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
        if not exists:
            print(log_warning.format(os.path.abspath(file_path)))
