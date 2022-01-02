from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
import json
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get the data from the form
        data = request.form
        calc_code = generate_random_string()
        
        # add placeholder in database
        database = get_database()
        database["results"][calc_code] = {
            "name": calc_code,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "num_of_points": data["num_of_points"],
            "input_type": data["input_type"],
            "image_url": "../website/data/images/placeholder.png",
            "csv_url:": ""
        }

        save_database(database)

        calculate_scvrp(data)

        return redirect(url_for('results', calc_code=calc_code))

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