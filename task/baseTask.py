'''
Author: mengzonefire
Date: 2021-09-24 21:04:29
LastEditTime: 2023-03-15 00:45:27
LastEditors: mengzonefire
Description: 任务类基类
'''

import json
import math
import os
import threading
import time
import traceback
from abc import abstractmethod
from concurrent.futures import ThreadPoolExecutor, wait
from queue import Queue

from common.const import getContext
from common.logger import writeLog
from common.text import *
from common.tools import downloadFile, parseData


class Task(object):

    def __init__(self):
        self.tasks = set()  # 任务线程对象容器
        self.userName = ''  # 推主id（不是昵称）
        self.savePath = ''  # 下载路径
        self.saveUri = ''  # 下载路径
        self.saveAbsPath = ''  # 下载路径
        self.twtId = None  # 推文id(int)
        self.userId = None  # 推主rest_id(int)
        self.cfg = {}  # 爬取media页的时候会强制覆盖全局配置参数，故在类成员内单独添加标记
        self.stop = False  # 进度条与生产者停止信号
        self.total = Queue()  # 任务总量计数器
        self.done = Queue()  # 已完成任务计数器
        self.dataList = Queue()  # 任务数据队列
        self.pageContent = None  # 接口元数据(用于debug)
        self.errFlag = False
        self.__data__ = []
        self.__di__ = False

    @abstractmethod
    def getDataList(self):
        raise NotImplemented

    def get_data0(self):
        if not self.__di__:
            self.__data__ = self.data()
            self.__di__ = True
        return self.__data__

    def data(self):
        arr = []
        if os.path.exists(os.path.join(self.savePath, '__data__')):
            with open(os.path.join(self.savePath, '__data__')) as f:
                arr += f.readlines()
        # todo
        if os.path.exists(
                os.path.join(self.savePath.replace(getContext('dl_path'), getContext('od_path')), '__data__')):
            with open(os.path.join(self.savePath.replace(getContext('dl_path'), getContext('od_path')),
                                   '__data__')) as f0:
                arr += f0.readlines()
        arr = list(map(lambda s: s.replace('\n', ''), arr))
        return arr

    def parseData(self, cursor, rest_id_list):
        try:
            cursor, rest_id_list = parseData(
                self.pageContent, self.total, self.userName, self.dataList, self.cfg, rest_id_list, cursor, self)
        except (KeyError, TypeError):
            self.errFlag = True
            print(parse_warning)
            writeLog(f'{self.userName}_unexpectData',
                     f'{traceback.format_exc()}\n\n{json.dumps(self.pageContent, ensure_ascii=False)}')  # debug
        except Exception:
            self.errFlag = True
            print(crash_warning)
            writeLog(f'{self.userName}_crash',
                     traceback.format_exc())  # debug
        finally:
            if self.errFlag or not cursor:  # 结束
                self.stopGetDataList()
                return None, None
            else:  # 继续
                return cursor, rest_id_list

    def stopGetDataList(self):
        for _ in range(getContext('concurrency')):
            self.dataList.put(None)

    def progressBar(self, start):
        while True:
            for i in ['|', '/', '一', '\\', '|', '/', '一', '\\']:
                for _ in range(5):
                    done = self.done.qsize()
                    total = self.total.qsize()
                    if total == 0:
                        if self.stop:
                            return
                        continue
                    progress = (done / total) * 50  # 缩短进度条长度防止cmd自动换行
                    length = time.perf_counter() - start
                    print(f"\r@{self.userName} {round(progress, 1) * 2}% [{'█' * math.floor(progress)}"
                          f"{' ' * (50 - math.ceil(progress))}] [{done}/{total}] {round(length, 1)}s {i}", end='')
                    if self.stop:
                        return
                    time.sleep(0.1)

    def start(self):
        self.savePath = os.path.normpath(self.savePath)
        self.saveAbsPath = os.path.abspath(self.savePath)
        if not os.path.exists(self.savePath):
            os.makedirs(self.savePath)
        start = time.perf_counter()
        t1, t2 = threading.Thread(target=self.getDataList), threading.Thread(
            target=self.progressBar, args=(start,))
        t1.start()
        t2.start()
        with ThreadPoolExecutor(max_workers=getContext('concurrency')) as executor:
            for _ in range(getContext('concurrency')):
                task = executor.submit(
                    downloadFile, self.savePath, self.saveUri, self.dataList, self.done)
                self.tasks.add(task)
        wait(self.tasks)
        self.stop = True
        t1.join()
        t2.join()
        if self.total.qsize():
            with open(os.path.join(self.savePath, '__data__'), 'w+', encoding="utf-8") as f:
                f.write(makeData(self.savePath))  # 文件的写操作
            print(task_finish.format(self.done.qsize(), self.total.qsize(),
                                     round(time.perf_counter() - start, 1), self.saveAbsPath))
        elif self.pageContent and not self.errFlag:
            print(dl_nothing_warning)
            writeLog(f'{self.twtId or self.userName}_noMedia',
                     json.dumps(self.pageContent, ensure_ascii=False))  # debug


def fun2(s: str):  # 需要优化  仅适用于自己
    return s.split('-')[-2] if len(s.split('-')) == 4 else ''


def makeData(path):
    arr = os.listdir(path)
    arr.sort()
    arr = list(map(fun2, arr))
    arr.remove('') if '' in arr else None
    new_li = list(set(arr))
    new_li.sort(key=arr.index)
    return '\n'.join(new_li)
