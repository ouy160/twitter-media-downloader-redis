'''
Author: mengzonefire
Date: 2021-09-21 15:48:35
LastEditTime: 2023-03-09 23:31:12
LastEditors: mengzonefire
Description: 主函数入口
'''
import sys
import traceback
from common.console import cmdMode, startCrawl, getList
from common.tools import *


def main():
    exe_path, _ = os.path.split(sys.argv[0])
    if exe_path:
        os.chdir(exe_path)  # 切换工作目录到程序根目录
    initalArgs()
    getEnv()
    if len(sys.argv) == 1:  # 命令行参数为空 / 双击运行程序 -> 进入交互模式
        print('version: {}'.format(
            version))
        checkUpdate()
        cmdMode(False)
    else:
        argsHandler()
        arg = getContext('args')
        if arg.x:
            stri = str(arg.x)
            if arg.s:
                stri += ',' + str(arg.s)
            print(stri)
            startCrawl(getList(stri))
        startCrawl(arg.url)


def test():  # debug
    getSysProxy()
    # with open('./sample/twt.json', 'r') as f:1
    #     print(getResult(json.loads(f.read())))


if __name__ == '__main__':
    try:
        main()
        # test()
    except KeyboardInterrupt:
        pass
    except Exception:  # 缺失异常处理
        print(crash_warning)
        print(traceback.format_exc())
        writeLog('crash', traceback.format_exc())
