import pyrebase
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)

# Connect to Firebase
def connect():
    config = {
        'apiKey': "AIzaSyBJxyh7PQlzL9D62iOyX1oLwQbsNwJZIpk",
        'authDomain': "is213-userdata.firebaseapp.com",
        'databaseURL': "https://is213-userdata-default-rtdb.asia-southeast1.firebasedatabase.app",
        'projectId': "is213-userdata",
        'storageBucket': "is213-userdata.appspot.com",
        'messagingSenderId': "787070048519",
        'appId': "1:787070048519:web:c98e878c3b17e93b8ecda2",
        'measurementId': "G-PHWRV43X8W",
    }

    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()

    return firebase.database()

db = connect()

@app.route("/getallusers", methods=['GET'])
def getAllUsers():
    try:
        data = db.child("users").get()
        data = data.val()
        num = len(data)
        num = str(num)
        if data == []:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "data": data
                    },
                    "message": 'No users in database'
                }
            ), 400
    except:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "data": data
                },
                "message": 'An error occured when trying to get users'
            }
        ), 400
    return jsonify(
        {
            "code": 200,
            "data": data,
            "message": 'Successfully obtained ' + num+' users'
        }
    ), 200


@app.route("/getuser/<string:userid>", methods=['GET'])
def getUserObj(userid):
    try:
        userObj = db.child("users").order_by_child(
            'userid').equal_to(userid).get()
        userObj = userObj.val()
        if userObj == []:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "userid": userid
                    },
                    "message": 'User does not exist'
                }
            ), 400
    except:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userid": userid
                },
                "message": 'User does not exist'
            }
        ), 400
    return jsonify(
        {
            "code": 200,
            "data": userObj[userid],
            "message": 'Successfully obtained user object'
        }
    ), 200

@app.route("/getuserbyemail/<string:email>", methods=['GET'])
def getUserByEmail(email):
    try:
        email = email.lower()
        userObj = db.child("users").order_by_child("email").equal_to(email).get()
        userObj = userObj.val()
        if userObj == []:
            return jsonify(
                {
                    "code": 400,
                    "data": {
                        "userid": email
                    },
                    "message": 'User does not exist'
                }
            ), 400
    except:
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userid": email
                },
                "message": 'User does not exist'
            }
        ), 400
    return jsonify(
        {
            "code": 200,
            "data": userObj,
            "message": 'Successfully obtained user object'
        }
    ), 200

@app.route("/createuser", methods=['POST'])
def create_user():
    data = request.get_json()
    userID = data["userid"]
    try:
        db.child("users").child(userID).set(data)
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred creating the account."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": data,
            "message": "Account successfully created."
        }
    ), 201


@app.route("/updatestripe", methods=['POST'])
def update_stripe():
    data = request.get_json()
    userID = data["userid"]
    stripeData = data['stripedata']
    try:
        db.child("users").child(userID).child(
            "stripedata").set(stripeData)
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred when updating Stripe data in database."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": data,
            "message": "Stripe data successfully updated in database."
        }
    ), 201


@app.route("/addstripe", methods=['POST'])
def add_stripe():
    data = request.get_json()
    userID = data["userid"]
    stripeData = data['stripedata']
    try:
        db.child("users").child(userID).child(
            "stripedata").set(stripeData)
    except:
        return jsonify(
            {
                "code": 500,
                "data": data,
                "message": "An error occurred when adding Stripe data to database."
            }
        ), 500
    return jsonify(
        {
            "code": 201,
            "data": stripeData,
            "message": "Stripe data successfully added to database."
        }
    ), 201


if __name__ == '__main__':
    CORS(app, resources={r"*": {"origins": "*"}})
    app.run(host='0.0.0.0', port=5003, debug=True)
