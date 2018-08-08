""" Trash Can Inventory Service
"""

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)

VERSION = "0.1"

@app.route('/')
def version():
    """Route IRI returns the API version """
    return jsonify(version=VERSION)

wcans = {}
@app.route('/waste/cans', methods=['GET','POST'])
def cans():
    """ /cans collection allows POST of new cans and GET of all cans """
    if request.method == "POST":
        can = request.get_json()
        result = validate_can(can)
        if result:
            print("ERROR: " + request.url + " : " + result)
            return jsonify(error=result), 400
        wcans[can["id"]] = can
        response = jsonify(can)
        response.status_code = 201
        response.headers['Location'] = "/waste/cans/" + str(can["id"])
        response.autocorrect_localtion_header = False
        return response
    elif request.method = 'GET':
        return jsonify(list(wcans.values()))
    else:
        return jsonify(error="bad HTTP verb, only GET and POST supported"), 400

@app.route('/waste/cans/<int:can_id>', methods=['GET','DELETE'])
def can(can_id):
    if can_id not in wcans:
        return jsonify(error="trash can id not found"), 404
    if request.method == 'GET':
        return jsonify(wcans[can_id])
    elif request.method == 'DELETE':
        del wcans[can_id]
        return ('', 204)
    else:
        return jsonify(error="bad HTTP verb, only GET and DELETE supported"), 400


def validate_can(can):
    """ Dbc checks for required can fields and settings
        returns False if can is valid
        returns a string describing the error otherwise
    """
    try:
        #Test id
        can["id"] = int(can["id"])
        if can["id"] < 0 or 999999999 < can["id"]:
            raise ValueError("can.id our of range [0..99999999]")
        #Test deployed
        if can["deployed"] == "True":
            can["deployed"] = True
        elif can["deployed"] == "False":
            can["deployed"] = False
        else:
            raise ValueError("can.deployed must be boolean (True, False)")
        #Test capacity
        can["capacity"] = float(can["capacity"])
        if can["capacity"] <= 0.0 or 9999 < can["capacity"]:
            raise ValueError("can.capacity out of range (0.0..9999.0)")
        #Test power
        if "power" not in can:
            raise ValueError("field power must be present")
    except Exception as ex:
        return str(ex)
    return "" #no errors
    
