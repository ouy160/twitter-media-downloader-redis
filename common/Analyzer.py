import collections
import decimal
import os
import re
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List

from common.const import getContext
from common.tools import getEnv


def post_frequency_analyzer():
    today = datetime.now().date()
    data_dir = "data.all"
    data_map = {}
    with open(data_dir) as f:
        for line in f.readlines():
            matches = re.findall("twitter\\.com/(\\w+)/@(\\w+)", line)
            for match in matches:
                username, tag = match
                if username in data_map:
                    print(username)
                data_map[username] = tag
    root_dir_old = getContext('od_path')
    root_dir_new = getContext('dl_path')
    time_window = timedelta(days=30)
    data = defaultdict(list)
    for blogger in list(set(os.listdir(root_dir_new) + os.listdir(root_dir_old))):
        avg_post_frequency = analyzer(blogger, time_window)
        format_frequency = decimal.Decimal(str(avg_post_frequency / time_window.days))
        data[format_frequency].append(blogger)

    keys_mid = [k for k in sorted(data.keys(), reverse=True) if 0 < k <= 1]
    keys_low = [k for k in sorted(data.keys(), reverse=True) if k == 0]
    keys_hig = [k for k in sorted(data.keys(), reverse=True) if k > 1]
    map_freq = collections.OrderedDict(sorted(data.items(), reverse=True))
    write_file(keys_low, data_map, map_freq, 'low', data_dir, today)
    write_file(keys_mid, data_map, map_freq, 'mid', data_dir, today)
    write_file(keys_hig, data_map, map_freq, 'hig', data_dir, today)


def write_file(keys: List[decimal.Decimal], data_map: dict, map_freq: dict, suffix: str, data_dir, today) -> None:
    joiner = []
    joiner.append(f'--统计于{today}--')
    for key in keys:
        for value in map_freq[key]:
            if value in data_map:
                joiner.append(f'https://twitter.com/{value}/@{data_map[value]} #{key:.2%}')
    with open(os.path.join(os.path.dirname(data_dir), f'data.analyze.{suffix}'), 'w', encoding='utf8') as out_f:
        out_f.write('\n'.join(joiner))


def analyzer(blogger: str, time_window: timedelta) -> float:
    time_window_secs = time_window.total_seconds()
    posts = get_posts(blogger)
    if not posts:
        return 0.0
    posts.sort()
    post_counts = []
    count = 0

    index = 0
    curr_time = datetime.now().timestamp()
    for post_time in posts:
        if curr_time - post_time <= time_window_secs:
            if index == 0:
                curr_time = post_time

            if post_time - curr_time > time_window_secs:
                post_counts.append(count)
                count = 1
                curr_time = post_time
            else:
                count += 1
        index += 1

    post_counts.append(count)
    return sum(post_counts) / len(post_counts)


def get_posts(blogger: str) -> List[float]:
    root_dir_old = getContext('od_path')
    root_dir_new = getContext('dl_path')
    root_dir_old_list = root_dir_old + f"\\{blogger}"
    root_dir_new_list = root_dir_new + f"\\{blogger}"
    result = set()
    for dirname in ["media", "home"]:
        lst = []
        path = os.path.join(root_dir_old_list, dirname)
        if os.path.isdir(path):
            lst += get_timestamps(path, blogger)
        path = os.path.join(root_dir_new_list, dirname)
        if os.path.isdir(path):
            lst += get_timestamps(path, blogger)
        result.update(lst)
    return sorted(result)


def get_timestamps(dir_path: str, blogger: str) -> List[float]:
    result = []
    for filename in os.listdir(dir_path):
        if blogger in filename:
            timestamp_str = filename[:15]
            timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S").timestamp()
            result.append(timestamp)
    return result


def format_pct(val: float, digits: int = 2) -> str:
    return f"{val:,.{digits}%}"


if __name__ == "__main__":
    getEnv()
    post_frequency_analyzer()
