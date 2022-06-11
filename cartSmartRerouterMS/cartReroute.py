from flask import Flask, request, jsonify
import requests
import os
app = Flask(__name__)

try:
    gkeEndPoint = os.environ['gke_cart']
    eksEndPoint = os.environ['eks_cart']
except:
    gkeEndPoint = "http://34.142.128.121:5001/"
    eksEndPoint = "http://a184a2176842c4ce4a56b1ec57ca71f5-1032756115.ap-southeast-1.elb.amazonaws.com:5001"


@app.route("/create", methods=['POST'])
def createVCart():
    data = request.get_json()
    gcpStatus = False
    eksStatus = False

    try:
        gcpRes = requests.post(gkeEndPoint+"/create", json=data, timeout=4)
        gcpStatus = gcpRes.ok
    except:
        # gcp Error
        None
    try:
        eksRes = requests.post(eksEndPoint+"/create", json=data, timeout=4)
        eksStatus = eksRes.ok
    except:
        # eks Error
        None
    if gcpStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  gcpRes.json()["data"],
                "message": "Virtual cart successfully created"
            }
        )
    elif eksStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  eksRes.json()["data"],
                "message": "Virtual cart successfully created. WARNIGING: GCP offline, using EKS instead."
            }
        )
    else:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "Both GCP and EKS is offline."
            }
        ), 500


@app.route("/cart", methods=['POST'])
def addItem():
    data = request.get_json()
    gcpStatus = False
    eksStatus = False
    try:
        gcpRes = requests.post(gkeEndPoint+"/cart", json=data, timeout=4)
        gcpStatus = gcpRes.ok
    except:
        # gcp Error
        None
    try:
        eksRes = requests.post(eksEndPoint+"/cart", json=data, timeout=4)
        eksStatus = eksRes.ok
    except:
        # eks Error
        None

    if gcpStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  gcpRes.json()["data"],
                "message": "Item successfully added to cart"
            }
        )
    elif eksStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  eksRes.json()["data"],
                "message": "Item successfully added to cart. WARNIGING: GCP offline, using EKS instead."
            }
        )
    else:
        return jsonify(
            {
                "code": 203,
                "data": data,
                "message": "Virtual Cart does not exist for this user"
            }
        ), 203


@app.route("/cart/delete", methods=['POST'])
def deleteItem():
    data = request.get_json()
    gcpStatus = False
    eksStatus = False
    try:
        gcpRes = requests.post(
            gkeEndPoint+"/cart/delete", json=data, timeout=4)
        print(gcpRes.json())
        gcpStatus = gcpRes.ok
    except:
        # gcp Error
        None
    try:
        eksRes = requests.post(
            eksEndPoint+"/cart/delete", json=data, timeout=4)
        eksStatus = eksRes.ok
    except:
        # eks Error
        None

    if gcpStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  gcpRes.json()["data"],
                "message": "Cart successfully deleted"
            }
        )
    elif eksStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  eksRes.json()["data"],
                "message": "Cart successfully deleted. WARNIGING: GCP offline, using EKS instead."
            }
        )
    else:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "Both GCP and EKS is offline."
            }
        ), 500


@app.route("/cart", methods=['DELETE'])
def delCart():
    data = request.get_json()
    gcpStatus = False
    eksStatus = False
    try:
        gcpRes = requests.delete(gkeEndPoint+"/cart", json=data, timeout=4)
        gcpStatus = gcpRes.ok
    except:
        # gcp Error
        None
    try:
        eksRes = requests.delete(eksEndPoint+"/cart", json=data, timeout=4)
        eksStatus = eksRes.ok
    except:
        # eks Error
        None

    if gcpStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  gcpRes.json()["data"],
                "message": "Cart successfully deleted"
            }
        )
    elif eksStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  eksRes.json()["data"],
                "message": "Cart successfully deleted. WARNIGING: GCP offline, using EKS instead."
            }
        )
    else:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "Both GCP and EKS is offline."
            }
        ), 500


@app.route("/cart", methods=['PUT'])
def checkoutCart():
    data = request.get_json()
    gcpStatus = False
    eksStatus = False
    try:
        gcpRes = requests.put(gkeEndPoint+"/cart", json=data, timeout=4)
        gcpStatus = gcpRes.ok
    except:
        # gcp Error
        None
    try:
        eksRes = requests.put(eksEndPoint+"/cart", json=data, timeout=4)
        eksStatus = eksRes.ok
    except:
        # eks Error
        None

    if gcpStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  gcpRes.json()["data"],
                "message": "Cart successfully checked out"
            }
        )
    elif eksStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  eksRes.json()["data"],
                "message": "Cart successfully checked out. WARNIGING: GCP offline, using EKS instead."
            }
        )
    else:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "Both GCP and EKS is offline."
            }
        ), 500


@app.route("/cart/cartid/<string:cartID>", methods=['GET'])
def getCartFromCartID(cartID):
    gcpStatus = False
    eksStatus = False
    try:
        gcpRes = requests.get(gkeEndPoint+"/cart/cartid/"+cartID, timeout=4)
        gcpStatus = gcpRes.ok
    except:
        # gcp Error
        None
    try:
        eksRes = requests.get(eksEndPoint+"/cart/cartid/"+cartID, timeout=4)
        eksStatus = eksRes.ok
    except:
        # eks Error
        None

    if gcpStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  gcpRes.json()["data"],
                "message": "Cart successfully retrieved"
            }
        )
    elif eksStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  eksRes.json()["data"],
                "message": "Cart successfully retrieved. WARNIGING: GCP offline, using EKS instead."
            }
        )
    else:
        return jsonify(
            {
                "code": 500,
                "data": "cartID = " + cartID,
                "message": "Both GCP and EKS is offline."
            }
        ), 500


@app.route("/cart/customerid/<string:customerid>", methods=['GET'])
def getCartFromCustomerID(customerid):
    gcpStatus = False
    eksStatus = False
    try:
        gcpRes = requests.get(
            gkeEndPoint+"/cart/customerid/"+customerid, timeout=4)
        gcpStatus = gcpRes.ok
    except:
        # gcp Error
        None
    try:
        eksRes = requests.get(
            eksEndPoint+"/cart/customerid/"+customerid, timeout=4)
        eksStatus = eksRes.ok
    except:
        # eks Error
        None

    if gcpStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  gcpRes.json()["data"],
                "message": "Cart successfully retrieved"
            }
        )
    elif eksStatus == True:
        return jsonify(
            {
                "code": 201,
                "data":  eksRes.json()["data"],
                "message": "Cart successfully retrieved. WARNIGING: GCP offline, using EKS instead."
            }
        )
    else:
        return jsonify(
            {
                "code": 500,
                "data": "customerid = "+customerid,
                "message": "Both GCP and EKS is offline."
            }
        ), 500


@app.route("/ping", methods=['GET'])
def ping():
    gcpStatus = False
    eksStatus = False
    try:
        gcpRes = requests.get(gkeEndPoint+"/ping", timeout=2)
        gcpStatus = gcpRes.ok
    except:
        # gcp Error
        None
    try:
        eksRes = requests.get(eksEndPoint+"/ping", timeout=4)
        eksStatus = eksRes.ok
    except:
        # eks Error
        None
    return jsonify(
        {
            "serviceName": "cartLB",
            "GKEOnlie": gcpStatus,
            "EKSOnline": eksStatus,
        }
    ), 201


if __name__ == '__main__':
    # app.run(port=5001, debug=True)
    app.run(host='0.0.0.0', port=5001, debug=True)
