# -*- encoding=utf8 -*-
__author__ = "79230"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
import logging
from poco.exceptions import PocoNoSuchNodeException
import json,time,os
#logging.basicConfig(level=logging.NOTSET)  # 设置日志级别
#logger = logging.getLogger("debuginfo")
# logger = logging.getLogger("airtest")
# logger.setLevel(logging.ERROR)
_print = print
def print(*args, **kwargs):
    _print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), *args, **kwargs)


from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# script content
print("start...")


# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)

# text("499772")

nowPageTitle=list()
for num in range(100):
    print(num,"page","debuginfo")
    #翻页
    while 1:
        goodsList=poco("android:id/content").offspring("com.xunmeng.pinduoduo:id/b1c").offspring("com.xunmeng.pinduoduo:id/ay4").offspring("com.xunmeng.pinduoduo:id/e8t").child("android.widget.FrameLayout")
        try:
            if poco("com.xunmeng.pinduoduo:id/b3y").exists():                
                break
            if goodsList[0].offspring("com.xunmeng.pinduoduo:id/tv_title").get_text() in nowPageTitle:
                poco("android:id/content").swipe("up")
            else:
                nowPageTitle=list()
                break
        except PocoNoSuchNodeException:
            if poco("com.xunmeng.pinduoduo:id/bs1").exists():
                poco("com.xunmeng.pinduoduo:id/bs1").click()
            poco("android:id/content").swipe("up")
            continue


    for n,i in enumerate(goodsList):
        if poco("com.xunmeng.pinduoduo:id/bs1").exists():
            poco("com.xunmeng.pinduoduo:id/bs1").click()
        if n>1:
            #翻页问题 后两个不要
            break
        
        try:
            shortTitle=i.offspring("com.xunmeng.pinduoduo:id/tv_title").get_text()
            nowPageTitle.append(shortTitle)
            # 遍历目录
            flag=0
            for a,b,listJsonFile in os.walk('./data/'):
                if shortTitle+".json" in listJsonFile:
                    flag=1
                    continue
            if flag==1:
                continue
        except:
            print("shortTitle failed")
            continue
        
        i.offspring("com.xunmeng.pinduoduo:id/tv_title").click()

        try:
            title=poco("android:id/content").offspring("com.xunmeng.pinduoduo:id/cvc").offspring("com.xunmeng.pinduoduo:id/fat")[0].get_text()
            price=poco("com.xunmeng.pinduoduo:id/gd6").get_text()
        except PocoNoSuchNodeException:
            continue
        if poco("com.xunmeng.pinduoduo:id/gjv").exists():
            deal=poco("com.xunmeng.pinduoduo:id/gjv").get_text()
        elif poco("com.xunmeng.pinduoduo:id/g29").exists():
            deal=poco("com.xunmeng.pinduoduo:id/g29").get_text()
        elif poco("com.xunmeng.pinduoduo:id/g27").exists():
            deal=poco("com.xunmeng.pinduoduo:id/g27").get_text()
            
        swipeNum=30
        while not poco("com.xunmeng.pinduoduo:id/g5e").exists():
            swipeNum-=1
            if swipeNum<=0:
                break
            poco("android:id/content").swipe("up")
        try:
            shop_info=poco("com.xunmeng.pinduoduo:id/g5e").get_text()
        except PocoNoSuchNodeException:
            shop_info="None"
        
        print(shortTitle,title,price,shop_info,deal)
        

        d={
            "title":title,
            "price":price,
            "shop_info":shop_info,
            "deal":deal,
        }
        
        poco("com.xunmeng.pinduoduo:id/bs1").click()

        with open ("data/%s.json"%(shortTitle),"w+") as f:
            json.dump(d,f)
    if poco("com.xunmeng.pinduoduo:id/b3y").exists():
        print("全部完成")
        break
    






