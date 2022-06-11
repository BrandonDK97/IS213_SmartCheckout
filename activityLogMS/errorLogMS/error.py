import json
import os
import amqp_setup
import requests


API_KEY = '5304110899:AAEBu9BUMvaQiyRervuUpqaMHlJHMnDvs3g' 
monitorBindingKey='*.error'

telegramSubscribers = ['670764767','69639099','300702075']
TELEGRAM_URL = "https://api.telegram.org/bot{}/sendMessage".format(API_KEY)

def notifyUserTele(msg):
    try:
        for userid in telegramSubscribers:
            payload = {
            "text": msg,
            "chat_id": userid
            }
            requests.post(TELEGRAM_URL, payload)
        print('Telegram notification sent')
    except Exception as e:
        print()
        print('Telegram notification failed:', e)

def receiveError():
    amqp_setup.check_setup()
    queue_name = "Error"
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() 

def callback(channel, method, properties, body): 
    print("\nReceived an error by " + __file__)
    processError(body)        
    print() 

def processError(errorMsg):
    print("Printing the error message:")
    try:
        error = json.loads(errorMsg)
        print("--JSON:", error)
        notifyUserTele(error)
    except Exception as e:
        print("--NOT JSON:", e)  
        print("--DATA:", errorMsg)
        notifyUserTele(errorMsg)
    print()

if __name__ == "__main__":   
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveError()
