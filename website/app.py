from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask import send_file, send_from_directory, safe_join, abort
import json
import datetime
import csv

from numpy.core.numeric import full
from CVRP import Cvrp
import numpy as np
import copy

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
                full_costs = calculate_scvrp(jsonData['returnObject'], calc_code)
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
                full_cost = calculate_scvrp(jsonData['returnObject'], calc_code)

            return {
                'code' : calc_code
            }

        #if(jsonData['requestType'] == 'goToSolution'):
            #return redirect(f'/result/{jsonData["code"]}')

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
    
def calculate_scvrp(data,  calc_code):
    print("start calculation")
    arr_points = data["points"]
    arr_x = []
    arr_y = []
    demand = {}
    arr_x.append(0)
    arr_y.append(0)
    demand[0] = 0
    vehicle_capacity = int(data["cap"])
    i = 1
    for _element in arr_points:
        arr_x.append(float(_element["x"]))
        arr_y.append(float(_element["y"]))
        demand[i] = float(_element["q"])
        i += 1
    arr_x = np.array(arr_x)
    arr_y = np.array(arr_y)
    #demand = np.array(demand)
    print(f"arr_x: {arr_x}")
    print(f"arr_y: {arr_y}")
    print(f"demand client: {demand}")
    
    demand_copy = copy.deepcopy(demand)
    arcs, costs = Cvrp.generate_arcs_and_costs(loc_x = arr_x, loc_y = arr_y)
    saving = Cvrp.generate_saving_matrix(arcs, costs)
    #n = len(arr_x)
    #N = [i for i in range(1, n+1)]
    #V = [0] + N
    #solution = solver(arcs, N, vehicle_capacity, demand, costs,V )
    routes, demands = Cvrp.generate_routes(saving, demand, vehicle_capacity)
    print(f"solution {routes}")
    print(f"demand car {demands}")
    print(f"clienc demand_copy {demand_copy}")
    Cvrp.plotting_solution(arr_x, arr_y, list(demand_copy.values()), vehicle_capacity, routes, index = calc_code)
    full_cost = Cvrp.routes_full_cost(routes, costs)
    #zapisz do csv
    #print(f"full cost {full_cost}")
    with open('./data/csv_files/'+calc_code+'.csv', 'w', newline = '') as csvfile:
        my_writer = csv.writer(csvfile, delimiter = ' ')
        my_writer.writerow('arcs')
        my_writer.writerow(arcs)
        my_writer.writerow('costs')
        my_writer.writerow(costs)
        my_writer.writerow('saving')
        my_writer.writerow(saving)
        my_writer.writerow('routes')
        my_writer.writerow(routes.values())

        database = get_database()
        database["results"][calc_code] = {
                    "name": calc_code,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "num_of_points": database["results"][calc_code]["num_of_points"],
                    "input_type": database["results"][calc_code]["input_type"],
                    "full_cost": full_cost,
                    "image_url": "../data/images/placeholder.png",
                    "csv_url:": ""
        }
        update_database(database)
    return full_cost