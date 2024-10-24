import requests


# url="https://www.12306.cn/index/script/core/common/station_name_new_v10065.js"
# a = requests.get(url, verify=False)
#
#
# with open("station_name_new_v10065.py", "wb") as f:
#     f.write(a.content)
#     f.close()


from station_name_new_v10065 import station_names

def get_station_key():
    station_dict={}
    new_name = station_names.split("|||")
    for x in new_name:
        if x == "":
            continue
        y = x.split('|')
        station_dict[y[1]] = y[2]
    return station_dict


def get_station_name():
    station_dict = {}
    new_name = station_names.split("|||")
    for x in new_name:
        if x == "":
            continue
        y = x.split('|')
        station_dict[y[2]] = y[1]
    return station_dict



