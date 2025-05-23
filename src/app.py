"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object

jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def Get_All_Family_Members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {"jackson": "Family",
                     "family": members}
    return jsonify(response_body), 200

#retrieve one family member by id
@app.route('/members/<int:member_id>', methods=['GET'])
def Get_Family_Member(member_id): 
    # This is how you can use the Family datastructure by calling its methods
    member = jackson_family.get_member(member_id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"msg": "Member not found"}), 404
    
#Add a new family member
@app.route('/members', methods=['POST'])
def Add_Family_Member():
    # This is how you can use the Family datastructure by calling its methods
    body = request.get_json()
    if not body:
        return jsonify({"msg": "No data provided"}), 400
    if 'first_name' not in body or 'age' not in body or 'lucky_numbers' not in body:
        return jsonify({"msg": "Missing required fields"}), 400
    member = jackson_family.add_member(body)
    return jsonify(member), 200

# Delete a family member by id
@app.route('/members/<int:member_id>', methods=['DELETE'])
def Delete_Family_Member(member_id):
    # This is how you can use the Family datastructure by calling its methods
    member = jackson_family.delete_member(member_id)
    if member:
        return jsonify({"msg": "Member deleted"}), 200
    else:
        return jsonify({"msg": "Member not found"}), 404


# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
