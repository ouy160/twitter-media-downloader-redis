current_date=$(date +\%Y\%m\%d)
nohup python /var/services/homes/super/project/twitter-downloader/twitter-media-downloader.py -x 5 > /var/services/homes/super/project/twitter-downloader/log/out.$current_date.log 2> /var/services/homes/super/project/twitter-downloader/log/error.$current_date.log &

