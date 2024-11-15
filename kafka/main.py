import json
import platform, psutil, subprocess
from time import sleep


class GetSysInfo:
    def __init__(self):
        """
        flag: 占位符,没啥用 | 为了用类归档相同的方法同时让pycharm不提示
        """
        self.flag = 0

    def sys_releases(self):
        self.flag = 1
        sys_type = platform.system()
        if sys_type == 'Darwin':
            pass
        elif sys_type == 'Linux':
            pass
        elif sys_type == 'Windows':
            return {
                "system_release": f"{sys_type}-{platform.release()}"
            }

    def sys_cpu(self):
        self.flag = 2
        tmp = subprocess.run("cat /proc/cpuinfo  | grep name | uniq | cut -d ':' -f2", shell=True, capture_output=True)
        cpu_name = tmp.stdout.decode("utf-8").strip('\n').strip('^ ')
        return {
            "cpu_model": cpu_name,
            "cpu_core": psutil.cpu_count(logical=False),
            "cpu_process": psutil.cpu_count(logical=True),
            "cpu_max_mhz": f"{int(psutil.cpu_freq().max)} MHz"
        }

    def sys_memory(self):
        self.flag = 3
        return {
            "mem_total": f"{(psutil.virtual_memory().total / 1024 / 1024 / 1024):.1f} GB",
            "mem_used": f"{(psutil.virtual_memory().used / 1024 / 1024 / 1024):.1f} GB",
            "mem_free": f"{(psutil.virtual_memory().free / 1024 / 1024 / 1024):.1f} GB"
        }

    def sys_disk(self):
        self.flag = 4
        disk_list = psutil.disk_partitions()
        i = len(disk_list)
        j = 1
        result = {
            "disk_total": len(disk_list),
        }
        for x in disk_list:
            result[f"part {j}"] = {
                "disk_mount": x.mountpoint,
                "disk_type": x.fstype,
            }
            j = j + 1
            return result

    def sys_all(self):
        self.flag = 5
        return [
            self.sys_releases(),
            self.sys_cpu(),
            self.sys_memory(),
            self.sys_disk()
        ]


class GetRunSource:
    def __init__(self):
        self.flag = 0
        pass

    def use_cpu(self):
        self.flag = 1
        return {
            "cpu_use": int(psutil.cpu_percent())
        }


def thread_poll1():
    get_sys_info = GetSysInfo()
    print("start thread1")
    while True:
        print(get_sys_info.sys_all())
        sleep(60)

def thread_poll2():
    get_run_source = GetRunSource()
    print("start thread2")
    while True:
        print(get_run_source.use_cpu())
        sleep(5)

if __name__ == '__main__':
    import threading
    thread1 = threading.Thread(target=thread_poll1)
    thread2 = threading.Thread(target=thread_poll2)
    thread1.start()
    thread2.start()

#
# test = GetSysInfo()
# print(test.sys_all())