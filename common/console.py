'''
Author: mengzonefire
Date: 2021-09-21 09:20:19
LastEditTime: 2023-03-13 20:36:56
LastEditors: mengzonefire
Description: 命令行交互模块
'''
import time

from common.Analyzer import post_frequency_analyzer
from task.singlePageTask import SinglePageTask
from task.searchTask import UserSearchTask
from typing import List
from common.text import *
from common.const import *
from common.tools import getGuestCookie, getUserId, saveEnv, showConfig, setProxy, setCookie, clear
from task.userFollowingTask import UserFollowingTask
from task.userHomeTask import UserHomeTask
from task.userLikesTask import UserLikesTask
from task.userMediaTask import UserMediaTask


def cmdMode(clearScreen=True):
    if clearScreen:
        clear()
    showConfig()
    print(input_ask)
    url_list = []
    while True:
        temp = input()
        if not temp:
            break
        elif temp == '0':
            return
        elif temp == '1':
            setCookie()
            saveEnv()
            showConfig()
            print(input_ask)
        elif temp == '2':
            setProxy()
            saveEnv()
            showConfig()
            print(input_ask)
        elif temp == '3':
            config()
            showConfig()
            print(input_ask)
        elif temp == '4' or temp.count('5') > 0 or temp == '6' or temp == '7' or temp == 8:
            url_list = getList(temp)
        elif temp == '9':
            post_frequency_analyzer()
        elif temp.count('@') > 0:
            url_list = process_data([temp])
        elif urlChecker(temp):
            url_list.append(temp)
        else:  # 输入错误, 重置
            input(input_warning)
            clear()
            showConfig()
            print(input_ask)
            url_list = []
    if url_list:
        startCrawl(url_list)
    if input(continue_ask):
        cmdMode()


def getList(num):
    num = str(num)
    url_list = []
    if num == '4':
        url_list = process_data(read_data('data'))
    elif num.startswith('5'):
        url_list = process_data(read_data('data.hot'))
        if num.count(",") > 0:
            skip = int(num.split(",")[1])
            url_list = url_list[skip - 1:]
    elif num.startswith('-5'):
        l = read_data('data.hot')
        l.reverse()
        url_list = process_data(l)
        if num.count(",") > 0:
            skip = int(num.split(",")[1])
            url_list = url_list[skip - 1:]
    elif num == '6':
        url_list = process_data(read_data('data.analyze.low'))
    elif num == '7':
        url_list = process_data(read_data('data.analyze.mid'))
    elif num == '8':
        url_list = process_data(read_data('data.analyze.hig'))
    return url_list


def read_data(fileName):
    if not os.path.exists(fileName) and fileName.count("analyze") > 0:
        post_frequency_analyzer()
    url_list = []
    f = open(fileName, 'r', encoding='UTF-8')
    line = f.readline()
    while line:
        # if line.startswith("http"):
        url_list.append(line.replace("\n", '').split(" ")[0])
        line = f.readline()
    f.close()
    return url_list


def process_data(list: List):
    url_list = []
    tempList = []
    for url in list:
        if not url:
            continue
        else:
            if str(url).count("/@") > 0:
                if str(url).endswith("/@all"):
                    tempList.append(removesuffix(str(url), "/@all") + "/@mhl")
                else:
                    tempList.append(url)
            else:
                url_list.append(url)
    if len(tempList) > 0:
        for u in tempList:
            suffix = u.split("@")[-1]
            if suffix.count('m') > 0:
                url_prefix = removesuffix(str(u), "/@" + suffix)
                url_list.append('https://twitter.com/' + url_prefix + "/media")
        #     if suffix.count('h') > 0:
        #         url_prefix = removesuffix(str(u), "/@" + suffix)
        #         url_list.append('https://twitter.com/' + url_prefix)
        # for u in tempList:
        #     suffix = u.split("@")[-1]
        #     if suffix.count('l') > 0:
        #         url_prefix = removesuffix(str(u), "/@" + suffix)
        #         url_list.append('https://twitter.com/' + url_prefix + "/likes")
    return url_list


def removesuffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[:-len(suffix)]
    return input_string


def config():  # 设置菜单
    clear()
    while True:
        set = input(download_settings_ask)
        if set == '0':
            break
        elif set == '1':
            setType()
            saveEnv()
        elif set == '2':
            maxConcurrency()
            saveEnv()
        elif set == '3':
            quotedStatus()
            saveEnv()
        elif set == '4':
            retweetedStatus()
            saveEnv()
        elif set == '5':
            mediaStatus()
            saveEnv()
        elif set == '6':
            setFileName()
            saveEnv()
        else:
            input(input_num_warning)
            clear()
    clear()


def setType():  # 设置下载类型
    clear()
    while True:
        only = ''.join(set(list(input(set_type_ask))))
        if only == '0':
            break
        elif set(only) <= set('1234'):
            type = []
            for i in only:
                if i == '1':
                    type.append('photo')
                elif i == '2':
                    type.append('animated_gif')
                elif i == '3':
                    type.append('video')
                elif i == '4':
                    type.append('full_text')
            setContext('type', '&'.join(type))
            break
        elif only == '5':
            type = ['photo', 'animated_gif', 'video', 'full_text']
            setContext('type', '&'.join(type))
            break
        else:
            input(input_num_warning)
            clear()
    clear()


def setFileName():  # 设置自定义保存文件名
    clear()
    while True:
        fileName = input(set_fileName_ask).strip()
        if fileName == '0':
            break
        else:
            if not len(p_unexpect_var.findall(fileName)):
                setContext('fileName', re.sub(r'[\\/:*?"<>|]', '', fileName))
                break
            else:
                input(unexpectVar_input_warning)
                clear()
    clear()


def maxConcurrency():  # 设置线程数
    clear()
    while True:
        num = input(max_concurrency_ask)
        if num == '0':
            break
        else:
            try:
                setContext('concurrency', int(num))
                clear()
                break
            except ValueError:
                input(input_num_warning)
                clear()
    clear()


def mediaStatus():  # 设置非媒体
    clear()
    while True:
        set = input(media_status_ask)
        if set == '0':
            break
        elif set == '1':
            setContext('media', True)
            break
        elif set == '2':
            setContext('media', False)
            break
        else:
            input(input_num_warning)
            clear()
    clear()


def quotedStatus():  # 设置引用
    clear()
    while True:
        set = input(quoted_status_ask)
        if set == '0':
            break
        elif set == '1':
            setContext('quoted', True)
            break
        elif set == '2':
            setContext('quoted', False)
            break
        else:
            input(input_num_warning)
            clear()
    clear()


def retweetedStatus():  # 设置转推
    clear()
    while True:
        set = input(retweeted_status_ask)
        if set == '0':
            break
        elif set == '1':
            setContext('retweeted', True)
            break
        elif set == '2':
            setContext('retweeted', False)
            break
        else:
            input(input_num_warning)
            clear()
    clear()


def startCrawl(urlList: List):
    if not len(urlList) or not getGuestCookie():
        return
    dl_path = getContext('dl_path')
    if not os.path.exists(dl_path):
        os.mkdir(dl_path)
    size = len(urlList)
    success = 0
    print('\n共{}条数据, 当前时间:{}'.format(size, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    for inx, url in enumerate(urlList):
        if not url:
            continue
        if urlChecker(url):
            print('\n正在提取 第{}条: {} > 剩余{}条 , 当前时间:{}'.format(inx + 1, url, size - inx - 1,
                                                                          time.strftime("%Y-%m-%d %H:%M:%S",
                                                                                        time.localtime())))
            urlHandler(url)
            success += 1
        else:
            print('\n不支持: {}'.format(url))
    print(
        '\n爬取完成. 共完成{}条数据. 当前时间:{}'.format(success, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))


def urlChecker(url: str):
    return p_twt_link.findall(url) or p_user_link.findall(url) or url[0] == '@'


def urlHandler(url: str):
    cfg = {'media': getContext('media'), 'quoted': getContext(
        'quoted'), 'retweeted': getContext('retweeted')}

    # singlePage
    twt_link = p_twt_link.findall(url)
    if twt_link:
        userName = twt_link[0][0]
        twtId = int(twt_link[0][1])
        SinglePageTask(userName, twtId, cfg).start()
        return

    user_link = p_user_link.findall(url)
    if user_link:
        func = url.split('/')[-1]
        userName = user_link[0]
        userInfoArr = getUserId(userName)
        if not userInfoArr:
            return
        userId = userInfoArr[0]
        uname = userInfoArr[1]
        if func == 'media':
            # userMediaPage
            UserMediaTask(userName, uname, userId, cfg).start()
            return
        elif func == 'likes':
            # userLikesPage
            UserLikesTask(userName, uname, userId, cfg).start()
            return
        elif func == 'following':
            # userFollowingPage
            UserFollowingTask(userName, uname, userId).start()
            return
        else:
            # userHomePage
            UserHomeTask(userName, uname, userId, cfg).start()
            return

    # searchPage
    if url[0] == '@':
        if 'advanced=' in url:
            advanced = url.split('&')[-1].replace('advanced=', '')
            userName = url.split('&')[0].replace('@', '')
            date = None
        elif '&' in url and len(url.split('&')) == 2:
            advanced = None
            userName = url.split('&')[0].replace('@', '')
            date = [url.split('&')[1].split('|')[0],
                    url.split('&')[1].split('|')[1]]
        elif '&' not in url:
            advanced = None
            userName = url[1:]
            date = None
        else:
            print(f'无法解析：{url}')
            return
        if userName:
            UserSearchTask(userName, date, advanced, cfg).start()
        elif advanced:
            UserSearchTask(userName, date, advanced, cfg).start()
