import pyrebase
from flask import Flask, jsonify, request
from flask_cors import CORS
from invokes import invoke_http
import pika
import os

# connector to rabbitMQ
# rabbitMQhostname = "localhost"
rabbitMQhostname = os.environ['rabbit_host'] or "localhost"
port = 5672
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=rabbitMQhostname, port=port,
        heartbeat=3600, blocked_connection_timeout=3600,
    )
)
channel = connection.channel()
exchangename = "order_topic"
exchangetype = "topic"
####

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

stripeMSURL = os.environ['stripe_host'] or "http://localhost:5002"
accountMSURL = os.environ['account_host'] or "http://localhost:5003"
# stripeMSURL = "http://localhost:5002"
# accountMSURL = "http://accountms:5003"
# accountMSURL = "http://localhost:5003"

# 1. Check if user exists in firebase
def exists(id, phone, email):
    getallURL = accountMSURL + "/getallusers"
    result = invoke_http(getallURL, method='GET')
    users = result['data']
    error = []
    if users == {}:
        return error
    if id in users:
        error.append('user')
    for key in users:
        try:
            if users[key]['email'] == email:
                error.append('email')
            if users[key]['phone'] == phone:
                error.append('phone')
        except:
            pass
    return error


# 2.Add new user to database
# Format: {
#     "userid":"caleb123",
#     "name":"Caleb",
#     "password":"1234",
#     "phone":"41998952",
#     "email":"001245@hotmail.com"
#     }
@app.route("/createaccount", methods=['POST'])
def create_account():
    data = request.get_json()
    data['userid'] = data['userid'].lower()
    data['email'] = data['email'].lower()
    userID = data["userid"]
    phone = data["phone"]
    email = data['email']
    name = data['name']
    exists(userID, phone, email)
    errors = exists(userID, phone, email)
    message = ''
    if len(errors) > 0:
        for err in errors:
            message += err + ', '
        message += "already exists"
        amqpMessage = 'Account creation attempt with Name:' + name + ' Email:'+email+ ' Phone:'+phone+' tried to create account but ' + message
        channel.basic_publish(exchange=exchangename, routing_key="account.error",
                            body=amqpMessage, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userid": userID,
                    "phone": phone
                },
                "message": message
            }
        ), 400
    createuserURL = accountMSURL + "/createuser"
    result = invoke_http(createuserURL, method='POST', json=data)
    code = result["code"]
    message = result["message"]
    if code not in range(200, 300):
        channel.basic_publish(exchange=exchangename, routing_key="account.error",
                            body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify({
            "code": 500,
            "data": {"create_account_result": result},
            "message": message
        }), 500
    else:
        message = "Account created successfully"
        channel.basic_publish(exchange=exchangename, routing_key="account.info",
                            body=message)
        return jsonify(
            {
                "code": 201,
                "data": data,
                "message": "Account successfully created."
            }
        ), 201

# 3.Verify user login
# UserID login format:
#    {
#     "userid":"laleb123",
#     "password":"1234",
#     "phone":""
#    }
#          OR
# Phone login formet:
#    {
#     "userid":"",
#     "password":"1234",
#     "phone":"97452903"
#    }

@app.route("/verifylogin", methods=['POST'])
def verifyLogin():
    #get login post request
    data = request.get_json()
    email = data['email'].lower()
    # phone = data['phone']
    password = data['password']
    if email == "":
        return jsonify(
            {
                "code": 400,
                "data": None,
                "message": "Please key in login details"
            }
        ), 400
    try: #query datebase with email as key
        getallURL = accountMSURL + "/getuserbyemail/" + email
        result = invoke_http(getallURL, method='GET')
        code = result['code']
        if code == 400:
            return jsonify(
            {
                "code": 400,
                "data": result,
                "message": "Incorrect login details or password."
            }
        ), 400
        keys = list(result['data'].keys())
        user = result['data'][keys[0]]
        if user['email'] == email and user['password'] == password:
            return jsonify(
                    {
                        "code": 201,
                        "data": user,
                        "message": "Login successful"
                    }
                ), 201
        else:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                            "phone": user['phone'],
                            "userid": user['email']
                        },
                    "message": "Incorrect login details or password."
                }
            ), 400
    except:
        return jsonify(
            {
                "code": 400,
                "data": result,
                "message": "Incorrect login details or password."
            }
        ), 400


# 4.Add payment details
# Format:
# {"userid":"brandon123456","card":{"number":"4000056655665556","exp_month":3,"exp_year":2023,"cvc":"314"}}
@app.route("/addpaymentdetails", methods=['POST'])
def addPaymentDetails():
    # Get data
    data = request.get_json()
    userID = data['userid']
    # Check if user is already a stripe customer
    getUser_URL = accountMSURL + "/getuser/"+userID
    userdata = invoke_http(getUser_URL, method='GET')
    userObj = userdata['data']
    try:
        # If already a stripe customer, invoke stripe microservice /updatecustomer
        if userObj['stripedata']:
            stripeUpdateCustomerURL = stripeMSURL + "/updatecustomer"
            # Creating object with new card details and customer's current stripe data to update stripe
            stripeUpdateData = {}
            stripeUpdateData['card'] = data['card']
            stripeUpdateData['stripedata'] = userObj['stripedata']
            stripeCustomerResult = invoke_http(
                stripeUpdateCustomerURL, method='POST', json=stripeUpdateData)
            code = stripeCustomerResult["code"]
            stripeData = stripeCustomerResult["data"]
            message = stripeCustomerResult["message"]
            stripeAmqpMessage = userID +': '+ message
            if code not in range(200, 300):
                channel.basic_publish(exchange=exchangename, routing_key="stripe.error",
                                    body=stripeAmqpMessage, properties=pika.BasicProperties(delivery_mode=2))
                return jsonify({
                    "code": 500,
                    "data": {"stripe_result": stripeCustomerResult},
                    "message": message
                }), 500
            else:
                channel.basic_publish(exchange=exchangename, routing_key="stripe.info",
                                    body=message, properties=pika.BasicProperties(delivery_mode=2))
            # Update stripe TokenID, customerID and cardID details to Firebase tied to userID
            updatedStripeData = {}
            updatedStripeData['userid'] = userID
            updatedStripeData['stripedata'] = stripeData
            accountUpdateStripeURL = accountMSURL + "/updatestripe"
            updateCustomerResult = invoke_http(
                accountUpdateStripeURL, method='POST', json=updatedStripeData)
            code = updateCustomerResult["code"]
            customerData = updateCustomerResult["data"]
            message = updateCustomerResult["message"]
            if code not in range(200, 300):
                message = "An error occurred when updating Stripe details on database."
                channel.basic_publish(exchange=exchangename, routing_key="account.error",
                                    body=message, properties=pika.BasicProperties(delivery_mode=2))
                return jsonify(
                    {
                        "code": 500,
                        "data": {
                            "userid": userID,
                            "cardDetails": data
                        },
                        "message": "An error occurred when updating Stripe details on database."
                    }
                ), 500
            else:
                message = 'User stripe details successfully updated in database'
                channel.basic_publish(exchange=exchangename, routing_key="account.info",
                                    body=message, properties=pika.BasicProperties(delivery_mode=2))
                return jsonify(
                    {
                        "code": 201,
                        "data": updatedStripeData,
                        "message": "User stripe details successfully updated in firebase"
                    }
                ), 201
    except:
        pass
    # If not a stripe customer, invoke stripe microservice /createcustomer
    stripeCreateCustomerURL = stripeMSURL + "/createcustomer"
    # Post UserID and new card details to stripe
    stripeCustomerResult = invoke_http(
        stripeCreateCustomerURL, method='POST', json=data)
    code = stripeCustomerResult["code"]
    stripeData = stripeCustomerResult["data"]
    message = stripeCustomerResult["message"]
    if code not in range(200, 300):
        stripeAmqpMessage = userID +': '+ message
        channel.basic_publish(exchange=exchangename, routing_key="stripe.error",
                            body=stripeAmqpMessage, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify({
            "code": 500,
            "data": {"stripe_result": stripeCustomerResult},
            "message": message
        }), 500
    else:
        channel.basic_publish(exchange=exchangename, routing_key="stripe.info",
                            body=message, properties=pika.BasicProperties(delivery_mode=2))

    # Add stripe TokenID, customerID and cardID details to Firebase tied to userID
    accountAddStripeURL = accountMSURL + "/addstripe"
    newStripeData = {}
    newStripeData['userid'] = userID
    newStripeData['stripedata'] = stripeData
    updateCustomerResult = invoke_http(
        accountAddStripeURL, method='POST', json=newStripeData)
    code = updateCustomerResult["code"]
    customerData = updateCustomerResult["data"]
    message = updateCustomerResult["message"]
    if code not in range(200, 300):
        message = "An error occurred when updating Stripe details on database."
        channel.basic_publish(exchange=exchangename, routing_key="account.error",
                            body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userid": userID,
                    "cardDetails": data
                },
                "message": "An error occurred when adding Stripe details on database."
            }
        ), 500
    else:
        message = 'User stripe details successfully added to database'
        channel.basic_publish(exchange=exchangename, routing_key="account.info",
                            body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "code": 201,
                "data": newStripeData,
                "message": "User stripe details successfully added to firebase"
            }
        ), 201


if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=5000, debug=True)
