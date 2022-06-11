import geopy.distance
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


class Store:
    def __init__(self, location, longitude, latitude):
        self.location = location
        self.longitude = longitude
        self.latitude = latitude

S1 = Store("SMU Store", 103.852119, 1.296568)
S2 = Store("Tampines Store", 103.956788, 1.349591)
store_list = [S1, S2]

app = Flask(__name__)

# request looks like
# {
#   longitude: 103.852119
#   latitude: 1.296568
# }

# http://127.0.0.1:5000/location


@app.route("/location", methods=['POST'])
def location():
    try:
        data = request.get_json()
        cust_longitude = float(data["longitude"])
        cust_latitude = float(data["latitude"])
        cust_coords = (cust_latitude, cust_longitude)
        for store in store_list:
            longitude = store.longitude
            latitude = store.latitude
            store_coords = (latitude, longitude)
            distance = geopy.distance.geodesic(cust_coords, store_coords).km
            if distance < 5:
                return jsonify(
                    {
                        "code": 201,
                        "location": store.location,
                        "lat" : latitude,
                        "long" : longitude,
                        "distance from store (KM)": str(round(distance,2))
                    }
                ), 201
        return jsonify(
            {
                "code": 201,
                "message": "Not in any store",
                "distance from store (KM)": "N.A"
            }
        ), 201
    except:
        return jsonify(
            {
                "code": 400,
                "message": "Bad Request, check body"
            }
        ), 400


if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=5006, debug=True)
