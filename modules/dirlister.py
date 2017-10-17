# !/usr/bin/Python
# -*- coding:utf-8 -*-
import os

##返回目标机器目录
def run(**args):
    print "[*] in dirlister module."
    files = os.listdir(".")
    return str(files)
