from flask import Flask, request
from linebot.models import *
from linebot import *
import json
import requests

app = Flask(__name__)

line_bot_api = LineBotApi('XXXXXXXX')
handler = WebhookHandler('XXXXXXXX')


@app.route('/getimage', methods=['GET'])
def get_image():
    filename = BASE_DIR + "promote2-10sec (1).gif"
    return send_file(filename) ,200


@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_data(as_text=True)
    # print(body)
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"] 
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text'] 
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name

    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)
    
    reply(intent,text,reply_token,id,disname)

    return 'OK'
    
    
def reply(intent,text,reply_token,id,disname):
    if intent == 'Covid 19':
        data = requests.get('http://covid19.th-stat.com/json/covid19v2/getTodayCases.json')
        json_data = json.loads(data.text)
        
        Confirmed = json_data['Confirmed']  # ติดเชื้อสะสม
        Recovered = json_data['Recovered']  # หายแล้ว
        Hospitalized = json_data['Hospitalized']  # รักษาอยู่ใน รพ.
        Deaths = json_data['Deaths']  # เสียชีวิต
        NewConfirmed = json_data['NewConfirmed']  # บวกเพิ่ม
        text_message = TextSendMessage(
            text='โควิดวันนี้\nติดเชื้อสะสม = {} คน(+เพิ่ม{})\nหายแล้ว = {} คน\nรักษาอยู่ใน รพ. = {} คน\nเสียชีวิต = {} คน'.format(
                Confirmed, NewConfirmed, Recovered, Hospitalized, Deaths))

        print("data",data)
        print("text_message-->",text)
        line_bot_api.reply_message(reply_token, text_message)

    if intent == 'ซักถามอาการ - custom - yes':
        req = request.get_json(silent=True, force=True)
        fulfillmentText = ''
        sum = 0
        query_result = req.get('queryResult')
        weight = int(query_result.get('parameters').get('weight'))
        hight = int(query_result.get('parameters').get('hight'))
        age = int(query_result.get('parameters').get('age'))
        
        bmi = weight/((hight/100)**2) 

        print("Your BMI is: {0} and you are: ".format(bmi), end='')

        #conditions
        if ( bmi < 16):
            fulfillmentText = 'คุณอายุ{0}คุณมี BMI={1} ฉันคิดว่าคุณผอมเกินไปควรทานอาหารที่ให้พลังงานมากขึ้นนะคะ'.format(age,bmi)
            print("severely underweight")

        elif ( bmi >= 16 and bmi < 18.5):
            fulfillmentText = 'คุณอายุ{0}คุณมี BMI={1} ฉันคิดว่าคุณมีน้ำหนักน้อยเกินไปควรทานให้มากขึ้นนะคะ'.format(age,bmi)
            print("underweight")

        elif ( bmi >= 18.5 and bmi < 25):
            fulfillmentText = 'คุณอายุ{0}คุณมี BMI={1} น่าอิจฉาจุงเบยหุ่นดีมากกกกก'.format(age,bmi)
            print("Healthy")

        elif ( bmi >= 25 and bmi < 30):
            fulfillmentText = 'คุณอายุ{0}คุณมี BMI={1} ควรลดของมันและของทอดนะคะ'.format(age,bmi)
            print("overweight")

        elif ( bmi >=30):
            fulfillmentText = 'คุณอายุ{0}คุณมี BMI={1} ไอ่ต้าวววว กินให้น้อยลงหน่อยน๊า'.format(age,bmi)
            print("severely overweight")



        text_message = TextSendMessage(text=fulfillmentText)
        line_bot_api.reply_message(reply_token,text_message)
        

    if intent == 'ควรกินน้ำ':
        text_message = TextSendMessage(text='ทดสอบสำเร็จ')
        line_bot_api.reply_message(reply_token,text_message)

        
if __name__ == "__main__":
    app.run()
