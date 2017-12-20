import requests
import re
from pprint import pprint

def main():
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9035';
    r = requests.get(url,verify = False)
    pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
    result = re.findall(pattern,r.text)

    print(dict(result).keys())
    print(dict(result).values())

if __name__=='__main__':
    main()
