from flask import Flask, request, jsonify
import requests
import os
app = Flask(__name__)

try:
    gkeEndPoint = os.environ['gke_inventory']
    eksEndPoint = os.environ['eks_inventory']
except:
    gkeEndPoint = "http://35.197.147.52:80"
    eksEndPoint = "http://a51ccb76de4a34fe9a53edbcbc87e4da-664246035.ap-southeast-1.elb.amazonaws.com:80"
    
@app.route("/api/products", methods=['GET'])
def getProduct():
    gcpStatus=False
    eksStatus=False
    try:
        gcpRes = requests.get(gkeEndPoint+"/api/products" , timeout=4)
        gcpStatus = gcpRes.ok
    except:
        #gcp Error
        None
    try:
        eksRes = requests.get(eksEndPoint+"/api/products" , timeout=4)
        eksStatus = eksRes.ok
    except:
        #eks Error
        None
    
    if gcpStatus == True:
        return jsonify(gcpRes.json())
    elif eksStatus == True:
        return jsonify(eksRes.json())
    else:
        return jsonify(
            {
                "code": 500,
                "message": "Both GCP and EKS is offline."
            }
        ), 500

@app.route("/api/products/<int:id>", methods=['GET'])
def getSingleProduct(id):
    gcpStatus=False
    eksStatus=False
    try:
        gcpRes = requests.get(gkeEndPoint+"/api/products/"+str(id) , timeout=4)
        gcpStatus = gcpRes.ok
    except:
        #gcp Error
        None
    try:
        eksRes = requests.get(eksEndPoint+"/api/products/"+str(id) , timeout=4)
        eksStatus = eksRes.ok
    except:
        #eks Error
        None
    
    if gcpStatus == True:
        return jsonify(gcpRes.json())
    elif eksStatus == True:
        return jsonify(eksRes.json())
    else:
        return jsonify(
            {
                "code": 500,
                "message": "Both GCP and EKS is offline."
            }
        ), 500

@app.route("/api/products/add/<int:id>/<int:quantity>", methods=['GET'])
def addItemQty(id,quantity):
    gcpStatus=False
    eksStatus=False
    try:
        gcpRes = requests.get(gkeEndPoint+"/api/products/add/"+str(id)+"/"+str(quantity) , timeout=4)
        gcpStatus = gcpRes.ok
    except:
        #gcp Error
        None
    try:
        eksRes = requests.get(eksEndPoint+"/api/products/add/"+str(id)+"/"+str(quantity) , timeout=4)
        eksStatus = eksRes.ok
    except:
        #eks Error
        None
    
    if gcpStatus == True:
        return jsonify(gcpRes.json())
    elif eksStatus == True:
        return jsonify(eksRes.json())
    else:
        return jsonify(
            {
                "code": 500,
                "message": "Both GCP and EKS is offline."
            }
        ), 500

@app.route("/api/products/<int:id>/<int:quantity>", methods=['GET'])
def removeItemQty(id,quantity):
    gcpStatus=False
    eksStatus=False
    try:
        gcpRes = requests.get(gkeEndPoint+"/api/products/"+str(id)+"/"+str(quantity) , timeout=4)
        gcpStatus = gcpRes.ok
    except:
        #gcp Error
        None
    try:
        eksRes = requests.get(eksEndPoint+"/api/products/"+str(id)+"/"+str(quantity) , timeout=4)
        eksStatus = eksRes.ok
    except:
        #eks Error
        None
    
    if gcpStatus == True:
        return jsonify(gcpRes.json())
    elif eksStatus == True:
        return jsonify(eksRes.json())
    else:
        return jsonify(
            {
                "code": 500,
                "message": "Both GCP and EKS is offline."
            }
        ), 500


@app.route("/api/products", methods=['POST'])
def addProduct():
    data = request.get_json()
    gcpStatus=False
    eksStatus=False
    try:
        gcpRes = requests.post(gkeEndPoint+"/api/products", json = data , timeout=4)
        gcpStatus = gcpRes.ok
    except:
        #gcp Error
        None
    try:
        eksRes = requests.post(eksEndPoint+"/api/products", json = data , timeout=4)
        eksStatus = eksRes.ok
    except:
        #eks Error
        None
    
    if gcpStatus == True:
        return jsonify(gcpRes.json())
    elif eksStatus == True:
        return jsonify(eksRes.json())
    else:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "Both GCP and EKS is offline."
            }
        ), 500

@app.route("/api/products/<int:id>", methods=['DELETE'])
def deleteItem(id):
    gcpStatus=False
    eksStatus=False
    try:
        gcpRes = requests.delete(gkeEndPoint+"/api/products/"+str(id) , timeout=4)
        gcpStatus = gcpRes.ok
    except:
        #gcp Error
        None
    try:
        eksRes = requests.delete(eksEndPoint+"/api/products/"+str(id), timeout=4)
        eksStatus = eksRes.ok
    except:
        #eks Error
        None
    
    if gcpStatus == True:
        return jsonify(gcpRes.json())
    elif eksStatus == True:
        return jsonify(eksRes.json())
    else:
        return jsonify(
            {
                "code": 500,
                "message": "Both GCP and EKS is offline."
            }
        ), 500


@app.route("/ping", methods=['GET'])
def ping():
    gcpStatus=False
    eksStatus=False
    try:
        gcpRes = requests.get(gkeEndPoint+"/api/products/1", timeout=2)
        print(gcpRes)
        gcpStatus = gcpRes.ok
        print(gcpStatus)
    except:
        #gcp Error
        None
    try:
        eksRes = requests.get(eksEndPoint+"/api/products/1", timeout=4)
        eksStatus  = eksRes.ok
    except:
        #eks Error
        None
    return jsonify(
            {
                "serviceName": "inventoryLB",
                "GKEOnline": gcpStatus,
                "EKSOnline": eksStatus,
            }
        ), 201

if __name__ == '__main__':
    # app.run(port=80, debug=True)
    app.run(host='0.0.0.0', port=80, debug=True)