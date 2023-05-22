import testMySQLshow
import testMySQLaddvalue
import sys
import mysql.connector
import time

def name(name):
    conn = mysql.connector.connect (user='root', password='j2052',
                                   host='localhost',buffered=True) #登入MySQL
    cursor = conn.cursor()
    t= time.strftime("%Y/%m/%d %H:%M", time.localtime()) #抓輸入時間
    value=raw_input("Enter name:") #輸入顧客名稱
    gender=raw_input("Enter gender:")  #輸入性別
    telephonenumber=raw_input("Enter telephonenumber:")  #輸入電話號碼
    article=raw_input("Enter article:") #輸入商品名稱
    price=raw_input("Enter price:")  #輸入商品價格
    #接下來是將剛才輸入的資料弄成MySQL指令用的字串
    table=("create table A{}(name char(20),gender char(15),telephonenumber char(15),article char(100),price char(100),time char(100))".format(name))
    table2=("insert into A{}(name,gender,telephonenumber,article,price,time) value('name','gender','telephonenumber','article','price','time')".format(name))
    insert=("insert into A{}(name,gender,telephonenumber,article,price,time) value('{}','{}','{}','{}','{}','{}')".format(name,value,gender,telephonenumber,article,price,t))
    databases = ("create database A{}".format(name))
    use=("use A{}".format(name))
    #將剛剛的指令輸入進MySQL
    cursor.execute(databases)
    cursor.execute(use)
    cursor.execute(table)
    cursor.execute(table2)
    cursor.execute(insert)
    conn.commit()
    cursor.close() #先結束MySQL，不然會一直卡在輸入指令的地方
    testMySQLshow.name(name)  #顯示會員資料
    next=raw_input("Do you continue add new article?(y/n)")  #詢問是否繼續加入商品
    if next =='n': #輸入n，結束
        return
    elif next=='y': #輸入y，新增購買商品
        testMySQLaddvalue.name(name)
        return
