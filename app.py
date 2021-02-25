# coding=utf-8
import nothing as nothing
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
###21210203 Deployee到heroku成功pta2

auth_json_path = 'P-TA-702e4ead397e.json'
gss_scopes = ['https://spreadsheets.google.com/feeds']

# 連線
credentials = ServiceAccountCredentials.from_json_keyfile_name(auth_json_path, gss_scopes)
gss_client = gspread.authorize(credentials)
# 開啟 Google Sheet 資料表
spreadsheet_key_109fall = '1UROGY5ZJyO8NXZsV0pD5OK9xzqm0bg9lEto0V9qq-E0'
spreadsheet_key = '1V4uWY8Hyyho0AnBmDlW7Yq5QznFuGKxY6KQ_GYzoKe8'
'''
當需要連結一新表單時
1u4-k9auXaFgaYFA3kfQbp57AfF_fQUVKMbkHwSvyqng  
1. 更改spreadsheet_key(來自網址) https://docs.google.com/spreadsheets/d/<<1UROGY5ZJyO8NXZsV0pD5OK9xzqm0bg9lEto0V9qq-E0>>/edit#gid=0
2. 然後把p-ta-sheet@p-ta-271611.iam.gserviceaccount.com 加為編輯者
3.deploy pta3 with Github Desktop

'''


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('9BPCyvDVuIWXpWh1JbDJ6mEBb/XmxQD1P+YQU1F7j++6ZPaT6RSDiPjEXK7BdM04jzP2qal7kgHlXQGjqg7EhYwke5Rw+2xjG0SHyqyv/W9NX2NZMS0pW4Rl7TzFknj+l3CyIXF6x+5pQ3BDfUFItAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('d89bbe9d16737bc78c5e293daacb5ca9')
#d89bbe9d16737bc78c5e293daacb5ca9



# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@app.route('/home', methods=['GET'])
def homepage():
    return 'Hello, World!'


def add_point(RECEIVE):  # 之後要判斷資料庫中是否有此人
    ID = RECEIVE[0:9]
    sheet = gss_client.open_by_key(spreadsheet_key).worksheet('Bonus')
    add_count_plus = int(sheet.cell(95, 2).value)
    Date_Index = add_count_plus+3
    if "+" in RECEIVE:
        if "b" or "B" in RECEIVE:
            List_id = sheet.col_values(1)  # 讀取第2欄的一整欄
            List_name = sheet.col_values(3)  # 讀取第3欄的一整欄
            Student_Index = List_id.index(ID.capitalize()) #找這個人在哪
            if sheet.cell(Student_Index+1, Date_Index).value == "0":
                sheet.update_cell(Student_Index+1, Date_Index, RECEIVE[RECEIVE.find("+") + 1])
                return "優秀的"+List_name[Student_Index] + "今天加了" + RECEIVE[RECEIVE.find("+") + 1] + "分，成為同學們的典範。"
            else:
                return List_name[Student_Index]+"今天已經登記過了!"

    else:
        return "加分的格式如下\nExample: b10812019 +5\n請按格式輸入!不要亂打!"

def look_score(RECEIVE):  # 之後要判斷資料庫中是否有此人
    Name = RECEIVE[2:5]
    sheet = gss_client.open_by_key(spreadsheet_key).worksheet('Exam')
    add_count_plus = 18  #第三次小考


    List_name = sheet.col_values(3)  # 讀取第3欄的一整欄
    List_Score = sheet.col_values(4+add_count_plus-1)  # 讀取成績欄
    List_Score_total = sheet.col_values(4 + add_count_plus )  # 讀取成績欄
    #List_Checked = sheet.col_values(4 + add_count_plus +4)  # 讀取已查欄
    List_Checked = sheet.col_values(4 + 4 + 4)  # 讀取已查欄
    Student_Index = List_name.index(Name) #找這個人在哪



    if List_Checked[Student_Index] == "0": #還沒查成績
        sheet.update_cell(Student_Index + 1, 4 + 4 +4, "1")
        if int(List_Score_total[Student_Index]) < 60 :
            return RECEIVE[3:5]+"你的第四次小考" + List_Score[Student_Index] + "分，\n本學期總成績為"+ List_Score_total[Student_Index] +"\n今年9月見囉~"
        else:
            return RECEIVE[3:5]+"你的第四次小考" + List_Score[Student_Index] + "分，\n本學期總成績為"+ List_Score_total[Student_Index] + "\n恭喜老爺賀喜夫人!"
    else:
        return Name + "你查過了啦! 阿你是要查幾遍啦!?\n(如果你其實沒有查過，請告知宜運助教~)"



# GLOBAL
mode = "一般"
ID = "M10812019"
GID_stu =  "Ceb359316111f7cf2b022ce1a31579193"
GID_tch =  "Ceb359316111f7cf2b022ce1a31579193"
GID_FAT =  "C7891f464a14727a3655e23cd4d161ffd"
GID_noko0 = "C536a63270b1471342e92c624ba3e27e6"
GID_noko = "Cf35077badae654eee6be5536ab529121" #109學年大群
GID_Test = "C536a63270b1471342e92c624ba3e27e6" #測試

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global mode
    RECEIVE = event.message.text
   # TALKER = event.message.

    Y = time.struct_time.tm_year
    M = time.struct_time.tm_mon
    D = time.struct_time.tm_mday

    if mode == "加分":
        if "/enddd" == RECEIVE:
            mode = "一般"
            try:
                line_bot_api.push_message(GID_noko, TextSendMessage(text="========加分截止線========"))
            except LineBotApiError as e:
                # error handle
                raise e

            REPLY = "回到一般模式"
        else:
            REPLY = add_point(RECEIVE)

    elif mode == "一般":
        if "/addd" == RECEIVE: #轉換成加分模式的瞬間
            mode = "加分"
            sheet = gss_client.open_by_key(spreadsheet_key).worksheet('Bonus')
            add_count = int(sheet.cell(95, 2).value)
            sheet.update_cell(95, 2, str(add_count+1))
            sheet.update_cell(1, str(add_count+1+3), time.strftime("%m月%d日",time.localtime()))
            REPLY = time.strftime("加分模式已啟動!今天是%y/%m/%d(%a)\n第"+str(add_count+1)+"次加分", time.localtime())
            try:
                line_bot_api.push_message(GID_noko, TextSendMessage(text='請剛剛上課的同學按照:\n   學號 + 幾分\n的格式告訴我你要加幾分\n範例:\nb10912019 +5\n當我回復時才代表有成功喔~'))
            except LineBotApiError as e:
                # error handle
                raise e
        elif '這位是新來的物理助教' == RECEIVE:
            sheet = gss_client.open_by_key(spreadsheet_key).worksheet('Bonus')
            sheet.update_cell(97, 2,  event.source.group_id)
            #sheet.update_cell(97, 5,  line_bot_api.get_room_member_profile(GID_noko)('user_id'))
            REPLY = '各位同學好! 我對你們的要求只有三件事:白天工作，晚上讀書，假日批判喔!'

        elif 'QA' in RECEIVE:
            #mode = "QA"
            sheet_QA_tody = gss_client.create_by_key(spreadsheet_key)("Python測試用模板", parent_id="1l-RT4KyPTG2Jt_s9jmMXHqmgo0h7xLTv")
            #sheet_QA = gss_client.open_by_key(spreadsheet_key).worksheet('QA')
            sheet_Bonus = gss_client.open_by_key(spreadsheet_key).worksheet('Bonus')
            #QA_count_tody = int(sheet_QA.cell(95, 2).value)
            #sheet.update_cell(97, 5,  line_bot_api.get_room_member_profile(GID_noko)('user_id'))
            REPLY = '各位同學好! 我對你們的要求只有三件事:白天工作，晚上讀書，假日批判喔!'


        elif "/say" in RECEIVE: #宣布事項到群組(回復老師)
            try:
                line_bot_api.push_message(GID_tch, TextSendMessage(text=RECEIVE[4:]))
            except LineBotApiError as e:
                # error handle
                raise e
        elif "/not" in RECEIVE: #宣布事項到群組(助教用)
            try:
                line_bot_api.push_message(GID_noko, TextSendMessage(text= RECEIVE[5:]))
            except LineBotApiError as e:
                # error handle
                raise e
        elif "/fat" in RECEIVE: #宣布事項到群組(肥宅動起來)
            try:
                line_bot_api.push_message(GID_FAT, TextSendMessage(text=RECEIVE[4:]))
            except LineBotApiError as e:
                # error handle
                # Cbe5130080e22bb10fa1808e05bdb7572
                raise e
        elif "成績" in RECEIVE:
            try:
                REPLY = look_score(RECEIVE)
            except LineBotApiError as e:
                # error handle
                # Cbe5130080e22bb10fa1808e05bdb7572
                raise e
        elif "/looking" in RECEIVE:
            try:
                line_bot_api.push_message(GID_noko, TextSendMessage(text="第二次小考開放查成績囉~ 請同學私我(量子物理大師)查成績! 跟我說話時，請按照以下格式:\n\n我是xxx，我要查成績!\n\n記住喔!成績我只會說一次，請自己查自己的，請不要偷查暗戀ㄉ人ㄉ成績，謝些!"))
            except LineBotApiError as e:
                # error handle
                # Cbe5130080e22bb10fa1808e05bdb7572
                raise e
        else:
            nothing



    message = TextSendMessage(REPLY)
    line_bot_api.reply_message(event.reply_token, message)

    # 建立工作表3
    # sheet = gss_client.open_by_key(spreadsheet_key).sheet1

    # 自定義工作表名稱


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))#5000
    app.run(host='0.0.0.0', port=port)
    #每次重啟ngrok伺服器，要去 https://developers.line.biz/console/channel/1653931127/messaging-api 改一下Webhook URL
    #記得用https那個

'''
  # Google Sheet 資料表操作(舊版)
    #sheet.clear()  # 清除 Google Sheet 資料表內容
    listtitle = ["姓名", "電話"]
    #sheet.append_row(listtitle)  # 標題
    listdata = ["Liu", "0912-345678"]
    #sheet.append_row(listdata)  # 資料內容
    # Google Sheet 資料表操作(20191224新版)
    sheet.update_acell('G2', 'ABC')  # D2加入ABC
    #sheet.update_cell(2, 4, 'ABC')  # D2加入ABC(第2列第4行即D2)
    # 寫入一整列(list型態的資料)
    values = ['A', 'B', 'C', 'D']
    #sheet.insert_row(values, 1)  # 插入values到第1列
    # 讀取儲存格
    sheet.acell('B1').value
    sheet.cell(1, 2).value
    # 讀取整欄或整列
    sheet.row_values(1)  # 讀取第1列的一整列
    sheet.col_values(1)  # 讀取第1欄的一整欄
    # 讀取整個表
    sheet.get_all_values()
    '''
