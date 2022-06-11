from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from invokes import invoke_http
import pika
import json
import os

try:
    accountMSURL = os.environ['account_host'] or "http://localhost:5003"
    cartMSURL = os.environ['cart_host'] or 'http://192.168.193.175:5001'
    inventoryMSURL = os.environ['inventory_host'] or 'http://192.168.193.98:80'
    stripeMSURL = os.environ['stripe_host'] or 'http://127.0.0.1:5002'
    rabbitMQhostname = os.environ['rabbit_host'] or "localhost"
except:
    accountMSURL = "http://localhost:5003"
    cartMSURL = 'http://192.168.193.175:5001'
    inventoryMSURL = 'http://192.168.193.98:80'
    stripeMSURL = 'http://127.0.0.1:5002'
    rabbitMQhostname = "localhost"
app = Flask(__name__)
CORS(app)

# connector to rabbitMQ
# rabbitMQhostname = "activitylogms"
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


# Function 1 : Get Cart Details and Items in Cart


def getCartDetails(cid):
    # get cart details
    cart_URL = cartMSURL+"/cart/customerid/"+str(cid)
    result = invoke_http(cart_URL, method='GET')
    try:
        if result["data"] == "Customer does not have an open cart":
            return False
        else:
            cartDetails = result["data"]
            return cartDetails
    except Exception as e:
        print(e)
        # message = "An error occurred in getting cart details"
        channel.basic_publish(exchange=exchangename, routing_key="checkout.error",
                              body="Error geting cart Details Customer most likely does not have an open cart")
        return False  # Most Likely Customer does not have an open cart


# Function 2: Calculate the total price of the cart
def calculateAmount(cid):  # uses getCartDetails
    total = 0
    cartDetails = getCartDetails(cid)
    if cartDetails:
        cartItems = cartDetails["cartItems"]
        for item in cartItems:
            productid = item[0]
            qty = item[1]
            url = inventoryMSURL+"/api/products/"+str(productid)
            response = requests.get(url, verify=False)
            response = json.loads(response.text)
            price = response["price"]
            total += qty * price * 100  # Added *100.  1000 = $10 , 1234 = $12.34
        return total
    else:
        return False


# 1. Process Checkout Pipeline
@app.route("/checkout", methods=['POST'])
def processPayment():
    response = request.get_json()
    cid = response["cid"]
    # Step 1 Get Customer Stripe Details
    getUser_URL = accountMSURL + "/getuser/"+str(cid)
    customerData = invoke_http(getUser_URL, method='GET')
    customerStripeID = customerData['data']["stripedata"]["customerStripeID"]

    # Step 2 Calculate amount of items in cart
    amount = calculateAmount(cid)
    if amount == False:
        message = "Calculate amount error"
        channel.basic_publish(exchange=exchangename, routing_key="checkout.error",
                              body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "message": message,
                "code": 400
            }
        )

    # Step 3 Send payment instructions to Stripe
    payment_URL = stripeMSURL+"/chargecustomer"
    payment_data = {
        "amount": amount,
        "currency": "sgd",
        "customer": customerStripeID
    }
    result = invoke_http(payment_URL, method='POST', json=payment_data)

    if result["code"] == 200:
        # Step 4 Send updates to Inventory MS
        cartDetails = getCartDetails(cid)
        cartItems = cartDetails["cartItems"]
        minusInvent = True
        for item in cartItems:
            productid = item[0]
            qty = item[1]
            updateInventoryQtyURL = inventoryMSURL + \
                "/api/products/"+str(productid)+"/"+str(qty)
            result = requests.get(updateInventoryQtyURL)
        if result.status_code != 200:
            return jsonify(
                {
                    "message": "Checkout failed error with inventory",
                    "res": result,
                    "code": 400
                })
        # Step 5 Send updates to Cart MS that Cart has been checked out
        checkoutURL = cartMSURL+"/cart"
        result = invoke_http(checkoutURL, method='PUT',
                             json={"customerID": cid})
        if result["code"] == 201 or result["code"] == 200:
            return jsonify(
                {
                    "message": "Checkout successful",
                    "code": 200
                })
        else:
            message = "Checkout confirmation error, error with cartms"
            channel.basic_publish(exchange=exchangename, routing_key="checkout.info",
                                  body=message, properties=pika.BasicProperties(delivery_mode=2))
            return jsonify(
                {
                    "message": message,
                    "code": 400
                }
            )
    else:
        message = "Stripe error"
        channel.basic_publish(exchange=exchangename, routing_key="checkout.info",
                              body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "message": message,
                "code": 400
            }
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
