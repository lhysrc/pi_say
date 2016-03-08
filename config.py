# coding=utf-8
BaiDu_YuYin_TOKEN = '24.33e501655ef8a7bd71c019a5c174e800.2592000.1459786598.282335-4814376'
BaiDu_YuYin_API_KEY = "EuWCMZ8mC73R2QimNR5cFkGn"
BaiDu_YuYin_SECRET_KEY = "Yw2wsHC82pPeRCQM5EWjEB263wjDirCU"

BaiDu_API_STORE_API_KEY = '6aaa80cda8ee541ad53047b6ce6b8468'

Holiday_2016 = [
                   (4, 2), (4, 3), (4, 4),
                   (4, 30), (5, 1), (5, 2),
                   (6, 9), (6, 10), (6, 11),
                   (9, 15), (9, 16), (9, 17),
               ] + [(10, i) for i in range(1, 8)]
WorkdayInWeekend_2016 = [
    (6, 12), (9, 18), (10, 8), (10, 9)
]
# 节日	时间	调休上班	天数
# 元旦	1/1-1/3	与周末连休	3天
# 春节	2/7-2/13	2月6日、14日上班	7天
# 清明节	4/2-4/4	与周末连休	3天
# 劳动节	4/30-5/2	5月2日补休	3天
# 端午节	6/9-6/11	6月12日上班	3天
# 中秋节	9/15-9/17	9月18日上班	3天
# 国庆节	10/1-10/7	10月8日、9日上班	7天
