#!/bin/env python
# -*- encoding:utf-8 -*-
import os
import platform
import subprocess
import sys
from time import sleep



class SysInfo(object):
    def __init__(self):
        self.sys_type = platform.system()

    def get_sys_type(self):
        if self.sys_type == "Windows":
            sys_version_tmp = platform.version()
            sys_version = sys_version_tmp.split('.')
            return self.sys_type + "-" + sys_version[0]
        elif self.sys_type == "Linux":
            cmd_shell = "cat /etc/os-release | grep ^NAME= | cut -d '\"' -f2"
            release = subprocess.getoutput(cmd_shell)
            return self.sys_type + "-" + release

    def get_sys_version(self):
        if self.sys_type == "Windows":
            version = platform.version()
        elif self.sys_type == "Linux":
            cmd_shell = "cat /etc/os-release | grep ^VERSION= | awk '{print $1}' | cut -d '\"' -f2"
            version = subprocess.getoutput(cmd_shell)
        else:
            version = "???"
        return version

    def get_sys_arch(self):
        result = platform.architecture()[0]
        if result == '32bit':
            return 32
        else:
            return 64

    def get_sys_machine(self):
        result = platform.machine()
        return result.lower()


sys_info = SysInfo()
sys_type = sys_info.get_sys_type()
sys_version = sys_info.get_sys_version()
sys_arch = sys_info.get_sys_arch()
sys_match = sys_info.get_sys_machine()
print("系统类型:", sys_info.get_sys_type(), "\n系统版本:", sys_version, "\n系统位数: %s位" % sys_arch, "\n系统架构:",
      sys_match)

sleep(1000)