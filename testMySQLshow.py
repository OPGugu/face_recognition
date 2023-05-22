import sys
import mysql.connector

def box(j,le):  #製作表格蓋子顯示(下面有範本)
    for i in range(0,le[j]):  #偵測出來的長度顯示多少"-"
        sys.stdout.write("-")
    j+=1  #表示完成一個項目的蓋子
    if j != 6:  #因為項目只有6項，j還沒加到6表示還不能結束
        sys.stdout.write("+--") #每一項開頭框
        return box(j,le)
    else:   #表示結束
        sys.stdout.write("+")  #最後框
        return
def name(name):
    list=['','','','','','']
    list2=['','','','','','']
    le=[0,0,0,0,0,0]
    p=""
    p1=""
    p2=""
    p3=""
    p4=""
    p5=""
    i=0
    a=''
    an=0
    list3=[]
    d=0
    conn = mysql.connector.connect (user='root', password='j2052',
                               host='localhost',buffered=True)  #登入MySQL
    cursor = conn.cursor()
    use = ("use A{}".format(name))  #選擇會員指令的字串
    select = ("select * from A{}".format(name)) #讀取資料指令的字串
    cursor.execute(use)  #輸入選會員的指令
    cursor.execute(select)  #輸入讀取資料的指令
#print "+---------------+--------+-----------------+---------+-------+------------------+"
#print "| name          | gender | telephonenumber | article | price | time             |"
#print "+---------------+--------+-----------------+---------+-------+------------------+"
    for row2 in cursor.fetchall():  #抓取會員的資料
        for e in range(0,6):  #偵測會員資料中的各項字串長度，並把各項目中最長的字串，取出來
            if len(row2[e]) < len(list2[e]):
                le[e]=len(list2[e])
            elif len(row2[e])>len(list2[e]):
                le[e]=len(row2[e])
                list2[e]=row2[e]
    cursor.execute(use)
    cursor.execute(select)
    for row in cursor.fetchall():
        sys.stdout.write("+--")  #上開頭框
        box(0,le)  #蓋上框
        print ""
        if len(row[0])<le[0]:   #為了讓第一項字串較短的也能對齊最長的，再後面給予空格
            le6=le[0]-len(row[0])
            if le6 !=0:
                p=""
                for l in range(0,le6):
                    p+=" "
        else:
            p=""
        if len(row[1])<le[1]:   #為了讓第二項字串較短的也能對齊最長的，再後面給予空格
            le1=le[1]-len(row[1])
            if le1 !=0:
                p1=""
                for l in range(0,le1):
                    p1+=" "
        else:
            p1=""
        if len(row[2])<le[2]:   #為了讓第三項字串較短的也能對齊最長的，再後面給予空格
            le2=le[2]-len(row[2])
            if le2 !=0:
                p2=""
                for l in range(0,le2):
                    p2+=" "
        else:
            p2=""

        if len(row[3])<le[3]:   #為了讓第四項字串較短的也能對齊最長的，再後面給予空格
            le3=le[3]-len(row[3])
            if le3 !=0:
                p3=""
                for l in range(0,le3):
                    p3+=" "
        else:
            p3=""
        if len(row[4])<le[4]:   #為了讓第五項字串較短的也能對齊最長的，再後面給予空格
            le4=le[4]-len(row[4])
            if le4 !=0:
                p4=""
                for l in range(0,le4):
                    p4+=" "
        else:
            p4=""
        if len(row[5])<le[5]:   #為了讓第六項字串較短的也能對齊最長的，再後面給予空格
            le5=le[5]-len(row[5])
            if le5 !=0:
                p5=""
                for l in range(0,le5):
                    p5+=" "
        else:
            p5=""
        print "|",row[0],"{}|".format(p), row[1],"{}|".format(p1), row[2],"{}|".format(p2), row[3],"{}|".format(p3), row[4],"{}|".format(p4), row[5],"{}|".format(p5) #顯示項目
    sys.stdout.write("+--")   #下開頭框
    box(0,le)  #蓋下框
    print "" #空一行
    print("+-----------------------+")
    print("|Maybe customer favorite|")
    print("+-----------------------+")
    # 顯示會員可能喜歡的商品(相同商品購買2個以上)
    find=("select article from A{}".format(name))  #從此會員的資料尋找商品名稱指令的字串
    cursor.execute(find)  #輸入從此會員的資料尋找商品名稱指令
    for art in cursor.fetchall():  #抓取會員的商品名稱，並計算有幾個(d)
        list3.append("{}".format(art[0]))
        d+=1
    cursor.execute(find)
    for art2 in cursor.fetchall(): #再抓一次會員的商品名稱
        w=0
        for f in range(0,d):  #計算重複的商品數量
            if art2[0] == list3[f]: #用現在抓取的資料比對剛才存起來的資料，有重複就+1(商品數量)
                 w+=1
                 list3[f]=""  #因為是重複的，所以刪掉，這樣迴圈就不會重複計算到
        if w>1:
            space=""
            for b in range(0,24-len(str(w))-2-len(art2[0])): #空格長度等於去掉商品數量的數字，再去掉左右的"|"，再去掉商品名稱長度
                space+=" "
            print("|{} {}{}|".format(w,art2[0],space))
    print("+-----------------------+")  #蓋下框(長25)
    cursor.close()
    return
