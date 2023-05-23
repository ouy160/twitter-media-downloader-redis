'''
Author: mengzonefire
Date: 2021-09-21 15:48:35
LastEditTime: 2023-03-09 23:31:12
LastEditors: mengzonefire
Description: 主函数入口
'''
import json
import os
import random

from common.redisCli import getConnection

if __name__ == '__main__':
    r = getConnection()

    dir = r'I:\twitter\twitter_media_download'
    list = os.listdir(dir)
    count = 0
    count2 = 0
    count1 = 0
    for idir in list:
        blogerMediaDir = dir + "\\" + idir + "\\__ALL__"
        with open(blogerMediaDir, mode='r') as f:
            for item in f.readlines():
                arr = item.split("@#@")
                k = arr[0]
                v = arr[1]
                count += 1
                if r.exists("twitter:" + k):
                    count1 += 1
                    redisval = r.get("twitter:" + k)
                    if redisval == v:
                        pass
                    else:
                        if r.exists("repeat:" + k, v):
                            r.set("repeat:" + k + ":" + str(random.randint(1, 50))
                                  + str(random.randint(1, 50))
                                  + str(random.randint(1, 50)), v)
                        else:
                            r.set("repeat:" + k, v)
                else:
                    r.set("twitter:" + k, v)
                    count2 += 1
    print('总数' + str(count))
    print('重复' + str(count1))
    print('实际' + str(count2))
