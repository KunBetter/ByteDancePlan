import sys
import urllib.request
import json


def get_weather(city_name):
    city_code_dict = { \
        '北京': '101010100', '上海': '101020100', \
        '天津': '101030100', '重庆': '101040100', \
        }
    if len(city_name) == 0:
        print("city name is null")
        sys.exit()
    if city_name not in city_code_dict:
        print("city not exists")
        sys.exit()
    postal_code = city_code_dict[city_name]
    if postal_code.isdigit() == False:
        print("input is not number!")
        sys.exit()
    url = "http://www.weather.com.cn/data/cityinfo/" + postal_code + ".html"
    res = urllib.request.urlopen(url)
    content = res.read()
    # print content
    result_dict = json.loads(content)  # 从网页爬取的json转化成字典
    item = result_dict.get('weatherinfo')  # 取字典的值用get方法
    # print result_dict['weatherinfo']['city']
    print("%s    天气:%s,最高温度:%s,最低温度:%s" % (item.get('city'), \
                                           item.get('weather'), item.get('temp2'), item.get('temp1')))


if __name__ == '__main__':
    get_weather("上海")
