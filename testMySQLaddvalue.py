import face_recognition_knn
import testMySQLshow
import sys
import mysql.connector
import time

def name(name):
    conn = mysql.connector.connect (user='root', password='j2052',
                                   host='localhost',buffered=True) #登入MySQL
    cursor = conn.cursor()
    use = ("use A{}".format(name))  #選擇會員的指令的字串
    select = ("select * from A{}".format(name)) #讀取資料指令的字串
    cursor.execute(use)  #輸入選會員的指令
    cursor.execute(select)  #輸入讀取資料的指令
    for row in cursor.fetchall(): #抓取會員的資料(但只會用到姓名性別電話)
        continue
    t= time.strftime("%Y/%m/%d %H:%M", time.localtime())  #抓取輸入時間
    article=raw_input("Enter article:")  #輸入商品名稱
    if article=='exit':  #如果輸入的是exit，就結束新增商品
        cursor.close()
        return
    price=raw_input("Enter price:")  #輸入商品價格
    if price=='exit':  #如果輸入的是exit，就結束新增商品
        cursor.close()
        return
    else:
        while True:  #將剛剛輸入的商品資料丟進MySQL，並循環輸入商品，直到輸入exit離開
            insert=("insert into A{}(name,gender,telephonenumber,article,price,time) value('{}','{}','{}','{}','{}','{}')".format(name,row[0],row[1],row[2],article,price,t))
            cursor.execute(insert)
            conn.commit()
            testMySQLshow.name(name)  #顯示會員資料
            article=raw_input("Enter article:")
            if article=='exit':  #如果輸入的是exit，就結束新增商品
                cursor.close()
                break
            price=raw_input("Enter price:")
            if price=='exit':  #如果輸入的是exit，就跳出新增商品的迴圈
                cursor.close()
                break

