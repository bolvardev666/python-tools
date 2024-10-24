from time import sleep
import requests,urllib3
from urllib3.exceptions import InsecureRequestWarning
from colorama import Fore,Style
from header import header
from _test import get_station_name,get_station_key


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from 接口自动化.station_name_new_v10065 import station_names

station_key = get_station_key()
station_name = get_station_name()

prefix = 'https://kyfw.12306.cn/otn/leftTicket/query?'
start_time = "leftTicketDTO.train_date=" + "2024-10-24"
from_station = f"leftTicketDTO.from_station={station_key['南京南']}"
to_station = f"leftTicketDTO.to_station={station_key['杭州东']}"
purpose_codes = "purpose_codes=ADULT"
while True:
    GET12306_query = f"{prefix}{start_time}&{from_station}&{to_station}&{purpose_codes}"
    try:
        res = requests.get(GET12306_query, timeout=10, verify=False, headers=header)
        if res.status_code != 200:
            print("Failed to get 12306 data")
            exit(1)
    except InsecureRequestWarning as e:
        pass

    data = res.json()
    trains = data['data']['result']
    for x in trains:
        tmp = x.split("|")
        # print(tmp)
        # print(tmp[10])
        if tmp[32] == '': tmp[32] ="无"
        if tmp[31] == '': tmp[31] = "无"
        if tmp[30] == '': tmp[30] = "无"
        if tmp[26] == '': tmp[26] = "无"
        if tmp[30] == "无":
            print(
                f"车次：{tmp[3]}\t出发站：{station_name[tmp[6]]}\t\t目的地：{station_name[tmp[7]]}\t\t出发时间：{tmp[8]}\t到达时间：{tmp[9]}\t历时：{tmp[10]}\t商务座：{tmp[32]}\t一等座：{tmp[31]}\t二等座：{tmp[30]}\t无座：{tmp[26]}")
        else:
            print(f"车次：{tmp[3]}\t出发站：{station_name[tmp[6]]}\t\t目的地：{station_name[tmp[7]]}\t\t出发时间：{tmp[8]}\t到达时间：{tmp[9]}\t历时：{tmp[10]}\t商务座：{tmp[32]}\t一等座：{tmp[31]}\t二等座：{Fore.GREEN + tmp[30] + Style.RESET_ALL}\t无座：{tmp[26]}")

    print(f"共计班次：{len(trains)}")

    sleep(10)

# https://kyfw.12306.cn/lcquery/query?train_date=2024-10-23&from_station_telecode=NKH&to_station_telecode=UUH&result_index=0&can_query=Y&isShowWZ=Y&sort_type=2&purpose_codes=00&is_loop_transfer=S&channel=E&_json_att=
