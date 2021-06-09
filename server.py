import json
from flask import Flask, jsonify, render_template
from flask_restful import Resource, abort, Api, reqparse
# https://flask-restful.readthedocs.io/en/latest/quickstart.html

app = Flask(__name__)
api = Api(app)

# from https://www.shelterlistings.org/county/wa-king-county.html
# name, address, phone number, general info, website url, county
# woman, man, child, lgbtq, charge?

SHELTER = {
    '1': {
        'name': 'Permanent Housing - Catholic Community Services', 'address': '100 23rd Ave. S, Seattle, WA 98144', 
        'phone': '(253) 863-8818', 
        'general-info': 'Sunrise Court provides permanent housing in Tacoma for chronically mentally ill adults. Sunrise Court consists of 20 units.', 
        'website': 'NA', 
        'county': 'King'},
    '2': {
        'name': 'Multi-service Center - Family Transitional', 
        'address': '1200 So 336th Street, Federal Way, WA 98003', 
        'phone': '253-838-6810', 
        'general-info': 'Class of Housing: housing for men and women in recovery', 
        'website': 'https://mschelps.org/gethelp/housing/', 
        'county': 'King'},
    '3': {
        'name': "Ywca - Angeline's Day Center For Homeless Women", 
        'address': '2024 Third Avenuet, Seattle, WA 98121, WA 98003', 
        'phone': '206-436-8650', 
        'general-info': 'Class of Housing: Day Center, Hygiene center for homeless women to access meals, laundry, showers, activities and connections to other services.', 
        'website': 'https://www.ywcaworks.org/programs/angelines-day-center', 
        'county': 'King'},
    '4': {
        'name': "Vine Maple Place Maple Valley", 
        'address': '21730 Dorre Don Way SE, Maple Valley, WA 98038', 
        'phone': '(425) 432-2119', 
        'general-info': 'Class of Housing: temporary emergency shelter for homeless single-parent families', 
        'website': 'https://www.vinemapleplace.org/', 
        'county': 'King'},
    '5': {
        'name': "Harrington Housing Transitional Housing Bellevue", 
        'address': '15980 NE 8th St, Bellevue, WA 98008', 
        'phone': '(425) 643-1434', 
        'general-info': 'Class of Housing: Transitional Housing', 
        'website': 'http://www.ccsww.org/', 
        'county': 'King'},
    "6": {
        "name": "Hopelink Redmond",
        "address": "8990 154th Avenue NE, Redmond, WA 98052",
        "phone": "(425)869-6000",
        "general-info": "Class of Housing: Transitional Housing, Emergency Family Shelter",
        "website": " https://www.hopelink.org/location/redmond-food-bank-and-emergency-services",
        "county": "King"
    }
}

@app.route('/')
def index():
    return render_template("index.html", SHELTER=SHELTER)
    # return jsonify(SHELTER)
    

def abort_if_shelter_doesnt_exist(shelter_id):
    if shelter_id not in SHELTER:
        abort(404, message="Shelter {} doesn't exist".format(shelter_id))

def parse_dict():
    parser.add_argument("name")
    parser.add_argument("address")
    parser.add_argument("phone")
    parser.add_argument("general-info")
    parser.add_argument("website")
    parser.add_argument("county")
    
    # Argument Parsing
# from flask_restful import reqparse
# parser = reqparse.RequestParser()
# parser.add_argument('rate', type=int, help='Rate to charge for this resource')
# args = parser.parse_args() // returns a python dict


parser = reqparse.RequestParser()

class SheltersList(Resource):
    def get(self):
        return SHELTER
    
    def post(self):
        parse_dict()
        args = parser.parse_args()
        shelter_id = int(max(SHELTER.keys())) + 1
        shelter_id = '%i' % shelter_id # how is this being calculated??? look it up later
        # creating new shelter with new shelter id
        SHELTER[shelter_id] = {
            "name": args["name"],
            "address": args["address"],
            "phone": args["phone"],
            "general-info": args["general-info"],
            "website": args["website"],
            "county": args["county"],
        }
        return SHELTER[shelter_id], 201

class Shelter(Resource):
    def get(self, shelter_id):
        # if shelter_id not in SHELTER:
        #     return "Not found", 404
        abort_if_shelter_doesnt_exist(shelter_id)
        return SHELTER[shelter_id]
        
    def put(self, shelter_id):
        parse_dict()
        args = parser.parse_args()
        abort_if_shelter_doesnt_exist(shelter_id)
        shelter = SHELTER[shelter_id]
        shelter["name"] = args["name"] if args["name"] is not None else shelter["name"]
        shelter["address"] = args["address"] if args["address"] is not None else shelter["address"]
        shelter["phone"] = args["phone"] if args["phone"] is not None else shelter["phone"]
        shelter["general-info"] = args["general-info"] if args["general-info"] is not None else shelter["general-info"]
        shelter["website"] = args["website"] if args["website"] is not None else shelter["website"]
        shelter["county"] = args["county"] if args["county"] is not None else shelter["county"]
        return shelter, 201
        
    def delete(self, shelter_id):
        abort_if_shelter_doesnt_exist(shelter_id)
        del SHELTER[shelter_id]
        return '', 204

api.add_resource(SheltersList, '/shelters')
api.add_resource(Shelter, '/shelters/<shelter_id>')


if __name__ == "__main__":
    app.run(debug=True)