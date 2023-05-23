'''
Author: mengzonefire
Date: 2021-09-21 09:19:02
LastEditTime: 2023-03-15 00:49:43
LastEditors: mengzonefire
Description: 推主推文批量爬取任务类
'''
import time
import httpx

from common.const import *
from common.text import *
from common.tools import getHttpText
from task.baseTask import Task


class UserMediaTask(Task):

    def __init__(self, userName, uname, userId, cfg):
        super(UserMediaTask, self).__init__()
        self.userName = userName
        self.uname = uname
        self.userId = userId
        self.cfg = cfg
        # self.savePath = '{}/{}@{}'.format(getContext('dl_path'), uname, userName)
        self.savePath = '{}/{}/media'.format(getContext('dl_path'), userName)
        self.saveUri = '@{}/media'.format(userName)

    def getDataList(self, cursor='', rest_id_list=[]):
        while True:
            if self.stop:
                return
            cursorPar = cursor and '"cursor":"{}",'.format(cursor)
            response = None
            with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), verify=False) as client:
                for i in range(1, 56):
                    try:
                        response = client.get(userMediaApi, params={
                            'variables': userMediaApiPar.format(self.userId, twtCount, cursorPar),
                            'features': commonApiPar})
                        break
                    except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError):
                        if i >= 55:
                            print(network_error_warning)
                            return False
                        else:
                            print(timeout_warning.format(i))
                            time.sleep(0.3)
            if not response:
                self.stopGetDataList()
                return
            if response.status_code != httpx.codes.OK:
                print(http_warning.format('UserMediaTask.getDataList',
                                          response.status_code, getHttpText(response.status_code)))
                self.stopGetDataList()
                return
            self.pageContent = response.json()
            cursor, rest_id_list = self.parseData(cursor, rest_id_list)
            if not cursor:
                break
