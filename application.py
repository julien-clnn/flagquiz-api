from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import random
import os

app = Flask(__name__)
CORS(app)

REGIONS = {
    "Europe": [
        "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina",
        "Bulgaria", "Croatia", "Cyprus", "Czech Republic", "Denmark", "Estonia",
        "Finland", "France", "Germany", "Greece", "Hungary", "Iceland", "Ireland",
        "Italy", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg", "Malta",
        "Moldova", "Monaco", "Montenegro", "Netherlands", "Norway", "Poland",
        "Portugal", "Romania", "Russia", "Serbia", "Slovakia", "Slovenia", "Spain",
        "Sweden", "Switzerland", "Ukraine", "United Kingdom"
    ],
    
    "Asia": [
        "Afghanistan", "Armenia", "Azerbaijan", "Bahrain", "Bangladesh", "Bhutan",
        "Brunei", "Cambodia", "China", "Georgia", "India", "Indonesia", "Iran", "Iraq",
        "Israel", "Japan", "Jordan", "Kazakhstan", "Kuwait", "Kyrgyzstan", "Laos",
        "Lebanon", "Malaysia", "Maldives", "Mongolia", "Myanmar", "Nepal", "North Korea",
        "Oman", "Pakistan", "Philippines", "Qatar", "Saudi Arabia", "Singapore",
        "South Korea", "Sri Lanka", "Syria", "Taiwan", "Tajikistan", "Thailand",
        "Turkey", "Turkmenistan", "United Arab Emirates", "Uzbekistan", "Vietnam",
        "Yemen"
    ],
    
    "Africa": [
        "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
        "Cameroon", "Cape Verde", "Central African Republic", "Chad", "Comoros",
        "Djibouti", "Egypt", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea",
        "Kenya", "Lesotho", "Liberia", "Libya", "Madagascar", "Malawi", "Mali",
        "Mauritania", "Mauritius", "Morocco", "Mozambique", "Namibia", "Niger",
        "Nigeria", "Rwanda", "Senegal", "Sierra Leone", "Somalia", "South Africa",
        "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda", "Zambia",
        "Zimbabwe"
    ],
    
    "North America": [
        "Bahamas", "Barbados", "Canada", "Costa Rica", "Cuba", "Dominican Republic",
        "El Salvador", "Grenada", "Guatemala", "Haiti", "Honduras", "Jamaica",
        "Mexico", "Nicaragua", "Panama", "United States"
    ],
    
    "South America": [
        "Argentina", "Bolivia", "Brazil", "Chile", "Colombia", "Ecuador", "Guyana",
        "Paraguay", "Peru", "Uruguay", "Venezuela"
    ],
    
    "Oceania": [
        "Australia", "Fiji", "New Zealand", "Papua New Guinea"
    ]
}

# Load flags data
try:
    with open('flags_metadata.json', 'r', encoding='utf-8') as f:
        FLAGS = json.load(f)
except FileNotFoundError:
    print("Flags metadata file not found")
    FLAGS = []

@app.route('/flag', methods=['GET'])
def get_random_flag():
    if not FLAGS:
        return jsonify({"error": "No flags available"}), 404

    flag = random.choice(FLAGS)
    return jsonify({
        "name": flag['name'],
        "flag_path": flag['flag_path'],  # Directement depuis le JSON
        "flag_code": flag['flag_code']   # Inclure le code du drapeau si nécessaire
    })

@app.route('/flag/<region>', methods=['GET'])
def get_random_region_flag(region):
    if region not in REGIONS:
        return jsonify({"error": "Invalid region"}), 400

    region_flags = [
        flag for flag in FLAGS 
        if flag['name'] in REGIONS[region]
    ]

    if not region_flags:
        return jsonify({"error": f"No flags available for {region}"}), 404

    flag = random.choice(region_flags)
    return jsonify({
        "name": flag['name'],
        "flag_path": flag['flag_path'],  # Directement depuis le JSON
        "flag_code": flag['flag_code']   # Inclure le code du drapeau si nécessaire
    })

@app.route('/regions', methods=['GET'])
def get_regions():
    return jsonify(list(REGIONS.keys()))

@app.route('/countries', methods=['GET'])
def get_countries():
    countries = [flag['name'] for flag in FLAGS]
    return jsonify(countries)

if __name__ == '__main__':
    app.run(debug=True)