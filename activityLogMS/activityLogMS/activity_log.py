import json
import os
import sys
import amqp_setup

monitorBindingKey='#'

def receiveActivityLog():
    amqp_setup.check_setup()
        
    queue_name = 'Activity_Log'
    
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() 

def callback(channel, method, properties, body): 
    print("\nReceived an order log by " + __file__)
    processActivityLog(body)
    print() 

# def processOrderLog(order):
#     print("Recording an order log:")
#     print(order)

def processActivityLog(accountMsg):
    print("Printing the account:")
    try:
        account = json.loads(accountMsg)
        print("--JSON:", account)
    except Exception as e:
        print("--NOT JSON:", e)
        print("--DATA:", accountMsg)
    print()


if __name__ == "__main__":  
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveActivityLog()
