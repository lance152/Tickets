"""
Usage:
    tickets.py [-dgztk] <from> <to> <date>

Options:
    -h --help Show help
    -d  动车
    -g  高铁
    -z  直达
    -t  特快
    -k  快速
"""

from docopt import docopt
import stations
import requests
from prettytable import PrettyTable
from colorama import Fore

def cli():
    arguments = docopt(__doc__, version='tickets 1.0')
    from_station = stations.get_telecode(arguments.get('<from>'))
    to_station = stations.get_telecode(arguments.get('<to>'))
    date = arguments.get('<date>')
    options = ''.join([key for key,value in arguments.items() if value is True])
    url = ('https://kyfw.12306.cn/otn/leftTicket/query?'
           'leftTicketDTO.train_date={}&'
           'leftTicketDTO.from_station={}&'
           'leftTicketDTO.to_station={}&'
           'purpose_codes=ADULT').format(date,from_station,to_station)
    r = requests.get(url,verify=False)
    raw_trains = r.json()['data']['result']
    x = PrettyTable()
    x._set_field_names(['车次','出发车站／到达车站','始发车站/到达车站','时间','历时', '商务座', '一等座', '二等座', '高级软卧', '软卧', '动卧', '硬卧', '软座', '硬座', '无座'])
    for raw_train in raw_trains:
        data_list = raw_train.split('|');
        train_no = data_list[3]
        initial = train_no[0].lower()
        from_station_code = data_list[4]
        to_station_code = data_list[5]
        from_station_u = data_list[6]
        to_station_u = data_list[7]
        start_time = data_list[8]
        arrive_time = data_list[9]
        duration = data_list[10]
        swz = data_list[32] or '--'
        first = data_list[31] or '--'
        second = data_list[30] or '--'
        gaojirw = data_list[21] or '--'
        ruanw = data_list[23] or '--'
        yingw = data_list[28] or '--'
        dongwo = data_list[33] or '--'
        ruanz = data_list[24] or '--'
        yingz = data_list[29] or '--'
        wuzuo = data_list[26] or '--'
        if initial in options:
            x.add_row([train_no,
                       '\n'.join([Fore.GREEN + stations.get_name(from_station_u) + Fore.RESET,
                                  Fore.RED + stations.get_name(to_station_u) + Fore.RESET]),
                       '\n'.join([Fore.GREEN + stations.get_name(from_station_code) + Fore.RESET,
                                  Fore.RED + stations.get_name(to_station_code) + Fore.RESET]),
                       '\n'.join([Fore.GREEN + start_time + Fore.RESET,
                                  Fore.RED + arrive_time + Fore.RESET]),
                       duration,
                       swz,
                       first,
                       second,
                       gaojirw,
                       ruanw,
                       yingw,
                       dongwo,
                       ruanz,
                       yingz,
                       wuzuo])
    print(x)
if __name__=='__main__':
    cli()