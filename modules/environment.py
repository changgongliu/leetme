# !/usr/bin/Python
# -*- coding:utf-8 -*-
import os

## 返回目标机器所有的环境变量
def run(**args):
    print "[*] In environment module"
    return str(os.environ)
