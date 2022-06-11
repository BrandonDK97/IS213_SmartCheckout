import stripe
import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from os import environ
app = Flask(__name__)
CORS(app)


stripe.api_key = environ.get("stripe_api_key") or "sk_test_51Kc9J2LLSNdGsMUOS8DYewqsFwrVDIlnJpUbLh1Kh2Kyt0oXhdCqeTBfOjAZFH1QyVpnSZseutTCPsJ49Q6BY81M00JdlN4TBb"

@app.route("/updatecustomer", methods=['POST'])
def updateCustomer():
  try:
    paymentDetails = request.get_json()
    cardDetails = paymentDetails['card']
    customerStripeID = paymentDetails['stripedata']['customerStripeID']
    cardID = paymentDetails['stripedata']['cardID']
    #Delete existing card
    stripe.Customer.delete_source(
      customerStripeID,
      cardID,
    )
    #Create new card tied to customer
    tokenObj = stripe.Token.create(
      card=cardDetails
      )
    cardObj = stripe.Customer.create_source(
    customerStripeID,
    source=tokenObj,
    )
    cardID = cardObj['id']
    tokenID = tokenObj['id']
    return jsonify(
        {
            "code": 201,
            "data": {
              "customerStripeID": customerStripeID,
              "cardID": cardID,
              "tokenID": tokenID
            },
            "message": "Card successfully updated."
            
        }
    ), 201
  except:
    return jsonify(
            {
                "code": 401,
                "data": paymentDetails,
                "message": "An error occurred creating the customer on Stripe."
            }
        ), 401

@app.route("/createcustomer", methods=['POST'])
def createCustomer():
  try:
    paymentDetails = request.get_json()
    cardDetails = paymentDetails['card']
    userID = paymentDetails['userid']
    customerObj = stripe.Customer.create(
      name=userID,
      description=userID
    )
    customerStripeID = customerObj['id']
    
    tokenObj = stripe.Token.create(
      card=cardDetails
      )

    cardObj = stripe.Customer.create_source(
    customerStripeID,
    source=tokenObj,
    )
    cardID = cardObj['id']
    tokenID = tokenObj['id']
    return jsonify(
        {
            "code": 201,
            "data": {
              "customerStripeID": customerStripeID,
              "cardID": cardID,
              "tokenID": tokenID
            },
            "message": "Customer successfully created."
            
        }
    ), 201
  except Exception as e:
    return jsonify(
            {
                "code": 402,
                "data": paymentDetails,
                "message": "An error occurred creating the customer on Stripe.",
                "error" : str(e)
            }
        ), 402

# amount
# {
#   "amount": 19.60,
#   "currency": SGD,
#   "customerStripeID": "cus_LJQj8BCDIsWNGp"
# }

@app.route("/chargecustomer", methods=['POST'])
def chargeCustomer():
  data = request.get_json()
  try:
    charge = stripe.Charge.create(
            amount = data["amount"],
            currency = data["currency"],
            customer = data["customer"]
    )
    return jsonify(
            {
                "code": 200,
                "message": "Payment successful"
            }
        )

  except Exception as e:
    return jsonify(
            {
                "code": 403,
                "message": str(e) # change to "Error processing payment"
            }
        ),403

@app.route("/listallpayments", methods=['GET'])
def getAllPayments():
  newList = []
  try:
    payments = stripe.Charge.list()
    payments = payments['data']
    for list in payments:
      amount = list['amount']
      amount = amount/10
      customerStripeID = list['customer']
      date = list['created']
      try:
        customerObj = stripe.Customer.retrieve(customerStripeID)
        name = customerObj['name']
      except:
        name = 'No Customer tied to this charge'
      paymentType = list['payment_method_details']['card']['brand']
      last4=list['payment_method_details']['card']['last4']
      tmp = {
                  'amount':amount,
                  'customerStripeID':customerStripeID,
                  'paymentType':paymentType,
                  'last4':last4,
                  'name':name,
                  'date':date
                }
      newList.append(tmp)
    count = len(newList)
    return jsonify(
            {
                "code": 200,
                "data": newList,
                "message": str(count)+ ' number of charges successfully retrieved'
            }
        )

  except Exception as e:
    return jsonify(
            {
                "code": 403,
                "message": 'Error getting charges from Stripe database' # change to "Error processing payment"
            }
        ),403

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          ": stripe payment service ...")
    app.run(host='0.0.0.0', port=5002, debug=True)

    