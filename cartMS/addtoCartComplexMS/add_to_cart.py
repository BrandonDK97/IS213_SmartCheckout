from flask import Flask, jsonify, request
from flask_cors import CORS
from invokes import invoke_http
import pika
import requests
import os
import json

try:
    inventoryMSURL = os.environ['inventory_host'] or "http://localhost:80"
    cartMSURL = os.environ['cart_host'] or "http://localhost:5001"
    rabbitMQhostname = os.environ['rabbit_host'] or "localhost"

except:  # if running in development
    inventoryMSURL = "http://localhost:80"
    cartMSURL = "http://localhost:5001"
    rabbitMQhostname = "localhost"

# connector to rabbitMQ
# rabbitMQhostname = "localhost"
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


####
'''
json = {
    "productID": "",
    "quantity": "",
    "customerID": "",
    "storeID": ""
}

'''
# 1.
# Create Virtual Cart
# [POST] /create


@app.route("/create", methods=['POST'])
def createVCart():
    data = request.get_json()
    customerID = data['customerID']
    storeID = data['storeID']
    createVCartURL = cartMSURL + "/create"
    result = invoke_http(createVCartURL, method='POST', json=data)
    code = result['code']
    message = result['message']
    if code not in range(200, 300):
        # post to rabbitMQ
        channel.basic_publish(exchange=exchangename, routing_key="order.error",
                              body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "code": 500,
                "data": {"create_vcart_result": result},
                "message": message
            }), 500
    else:
        message = "Virtual cart successfully created"
        # post to rabbitMQ
        channel.basic_publish(exchange=exchangename, routing_key="order.success",
                              body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "code": 201,
                "data": {"create_vcart_result": result},
                "message": message
            }), 201

# 2.
# Check if cart exists
# [GET] /cart/customerid?cid={customerID}


@app.route("/check", methods=['POST'])
def checkVCart():
    data = request.get_json()
    customerID = data['customerID']
    checkVCartURL = cartMSURL + "/cart/customerid/" + customerID
    result = invoke_http(checkVCartURL, method='GET')
    code = result['code']
    message = result['message']
    if code not in range(200, 300):
        # post to rabbitMQ
        channel.basic_publish(exchange=exchangename, routing_key="order.error",
                              body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "code": 500,
                "data": {"check_vcart_result": result},
                "message": message
            }), 500
    else:
        message = "Virtual cart exists"
        # post to rabbitMQ
        channel.basic_publish(exchange=exchangename, routing_key="order.success",
                              body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "code": 201,
                "data": {"check_vcart_result": result},
                "message": message
            }), 201

# 3.
# Add to cart when item in not in cart
# (Checks for quantity in inventory and adds to cart afterwards)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    print("START")
    data = request.get_json()
    quantityRequested = data['quantity']
    # Check cart exists
    checkVCartURL = cartMSURL + "/cart/customerid/" + data['customerID']
    result = invoke_http(checkVCartURL, method='POST')
    code = result['code']
    message = result['message']
    if code not in range(200, 300):
        # create new cart
        createVCartURL = cartMSURL + "/create"
        createVCartData = {
            "customerID": data['customerID'],
            "storeID": data['storeID']
        }
        result = invoke_http(createVCartURL, method='POST',
                             json=createVCartData)
        code = result['code']
        message = result['message']
        if code not in range(200, 300):
            # post to rabbitMQ
            channel.basic_publish(exchange=exchangename, routing_key="order.error",
                                  body=message, properties=pika.BasicProperties(delivery_mode=2))
            return jsonify(
                {
                    "code": 500,
                    "data": {"create_vcart_result": result},
                    "message": message
                }), 500
        else:
            message = "Virtual cart successfully created"
            # post to rabbitMQ
            channel.basic_publish(exchange=exchangename, routing_key="order.success",
                                  body=message, properties=pika.BasicProperties(delivery_mode=2))

    # Send to InventoryMS
    getProductByIdURL = inventoryMSURL + \
        "/api/products/" + str(data['productID'])
    print("Product url is " + getProductByIdURL)
    result = requests.get(getProductByIdURL)
    print("NEW")
    product = result.json()
    print(product)
    quantityInStock = product['quantity']

    if quantityRequested > quantityInStock:
        # Product exist, check stock
        # Post to RabbitMQ
        channel.basic_publish(exchange=exchangename,
                              routing_key='order.error', body=message, properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        return jsonify({
            "code": 500,
            "data": {
                "quantityRequested": quantityRequested,
                "quantityInStock": quantityInStock
            },
            "message": "Not enough quantity in stock"
        }), 50
    else:
        # Quantity Check passed
        # Send to CartMS
        addToCartURL = cartMSURL + "/cart"
        cartData = {
            "productID": data['productID'],
            "customerID": data['customerID'],
            "qty": quantityRequested
        }
        result = invoke_http(
            addToCartURL, method='POST', json=cartData)
        code = result['code']
        message = result['message']
        if code not in range(200, 300):
            # Post to RabbitMQ
            channel.basic_publish(exchange=exchangename,
                                  routing_key='order.error', body=message, properties=pika.BasicProperties(
                                      delivery_mode=2,  # make message persistent
                                  ))
            return jsonify({
                "code": 500,
                "data": {
                    "add_to_cart_result": result,
                },
                "message": message
            }), 500
        else:
            message = "Successfully added to cart"
            # Post to RabbitMQ
            channel.basic_publish(exchange=exchangename,
                                  routing_key='order.success', body=message, properties=pika.BasicProperties(
                                      delivery_mode=2,  # make message persistent
                                  ))
            return jsonify({
                "code": 201,
                "data": cartData,
                "message": "Product successfully added to cart"
            }), 201


@app.route("/test", methods=['GET'])
def test():
    message = "test"
    channel.basic_publish(exchange=exchangename, routing_key="order.error",
                          body=message, properties=pika.BasicProperties(delivery_mode=2))
    # res = channel.basic_publish(exchange=exchangename, routing_key="checkout.error",
    #                           body=message, properties=pika.BasicProperties(delivery_mode=2))
    # print(res)
    return "res"


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    customerID = data['customerID']
    productID = data['productID']
    obj = {
        "customerID": customerID,
        "productID": productID
    }
    removeFromCartURL = cartMSURL + "/cart/delete"
    result = invoke_http(removeFromCartURL, method='POST', json=obj)
    code = result['code']
    message = result['message']
    if code not in range(200, 300):
        # Post to RabbitMQ
        channel.basic_publish(exchange=exchangename,
                              routing_key='order.error', body=message, properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        return jsonify({
            "code": 500,
            "data": {
                "remove_from_cart_result": result,
            },
            "message": message
        }), 500
    else:
        message = "Successfully removed from cart"
        # Post to RabbitMQ
        channel.basic_publish(exchange=exchangename,
                              routing_key='order.success', body=message, properties=pika.BasicProperties(
                                  delivery_mode=2,  # make message persistent
                              ))
        return jsonify({
            "code": 201,
            "data": result['data'],
            "message": message
        }), 201


if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=5030, debug=True)
