from pymongo import MongoClient
from datetime import datetime
import requests

# client = MongoClient('mongodb://35.197.147.52:27017/') or MongoClient('mongodb://localhost:27017/')
client = MongoClient('mongodb://cart-mongodb:27017/') or MongoClient('mongodb://localhost:27017/')
# client = MongoClient('mongodb://localhost:27017/')


db = client.virtualCartMS

##checking status of run
stat=client.admin
# Issue the serverStatus command and print the results
serverStatusResult=stat.command("serverStatus")
print(serverStatusResult)


def createNewVirtualCart(customerID, storeID):
    # check if current got cart before making
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    currentCart = queryCustomerCurrentCart(customerID)
    if currentCart == None: # no current cart
        cart = {
            "cartID": getNextCartID(),
            "createdDatetime": dt_string,
            "customerID": customerID,
            "cartItems": [],
            "storeID": storeID,
            "cartStatus": "current"  # other cartStatus current/checkedout/deleted
        }
        result = db.cart.insert_one(cart)
        return cart
    else: #existing cart found
        # update storeID, for transaction. For example old cart at other store
        result = db.cart.update_one({'_id' : currentCart.get('_id') }, {'$set': {'storeID': storeID}})
        cart = db.cart.find_one({'_id' : currentCart.get('_id') })
        return cart

def addItemToCart(customerID,productID,qty):
    currentCart = queryCustomerCurrentCart(customerID)
    if currentCart == None: # no current cart
        return False

    cartItems = currentCart['cartItems']
    # check if product alrd in cart
    itemExist = False
    for i in range(0,len(cartItems)):
        if productID == cartItems[i][0]:
            cartItems[i][1] = qty
            itemExist = True

    if itemExist == False:
        cartItems.append([productID,qty])

    db.cart.update_one({'_id' : currentCart.get('_id') }, {'$set': {'cartItems': cartItems}})
    cart = db.cart.find_one({'_id' : currentCart.get('_id') })
    return cart

def deleteItemFromCart(customerID, productID):
    currentCart = queryCustomerCurrentCart(customerID)
    if currentCart == None: # no current cart
        return False

    cartItems = currentCart['cartItems']
    deleted = False
    for i in range(0,len(cartItems)):
        if productID == cartItems[i][0]:
            del cartItems[i]
            deleted = True
            break

    if deleted == False: # item not in cart
        return False

    db.cart.update_one({'_id' : currentCart.get('_id') }, {'$set': {'cartItems': cartItems}})
    cart = db.cart.find_one({'_id' : currentCart.get('_id') })
    return cart
        
def queryCart(cartID):
    cartID = int(cartID)
    res = db.cart.find_one({"cartID": cartID})
    return res

def queryCustomerCurrentCart(customerID):
    res = db.cart.find_one({"customerID": customerID , "cartStatus":"current"})
    return res #none if no cart found

def setCurrentCartToCheckout(customerID):
    try:
        currentCart = queryCustomerCurrentCart(customerID)
        db.cart.update_one({'_id' : currentCart.get('_id') }, {'$set': {"cartStatus": "checkOut"}})
        cart = db.cart.find_one({'_id' : currentCart.get('_id') })
        return cart
    except:
        return False # return error code in future

def setCurrentCartToDeleted(customerID):
    try:
        currentCart = queryCustomerCurrentCart(customerID)
        db.cart.update_one({'_id' : currentCart.get('_id') }, {'$set': {"cartStatus": "deleted"}})
        cart = db.cart.find_one({'_id' : currentCart.get('_id') })
        return cart
    except:
        return False # return error code in future

def getNextCartID():
    res = db.cart.find_one(sort=[("cartID", -1)])
    try:
        if res == None:
            return 0
        return res['cartID']+1
    except:
        return 0 # if no db is created


# print(queryCustomerCurrentCart("carleb123"))

# print(getNextCartID())

