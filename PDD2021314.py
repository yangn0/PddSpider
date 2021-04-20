# -- coding: utf-8 --
from selenium import webdriver
from time import sleep
import time
import random
import os
import csv
import datetime
import requests
import datetime
from xpinyin import Pinyin


def login():
    sleep(30)
def drop_down(name):
    driver.implicitly_wait(5)
    save_path = mk_dir_file(name=name)
    js = "return action=document.body.scrollHeight"
    height = driver.execute_script(js)
    # 将滚动条调整至页面底部
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(5)
    #定义初始时间戳（秒）
    t1 = int(time.time())
    #定义循环标识，用于终止while循环
    status = True
    # 重试次数
    num=0
    while status:
        # 获取当前时间戳（秒）
        t2 = int(time.time())
        # 判断时间初始时间戳和当前时间戳相差是否大于30秒，小于30秒则下拉滚动条
        url_ver = "verification.htm"
        url_numal = "https://m.yangkeduo.com/search_result.html?search_key"
        for i in range(20, 35):
            currentPageUrl = driver.current_url
            if url_numal in currentPageUrl:
                if t2-t1 < i:
                    new_height = driver.execute_script(js)
                    if new_height > height:
                        time.sleep(random.randint(0, 5))
                        driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                        driver.implicitly_wait(5)
                        get_data()
                        # 重置初始页面高度
                        height = new_height
                        # 重置初始时间戳，重新计时
                        t1 = int(time.time())
                elif num < 3:                        # 当超过30秒页面高度仍然没有更新时，进入重试逻辑，重试3次，每次等待30秒
                    time.sleep(3)
                    num = num+1
                else:    # 超时并超过重试次数，程序结束跳出循环，并认为页面已经加载完毕！
                    print("滚动条已经处于页面最下方！")
                    driver.execute_script('window.scrollTo(0, 0)')#'window.scrollTo(0, 0)'
                    status = False
                    # 滚动条调整至页面顶部
            elif url_ver in currentPageUrl:
                print("程序需要认证啦")
                time.sleep(30)
                currentPageUrl_1 = driver.current_url
                if url_numal in currentPageUrl_1:
                    drop_down(name)
            else:
                print("程序出现其他异常，请重新开始爬取程序")
    new_data_list = []
    [new_data_list.append(i) for i in data_list if i not in new_data_list]
    #new_data_list.sort(key=(lambda x: [x[-2]]))
    #new_data_list.sort(key=data_list.index)
    write_data(name, save_path, new_data_list)
def get_data():
    year = str(datetime.datetime.now().year)
    if datetime.datetime.now().month < 10:
        month = '0'+str(datetime.datetime.now().month)
    else:
        month = str(datetime.datetime.now().month)
    if datetime.datetime.now().day < 10:
        day = '0'+str(datetime.datetime.now().day)
    else:
        day = str(datetime.datetime.now().day)
    print("开始解析数据")
    parent = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div[3]/div[1]/div')
    good_items = parent.find_elements_by_class_name('nN9FTMO2')
    count = 1
    for tag in good_items:
        try:
            pic_url = tag.find_element_by_tag_name('img').get_attribute('src')
            shop_info = tag.find_element_by_class_name('pHbSR-xp').text
            price = tag.find_element_by_class_name('_1aY0op01').text
            deal = tag.find_element_by_class_name('_2bStxP74').get_attribute('data-suffix')
            print(shop_info+"        "+str(price)+"           "+deal+"    "+pic_url)
            p = Pinyin()
            pic_save_path = 'goods'+'\\'+str(year)+'\\'+str(month)+'\\'+str(day)+'\\'+str(year+month+day)+'_pdd_'+(p.get_pinyin(product_name, ''))
            pic_save_path = os.path.join(pic_save_path, (str(count)+'\\'+str(count)+'.png'))
            data_list.append([shop_info, price, deal, pic_url, count, pic_save_path])
            count += 1
            # if shop_info not in data_list:
        except Exception as e:
            pass

def write_data(name, save_path, data):
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    p = Pinyin()
    with open(r"D:\goods\{}{}{}_pdd_{}.csv".format(year, month, day, p.get_pinyin(name, '')), "a", newline='') as file:
        writer = csv.writer(file)
        for i in data:
            writer.writerow(i)
            savePics(url=i[-3], count=i[-2], path=save_path)

def savePics(url, count, path):
    # 目录不存在，就新建一个
    try:
        a = str(count)
        if not os.path.exists(path+a):
            os.chdir(path)
            os.mkdir(a)
        #save_pic_path = os.path.join(path, product_name)
        save_pic_path = os.path.join(path, str(count))
        if not os.path.exists(save_pic_path+str(count)+'.png'):
            os.chdir(save_pic_path)
            image = requests.get(url)
            f = open(str(count)+'.png', 'wb')
            #将下载到的图片数据写入文件
            f.write(image.content)
            f.close()
    except Exception as e:
        print(e)
def mk_dir_file(name, path='D:\\goods'):

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
    date = year+month+day
    p = Pinyin()
    path_pdd = date+'_pdd_'+p.get_pinyin(name, '')
    if not os.path.exists(os.path.join(path, path_pdd)):
        path_pdd = os.path.join(path, path_pdd)
        os.makedirs(path_pdd)
        path = os.path.join(path, path_pdd)
    else:
        path = os.path.join(path, path_pdd) #如果没有这个path则直接创建
    return path

def main(name):#
    driver.get('https://m.yangkeduo.com')#file:///C:/Users/Liu/Desktop/pdd.html
    sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[1]/div/div/div').click()
    sleep(random.randint(1, 3))
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[1]/form/input').send_keys(name)
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[2]').click()
    #login()
    drop_down(name)


if __name__ == '__main__':
    #product_name = input("请输入需要爬取的商品名称：")
    product_name="灯具"
    data_list = []
    driver = webdriver.Chrome()
    main(name=product_name)