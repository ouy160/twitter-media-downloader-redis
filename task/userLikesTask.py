'''
Author: mengzonefire
Date: 2023-03-01 13:58:17
LastEditTime: 2023-03-15 00:33:39
LastEditors: mengzonefire
Description: likes页爬取任务类
'''

import time
import httpx

from common.text import *
from common.const import *
from common.tools import getHttpText
from task.baseTask import Task


class UserLikesTask(Task):

    def __init__(self, userName: str, uname, userId: int, cfg):
        super(UserLikesTask, self).__init__()
        self.userName = userName
        self.uname = uname
        self.userId = userId
        self.cfg = cfg
        # self.savePath = os.path.join(getContext('dl_path'), userName, 'likes')
        self.savePath = '{}/{}/likes'.format(getContext('dl_path'), userName)
        self.saveUri = '@{}/likes'.format(userName)
    def getDataList(self, cursor='', rest_id_list=[]):
        while True:
            if self.stop:
                return
            cursorPar = cursor and '"cursor":"{}",'.format(cursor)
            response = None
            with httpx.Client(proxies=getContext('proxy'), headers=getContext('headers'), verify=False, timeout=60) as client:
                for i in range(1, 56):
                    try:
                        response = client.get(userLikesApi, params={
                            'variables': userLikesApiPar.format(self.userId, twtCount, cursorPar),
                            'features': commonApiPar})
                        break
                    except (httpx.ConnectTimeout, httpx.ReadTimeout, httpx.ConnectError, httpx.RemoteProtocolError):
                        if i >= 55:
                            print(network_error_warning)
                            self.stopGetDataList()
                            return
                        else:
                            print(timeout_warning.format(i))
                            time.sleep(0.3)
            if not response:
                self.stopGetDataList()
                return
            if response.status_code != httpx.codes.OK:
                print(http_warning.format('UserLikesTask.getDataList',
                                          response.status_code, getHttpText(response.status_code)))
                self.stopGetDataList()
                return
            self.pageContent = response.json()
            cursor, rest_id_list = self.parseData(cursor, rest_id_list)
            if not cursor:
                break
