from flask import Flask, request, jsonify
from cartMongoDB import createNewVirtualCart, addItemToCart, setCurrentCartToDeleted,setCurrentCartToCheckout, queryCart, queryCustomerCurrentCart, deleteItemFromCart
app = Flask(__name__)

# Create Virtual Cart
# [POST] /create
# POSTbody = {
#         "customerID": "string"
#         "storeID" : "string"
# }

@app.route("/create", methods=['POST'])
def createVCart():
    try:
        data = request.get_json()
        customerID = data['customerID']
        storeID = data['storeID']
        cartData = createNewVirtualCart(customerID, storeID)
        cartData.pop('_id', None)
        return jsonify(
            {
                "code": 201,
                "data": cartData,
                "message": "Virtual cart successfully created"
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred when creating virtual cart."
            }
        ), 500

# Add/Edit specific product
# [POST] /cart
# POSTbody = {
#         "customerID": "string"
#         "productID" : "string"
#         "qty" : int #qty will overide old qty,
# }


@app.route("/cart", methods=['POST'])
def addItem():
    try:
        data = request.get_json()
        customerID = data['customerID']
        productID = data['productID']
        qty = data['qty']
        cartData = addItemToCart(customerID, productID, qty)
        cartData.pop('_id', None)
        return jsonify(
            {
                "code": 201,
                "data": cartData,
                "message": "Item successfully added to cart"
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred when adding item to cart"
            }
        ), 500

@app.route("/cart/delete", methods=['POST'])
def deleteItem():
    try:
        data = request.get_json()
        customerID = data['customerID']
        productID = data['productID']
        cartData = deleteItemFromCart(customerID, productID)
        print(cartData)
        cartData.pop('_id', None)
        return jsonify(
            {
                "code": 201,
                "data": cartData,
                "message": "Item successfully deleted from cart"
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred when deleting item from cart"
            }
        ), 500

# Set cart to Delete
# [DELETE] /cart
# DELETEbody = {
#         "customerID": "string"
# }

@app.route("/cart", methods=['DELETE'])
def delCart():
    try:
        data = request.get_json()
        customerID = data['customerID']
        cartData = setCurrentCartToDeleted(customerID)
        cartData.pop('_id', None)
        return jsonify(
            {
                "code": 201,
                "data": cartData,
                "message": "Cart successfully deleted"
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred when deleting cart"
            }
        ), 500

# Set cart to checkedout
# [PUT] /cart
# PUTBody = {
#         "customerID": "string"
# }

@app.route("/cart", methods=['PUT'])
def checkoutCart():
    try:
        data = request.get_json()
        customerID = data['customerID']
        cartData = setCurrentCartToCheckout(customerID)
        cartData.pop('_id', None)
        return jsonify(
            {
                "code": 201,
                "data": cartData,
                "message": "Cart successfully checked out"
            }
        )
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred when checking out cart"
            }
        ), 500

# Get cart details using cartid
# [GET] /cart/cartid/{cartID}
# 192.168.193.175:5001/cart/cartid/123

@app.route("/cart/cartid/<string:cartID>", methods=['GET'])
def getCartFromCartID(cartID):
    try:
        cartData = queryCart(cartID)
        cartData.pop('_id', None)
        return jsonify(
            {
                "code": 201,
                "data": cartData,
                "message": "Cart successfully retrieved"
            }
        )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "cartId": cartID,
                "message": "An error occurred when looking for cart using cartID.",
                "error": str(e)
            }
        ), 500

# Get cart details using customerid
# [GET] /cart/customerid?cid={customerID}

#/cart/customerid/{customerID}

@app.route("/cart/customerid/<string:customerid>", methods=['GET'])
def getCartFromCustomerID(customerid):
    try:
        cartData = queryCustomerCurrentCart(customerid)
        cartData.pop('_id', None)
        if cartData == None:
            return jsonify(
                {
                    "code": 201,
                    "data": "Customer does not have an open cart",
                    "message": "Cart successfully retrieved"
                }
            )
        else:
            return jsonify(
                {
                    "code": 201,
                    "data": cartData,
                    "message": "Cart successfully retrieved"
                }
            )
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "cartId": customerid,
                "message": "An error occurred when looking for cart using customerID.",
                "error": str(e)
            }
        ), 500


@app.route("/ping", methods=['GET'])
def ping():
    return "Working"


if __name__ == '__main__':
    # app.run(port=5001, debug=True)
    print("Running Version 1.0")
    app.run(host='0.0.0.0', port=5001, debug=True)
