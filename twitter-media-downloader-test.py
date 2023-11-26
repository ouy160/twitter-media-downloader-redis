import os
import shutil

from common.redisCli import getConnection

r = getConnection()


def move_cache_files(src_dir, dest_dir):
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
                        # 检查文件是否为 .cache 文件
                        if file.endswith('.cache'):
                            parts = file.split('-')
                            if len(parts) == 4:
                                extracted_value = parts[2]
                                r.set('cache:' + user_folder, extracted_value)

                            # 构建源文件的完整路径
                            src_path = os.path.join(media_folder_path, file)

                            # 构建目标文件的完整路径
                            dest_path = os.path.join(dest_dir, file)

                            # 移动文件
                            shutil.move(src_path, dest_path)
                            print(f'Moved: {src_path} -> {dest_path}')


# 例子：将 /path/user/media/xxx.cache 中的 .cache 文件移动到 /dest 文件夹下
source_directory = '/var/services/homes/super/x-download'
destination_directory = '/var/services/homes/super/x-download-cache'

if __name__ == '__main__':
    move_cache_files(source_directory, destination_directory)
