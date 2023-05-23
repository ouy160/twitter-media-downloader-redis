'''
Author: mengzonefire
Date: 2021-09-21 15:48:35
LastEditTime: 2023-03-09 23:31:12
LastEditors: mengzonefire
Description: 主函数入口
'''
import os

from common.console import read_data, process_data


def fun(s):
    return s.replace('\n', '')


def fun2(s: str):
    return s.split('-')[-2] if len(s.split('-')) == 4 else ''
def makeData(path):
    arr = os.listdir(path)
    arr.sort()
    arr = list(map(fun2, arr))
    arr.remove('') if '' in arr else None
    new_li=list(set(arr))
    new_li.sort(key=arr.index)
    print('\n'.join(new_li))


def __data__(filePath):
    if os.path.exists(os.path.join(filePath, '__data__')):
        with open(os.path.join(filePath, '__data__')) as f:
            arr = f.readlines()
        arr = list(map(fun, arr))
        return arr
    else:
        return []


# if __name__ == '__main__':
#     print(__data__(r'C:\Users\qiaohuiguo\IdeaProjects\twitter-media-downloader\twitter_media_download\xiaoheiwu002'))
if __name__ == '__main__':
    # print(read_data())
    url_list = process_data(read_data())
    print(len(url_list))

