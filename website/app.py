from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask import send_file, send_from_directory, safe_join, abort
import json
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        # Get the data from the form
        jsonData = request.get_json()
        print(jsonData)

        if jsonData['requestType'] == 'sendPoints':
            calc_code = generate_random_string()
            database = get_database()
            if jsonData['type'] == 'manual':
                database["results"][calc_code] = {
                    "name": calc_code,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "num_of_points": jsonData["pointsLen"],
                    "input_type": 'Manual',
                    "full_cost": "0.00",
                    "image_url": "../data/images/placeholder.png",
                    "csv_url:": ""
                }
                update_database(database)
                calculate_scvrp(jsonData['manualObject'])
            else:
                database["results"][calc_code] = {
                    "name": calc_code,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "num_of_points": jsonData["pointsLen"],
                    "input_type": 'CSV',
                    "full_cost": "0.00",
                    "image_url": "../data/images/placeholder.png",
                    "csv_url:": ""
                }
                update_database(database)
                calculate_scvrp(jsonData['csvObject'])

            return {
                'code' : calc_code
            }

        if(jsonData['requestType'] == 'goToSolution'):
            return redirect(f'/result/{jsonData["code"]}')

    else:
        return render_template('index.html')

@app.route('/bibliography/')
def bibliography():
    return render_template('bibliography.html')

@app.route('/display/')
def display():
    return render_template('display.html', content=get_database())

@app.route('/result/<id>')
def result(id):
    return render_template('result.html', content=get_database()['results'][id])

@app.route('/data/images/<filename>')
def send_file(filename):
    return send_from_directory('./data/images/', filename)

@app.route('/data/csv_files/<filename>')
def get_csv_file(filename):
    return send_from_directory('./data/csv_files/', filename)

if __name__ == '__main__':
    app.run(debug=True)

def get_database():
    with open('./data/database/results_db.json', 'r') as file:
        database = json.load(file)
    return database

def update_database(data):
    with open('./data/database/results_db.json', 'w') as file:
        json.dump(data, file)

# create function that generates random string of length 7
def generate_random_string():
    import random
    import string
    return ''.join(random.choice(string.ascii_uppercase) for i in range(7))
    
def calculate_scvrp(data):
    # TO DO!!!
    pass