# -*- encoding=utf8 -*-
__author__ = "79230"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
import logging
from poco.exceptions import PocoNoSuchNodeException
import json,os,datetime,csv
from xpinyin import Pinyin
import shutil
import dingRobot
import traceback

sousuo="egf"  #搜索
sousuox="egu"  #搜索框 X
liebiao="e1w"   #商品列表
tupianx="bbm"   #图片 X
tupiancancel="f9o" #图片 取消
wancheng="b3i"  #完成
shangpinfanhui="bpp"    #商品页返回
zhutu="fnr" #主图
sava10="g72"    #保存10张
biaoti="f07"    #标题
jiage="g0_" #价格
xiaoliang="g6t" #销量
dianpu="fry"    #店铺
xiangqing1="dta"
xiangqing2="dtb"

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
from airtest.core.android.android import Android
from airtest.core.android.adb import ADB, AdbError, AdbShellError, DeviceConnectionError
device = Android()
currentDevice = device.get_default_device()
#device.install_app(r".\clipper.apk",True)
adb=ADB(currentDevice)
# a=shell("am broadcast -a clipper.get")
# print(a)

# generate html report
# from airtest.report.report import simple_report
# simple_report(__file__, logpath=True)

# text("RE")
def mk_dir_file(name, PcNum, path='D:\\pdd_goods'):
    year = str(datetime.datetime.now().year)
    if datetime.datetime.now().month < 10:
        month = '0'+str(datetime.datetime.now().month)
    else:
        month = str(datetime.datetime.now().month)
    if datetime.datetime.now().day < 10:
        day = '0'+str(datetime.datetime.now().day)
    else:
        day = str(datetime.datetime.now().day)
    if not os.path.exists(os.path.join(path, year)):
        year_path = os.path.join(path, year)
        os.makedirs(year_path)
        path = os.path.join(path, year)
    else:
        path = os.path.join(path, year)
    if not os.path.exists(os.path.join(path, month)):
        month_path = os.path.join(path, month)
        os.makedirs(month_path)
        path = os.path.join(path, month)
    else:
        path = os.path.join(path, month)
    if not os.path.exists(os.path.join(path, day)):
        day_path = os.path.join(path, day)
        os.makedirs(day_path)
        path = os.path.join(path, day)
    else:
        path = os.path.join(path, day)
    p = Pinyin()
    # path_taobao = str(PcNum)+'_pdd_'+p.get_pinyin(name, '')+int(time.time()*100)
    # if not os.path.exists(os.path.join(path, path_pdd)):
    #     path_pdd = os.path.join(path, path_pdd)
    #     os.makedirs(path_pdd)
    #     path = os.path.join(path, path_pdd)
    # else:
    #     path = os.path.join(path, path_pdd) #如果没有这个path则直接创建
    path = os.path.join(path, "%s_%s_%s_%s.csv" %
                        (pcNum, "pdd", p.get_pinyin(name, ""), day))
    return path

pcNum="X1"
searchName="灯具"
# 珠宝
# searchNameList = [
#         "黄金项链", "黄金吊坠 ", "黄金转运珠", "黄金戒指", "黄金手镯", "黄金手链/脚链", "黄金耳饰", "钻戒", "钻石项链/吊坠", "钻石手镯/手链", "钻石耳饰", "裸钻", "彩宝", "K金吊坠", "K金项链", "K金戒指", "K金手镯/手链/脚链", "K金耳饰", "铂金 ", "翡翠手镯",
#         "翡翠吊坠", "翡翠耳饰", "和田玉吊坠", "和田玉手链", "和田玉戒指", "珍珠项链 ", "珍珠手链", "珍珠耳饰", "珍珠戒指",
#         "水晶玛瑙手链", "水晶玛瑙项链", "水晶玛瑙耳饰", "水晶玛瑙戒指", "银手镯", "银项链", "银手链", "银戒指", "银耳饰", "宝宝银饰", "投资金", "投资银", "投资收藏"
#     ]
searchNameList = [ "灯罩灯", "台灯", "床头灯", "应急灯", "筒灯","射灯", "天花灯", "厨卫灯", "节能灯","荧光灯", "白炽灯", "路灯", "水晶灯", "过道灯", "中式灯", "阳台灯", "美式灯", "日式灯", "欧式灯", "韩式灯", "地中海灯", "儿童灯", "轨道灯", "镜前灯", "杀菌灯", "麻将灯", "庭院灯", "卫浴灯", "浴霸灯","吊灯","壁灯", "吸顶灯", "落地灯", "吊扇灯", "客厅灯","卧室灯","LED灯", "照明灯"]
for searchName in searchNameList:
    searchNameErrorNum=0
    searchNameNum=0
    dingRobot.sendText(str(datetime.datetime.now())+" 机器号：%s 拼多多 正在爬取关键字:%s"%(pcNum,searchName))
    if poco("com.xunmeng.pinduoduo:id/"+sousuox).exists():
        poco("com.xunmeng.pinduoduo:id/"+sousuox).click()        # X 清空输入框
    text(searchName)
    poco("com.xunmeng.pinduoduo:id/"+sousuo).click()            # 搜索
    csv_path = mk_dir_file(searchName, pcNum,)
    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["网站来源","商品ID", "店铺名称", "商品名称", "价格","销量", "评分", "url", "picUrl", "图片本地path","属性"])
    dir_path = os.path.dirname(csv_path)

    nowPageTitle=list()
    for num in range(1000):
        print(num,"page","debuginfo")
        #翻页
        swipeWhileNum=0
        while 1:
            goodsList=poco("com.xunmeng.pinduoduo:id/"+liebiao).child("android.widget.FrameLayout")
            # 商品列表 
            try:
                if poco("com.xunmeng.pinduoduo:id/"+tupianx).exists():       # 图片 X
                    poco("com.xunmeng.pinduoduo:id/"+tupianx).click()
                    continue
                if poco("com.xunmeng.pinduoduo:id/"+tupiancancel).exists():       # 图片 save 取消
                    poco("com.xunmeng.pinduoduo:id/"+tupiancancel).click()
                    continue
                if poco("com.xunmeng.pinduoduo:id/"+wancheng).exists():       # 完成
                    print("全部完成")
                    goodsList=[]
                    break
                if poco("com.xunmeng.pinduoduo:id/"+shangpinfanhui).exists():       #商品页 返回<
                    poco("com.xunmeng.pinduoduo:id/"+shangpinfanhui).click()
                    break
                if goodsList[0].offspring("com.xunmeng.pinduoduo:id/tv_title").get_text() in nowPageTitle:
                    poco("android:id/content").swipe("up")
                    swipeWhileNum+=1
                    if swipeWhileNum >=50:
                        print("全部完成")
                        goodsList=[]
                        break
                else:
                    nowPageTitle=list()
                    break
            except PocoNoSuchNodeException:
#                 if poco("com.xunmeng.pinduoduo:id/bs1").exists():
#                     poco("com.xunmeng.pinduoduo:id/bs1").click()
                print("PocoNoSuchNodeException swipe 124")
                poco("android:id/content").swipe("up")      # 获取标题失败往下滑
                start_app("com.xunmeng.pinduoduo")
                continue
                
        for n,i in enumerate(goodsList):
#             if poco("com.xunmeng.pinduoduo:id/d5d").child("android.widget.ImageView").exists():
#                 poco("com.xunmeng.pinduoduo:id/d5d").child("android.widget.ImageView").click()
#             if poco("com.xunmeng.pinduoduo:id/bcg").exists():
#                 poco("com.xunmeng.pinduoduo:id/bcg").click()
            if poco("com.xunmeng.pinduoduo:id/"+shangpinfanhui).exists():
                poco("com.xunmeng.pinduoduo:id/"+shangpinfanhui).click()        #商品页 返回<
            if n>1:
                #翻页问题 一次只获取前两个
                break
            try:
                shortTitle=i.offspring("com.xunmeng.pinduoduo:id/tv_title").get_text()
                nowPageTitle.append(shortTitle)
                i.offspring("com.xunmeng.pinduoduo:id/tv_title").click()
            except:
                print("get shortTitle failed")
                continue
                
            # 安装方式 风格按时间 风格按地域 工艺 颜色 形状 灯身材质 灯罩材质 场景 风格 
            try:
                # pic
                goodId=int(time.time()*100)
                poco("com.xunmeng.pinduoduo:id/"+zhutu).click()            #主图
                swipe((1200,200),(100,200))
                poco().long_click(duration=2.0)
                shell("rm -rf /storage/emulated/0/DCIM/Pindd/goods")
                poco("com.xunmeng.pinduoduo:id/"+sava10).click()            #保存10张
                time.sleep(3)
                p=Pinyin()
                pic_path=os.path.join(dir_path, "%s_%s_%s_%s"%
                            (pcNum, "pdd", p.get_pinyin(searchName, ""), goodId))
                os.mkdir(pic_path)
                try:
                    pic_list=list()
                    adb.pull("/storage/emulated/0/DCIM/Pindd/goods/",pic_path)
                    for root, dirs, files in os.walk(pic_path):
                        for n,name in enumerate(files):
                            path=os.path.join(root, name)
                            shutil.move(path,os.path.join(pic_path,"%s.jpg"%(n+1)))
                            pic_list.append(os.path.join(pic_path,"%s.jpg"%(n+1)).split("\\",1)[1])
                    shutil.rmtree(pic_path+"/goods")
                except:
                    print("图片保存失败,保存截屏，等待10分钟")
                    snapshot(filename=pic_path)
                    time.sleep(60*10)
                
                poco("com.xunmeng.pinduoduo:id/"+tupianx).click()            #图片 X

                title=poco("com.xunmeng.pinduoduo:id/"+biaoti).get_text()   #标题
                if "活动标签" in title:
                    title=title.split("活动标签")[1]
                if "退货包运费" in title:
                    title=title.split("退货包运费")[0]
                price=poco("com.xunmeng.pinduoduo:id/"+jiage).get_text()       #价格

            except Exception as e:
                traceback.print_exc()
                # dingRobot.sendText(str(datetime.datetime.now())+" 机器号：%s 拼多多 获取信息失败 %s"%(pcNum,repr(e)))
                continue
            # 销量
            if poco("com.xunmeng.pinduoduo:id/"+xiaoliang).exists():
                deal=poco("com.xunmeng.pinduoduo:id/"+xiaoliang).get_text()
            else:
                deal=''

            swipeNum=30
            while not poco("com.xunmeng.pinduoduo:id/"+dianpu).exists():            #店铺
                swipeNum-=1
                if swipeNum<=0:
                    break
                poco("android:id/content").swipe("up")
            try:
                shop_info=poco("com.xunmeng.pinduoduo:id/"+dianpu).get_text()       # 店铺
            except PocoNoSuchNodeException:
                shop_info="None"


            while not poco(text="商品详情").exists():     #属性 poco("com.xunmeng.pinduoduo:id/dy7").offspring(text="查看全部")
                swipeNum-=1
                if swipeNum<=0:
                    break
                poco("android:id/content").swipe("up")
            for swipenum in range(7):
                poco("android:id/content").swipe("up")

            try:
                good_info=dict()
                keys=poco("com.xunmeng.pinduoduo:id/"+xiangqing1)
                values=poco("com.xunmeng.pinduoduo:id/"+xiangqing2)
                for num,key in enumerate(keys):
                    good_info[key.get_text()]=values[num].get_text()
                # print(good_info)
                # print(shortTitle,title,price,shop_info,deal)
            except Exception as e:
                print(repr(e))
                continue



            d={
                "goodId":goodId,
                "title":title,
                "price":price,
                "shop_info":shop_info,
                "deal":deal,
                "good_info":good_info,
                "pic_path":json.dumps(pic_list)
            }

            if poco("com.xunmeng.pinduoduo:id/"+shangpinfanhui).exists():
                poco("com.xunmeng.pinduoduo:id/"+shangpinfanhui).click()        #商品页 返回<

            # 保存
            searchNameNum+=1
            with open(csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["拼多多",d["goodId"], d['shop_info'], d["title"],d['price'], d['deal'],'','','',d['pic_path'],d["good_info"]])
        

        if poco("com.xunmeng.pinduoduo:id/"+wancheng).exists() or swipeWhileNum >=10:
            print("全部完成")
            keyevent("KEYCODE_BACK")
            dingRobot.sendText(str(datetime.datetime.now())+" 机器号：%s 拼多多 关键字:%s爬取完成 成功%s条 失败%s条"%(pcNum,searchName,searchNameNum,searchNameErrorNum))
            break