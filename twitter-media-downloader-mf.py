import os
import shutil

from common.redisCli import getConnection

r = getConnection()


def move_cache_files(src_dir, dest_dir, min_size=900 * 1024 * 1024):
    # 遍历源目录的一级子目录
    for user_folder in os.listdir(src_dir):
        user_folder_path = os.path.join(src_dir, user_folder)

        # 如果目标目录不存在，则创建它
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        # 检查路径是否为目录
        if os.path.isdir(user_folder_path):
            # 遍历每个用户目录下的一级子目录
            for media_folder in os.listdir(user_folder_path):
                media_folder_path = os.path.join(user_folder_path, media_folder)

                # 检查路径是否为目录
                if os.path.isdir(media_folder_path):
                    # 遍历每个 media 目录下的文件
                    for file in os.listdir(media_folder_path):
                        # 检查文件是否为 .mp4 文件
                        if file.endswith('.mp4'):
                            # 构建源文件的完整路径
                            src_path = os.path.join(media_folder_path, file)

                            # 获取文件大小
                            try:
                                file_size = os.path.getsize(src_path)
                            except Exception as e:
                                print(f"Error getting size for {src_path}: {e}")
                                file_size = 0

                            # 如果文件大小大于指定大小，移动文件
                            if file_size > min_size:
                                # 构建目标文件的完整路径
                                dest_path = os.path.join(dest_dir, file)

                                # 移动文件
                                shutil.move(src_path, dest_path)

                                if len(dest_path.split("-")) >= 4:
                                    r.set("max:file:" + user_folder, dest_path.split("-")[2])

                                # 打印移动信息
                                print(f'Moved: {src_path} -> {dest_path}, Size: {file_size} bytes')


# 例子：将 /path/user/media/xxx.cache 中的 .cache 文件移动到 /dest 文件夹下
source_directory = '/var/services/homes/super/x-download'
destination_directory = '/var/services/homes/super/x-download-max'

if __name__ == '__main__':
    move_cache_files(source_directory, destination_directory)
