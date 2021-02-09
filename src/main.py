"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import Queue
from twilio.rest import Client
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

newQueue = Queue()
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/new', methods=['POST'])
def create_queue():
    name = request.json.get('name')
    phone = request.json.get('phone')
    item = {
        "name": name,
        "phone": phone
    }
    newQueue.enqueue(item)

    if not name:
        return jsonify({"msg": "name is required"}), 400
    if not phone:
        return jsonify({"msg": "phone is required"}), 400

    return jsonify({"Success": "user has been created"}), 201

@app.route('/next', methods=['GET'])
def next_queue():
    if newQueue != []:
        newQueue.dequeue()
        return jsonify({"msg": "the list goes to the next"}),200
    else:
        return jsonify({"msg": "Empty List"}),400
    
    

@app.route('/all', methods=['GET'])
def all_queue():
    all = newQueue.get_queue()
    return jsonify({"success": "ok"}, all), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
