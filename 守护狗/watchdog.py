import json
import os.path
import getpass
from time import sleep
import datetime
from crontab import CronTab

json_path = './conf.json'
poll_time = 10  # crontab 10分钟检查一次
cron_time = 1


def load_json_data():
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


def init_watchdog():
    user_name = getpass.getuser()
    this_file = os.path.abspath(__file__)
    cron_str = f"python3 {this_file}"
    print(f"文件路径:{this_file}\n用户名:{user_name}\n添加cron计划:{cron_str}")

    sys_cron = CronTab(user=user_name)
    job = sys_cron.new(command=cron_str)
    job.minute.every(cron_time)
    sys_cron.write()
    create_flag()   #一个标识


def check_service(data: dict):
    service = []
    for service_name in data:
        service.append(service_name)
    for ser in service:
        print(f"check service {ser}")
        start = data[ser]['start']
        stop = data[ser]['stop']
        check = data[ser]['check']
        exec_command(ser, check, start, stop)
        sleep(poll_time)


def exec_command(name: str, check: str, start: str, stop: str):
    res = os.system(check)
    if res != 0:
        os.system(stop)
        os.system(start)
        time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        print(f"{time}--->服务[{name}]检查失败,执行重启")
        return False
    else:
        time = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        print(f"{time}--->服务[{name}]检查正常")
        return True


def create_flag():
    time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    with open('./.flag', 'w') as f:
        f.write(f"{time}--->create crontab")


if __name__ == '__main__':
    if os.path.exists('./.flag'):
        print("计划任务存在,不再创建")
    else:
        init_watchdog()
    print("开始执行服务检测")
    check_service(load_json_data())
