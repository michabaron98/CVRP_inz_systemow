from os import write
from matplotlib.collections import _CollectionWithSizes
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import csv 

class Cvrp():
    
    def plotting_points(loc_x = [0], loc_y = [0], demand = [10], vehicle_capacity = 20):
        """
        Method returns graph of points in a coordinate network and save it as png file
        ---------
        Parameters:
        loc_x - list - List of x coordinates of points
        loc_y - list - List of y coordinates of points
        demand - list - List of demand of every client
        vehicle_capacity - number of item which can take a vehilce.
        """
        if max(demand) > vehicle_capacity:
            vehicle_capacity = max(demand)
        _n = len(loc_x) - 1
        _N = [i for i in range(1, _n+1)] #indeksy klinetow
        #_V = [0] + _N # indeksy pojazdow    
        plt.scatter(loc_x[1:], loc_y[1:], c='b')
        for i in _N:
            plt.annotate('$q_%d=%d$' % (i, demand[i]), (loc_x[i]+2, loc_y[i]))
        plt.plot(loc_x[0], loc_y[0], c='r', marker='s')
        plt.axis('equal')
        #plt.savefig('points.png')

    def generate_arcs_and_costs(loc_x = [0], loc_y = [0]):
        """
        Function returns a list of arcs  and list of costs
        ---------
        Parameters:
        loc_x - list - List of x coordinates of points
        loc_y - list - List of y coordinates of points
        """
        _n = len(loc_x) - 1
        _N = [i for i in range(1, _n+1)] #indeksy klinetow
        _V = [0] + _N # indeksy pojazdow   
        _arcs = [(i, j) for i in _V for j in _V if i != j] #zestawienie łuków
        _costs = {(i, j): np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j]) for i, j in _arcs}#koszt przejazdu
        return _arcs, _costs

    def generate_saving_matrix(arcs, costs):
        """
        Function returns sorted matrix of savings - dict
        ---------
        Parameters:
        arcs - list - All arcs in graph. Example: [(0,1), (1,0)]
        costs - dict - Key - arc, Value - cost of trip. Example {(0,1): 123, (1,0):123}

        """
        _saving = {}
        for i, j in arcs:
            _c_1_i = costs.get((0, i))
            _c_j_1 = costs.get((j, 0))
            _c_i_j = costs.get((i, j))
            if _c_1_i == None: _c_1_i = 0
            if _c_j_1 == None: _c_j_1 = 0
            if _c_i_j == None: _c_i_j = 0
            _s = _c_1_i + _c_j_1 - _c_i_j
            _saving[(i, j)] = _s
        
        _savings_sort = {k: v for k, v in sorted(_saving.items(), reverse=True, key=lambda item: item[1])}
        _temp = {val : key for key, val in _savings_sort.items()}  #usuwanie
        _savings_sorted = {val : key for key, val in _temp.items()} #duplikatow
        return _savings_sorted

    def generate_routes(savings, q, Q):
        """
        Method returns dictionaries of routes and their demands
        ---------
        Parameters:
        savings - dict - Key - depots (i, j), Value - savings.
        loc_y - list - List of y coordinates of points
        """
        _routes = {}
        _count = 1
        _copy_q = q.copy()
        _routes = defaultdict(list)
        _demands = dict()

        for i, j in savings:
            if bool(q):
                if i in q or j in q:
                    _values = _routes[_count]
                    _demand = 0
                    if _routes[_count]:
                        for val in _values:
                            _demand += int(_copy_q.get(val, 0))
                    else: 
                        _routes[_count].append(0)

                    if i not in _values and i in q and j not in _values and j in q:
                        _added_demand = int(_copy_q.get(i)) + int(_copy_q.get(j))
                        _demand += _added_demand
                        if _demand <= Q:
                            _routes[_count].append(i)
                            _routes[_count].append(j)
                        elif _added_demand < Q:
                            _demands[_count] = _demand - int(_copy_q.get(i)) - int(_copy_q.get(j))
                            _routes[_count].append(0)
                            _routes[_count+1] = [0, i, j]
                            _count += 1
                            _demands[_count] = _demand - int(_copy_q.get(i)) - int(_copy_q.get(j))
                        q.pop(i, None)
                        q.pop(j, None)

                    elif i in _values and j not in _values and j in q:
                        _demand += int(_copy_q.get(j))
                        if _demand <= Q:
                            if _routes[_count].index(i) == 1:
                                _routes[_count].insert(1, j)
                            else:
                                _routes[_count].append(j)
                        else:
                            _demands[_count] = _demand - int(_copy_q.get(j))
                            _routes[_count].append(0)
                            _routes[_count+1] = [0, j]
                            _count += 1
                            _demands[_count] = _demand - int(_copy_q.get(j))
                        q.pop(j, None)

                    elif i not in _values and i in q and j in _values:
                        _demand += int(_copy_q.get(i))
                        if _demand <= Q:
                            if _routes[_count].index(j) == 1:
                                _routes[_count].insert(1, i)
                            else:
                                _routes[_count].append(i)
                        else:
                            _demands[_count] = _demand - int(_copy_q.get(i))
                            _routes[_count].append(0)
                            _routes[_count+1] = [0, i]
                            _count += 1
                            _demands[_count] = _demand - int(_copy_q.get(i))
                        q.pop(i, None)
     
        _routes[_count].append(0)

        return _routes, _demands

    def routes_full_cost(routes, costs):
        """
        Method returns the total cost of all routes
        ---------
        Parameters:
        routes - dict - Key - number of route, Value - list of depots in the route.
        costs - dict - Key - arc, Value - cost of trip. Example {(0,1): 123, (1,0):123}
        """
        _full_cost = 0

        for key in routes:
            depots = routes.get(key)
            for i in range(len(depots)):
                if i+1 < len(depots):
                    _full_cost += costs[depots[i], depots[i+1]]

        return _full_cost

    def plotting_solution(loc_x=[0], loc_y=[0], demand=[10], vehicle_capacity=20, active_arcs = {0:0}, index = "deafulf_index"):
        """
        Method returns graph of solution in a coordinate network and save it as png file
        ---------
        Parameters:
        loc_x - list - List of x coordinates of points
        loc_y - list - List of y coordinates of points
        demand - list - List of demand of every client
        vehicle_capacity - number of item which can take a vehilce.
        active_arcs - dict - Dictionary of active arcs
        index - string - index name of solution
        """
        _n = len(loc_x) - 1
        _N = [i for i in range(1, _n+1)] #indeksy klinetow
        plt.scatter(loc_x[1:], loc_y[1:], c='b')
        for i in _N:
            plt.annotate('$q_%d=%d$' % (i, demand[i]), (loc_x[i]+2, loc_y[i]))
        for i, j in active_arcs:
            plt.plot([loc_x[i], loc_x[j]], [loc_y[i], loc_y[j]], c='g', alpha=0.3)
        plt.plot(loc_x[0], loc_y[0], c='r', marker='s')
        plt.axis('equal')
        _path = "./data/images/" + index + ".png"
        plt.savefig(_path)

    def read_csv(path = "./data/csv_files/", index = "deafulf_index"):
        """
        Function returns lists of localization and demand and also vehicle capacity
        ------------------
        CSV file order:
        First line - vehicle capacity
        Rest lines - localization x, localization y, demand
        """
        with open('file.csv', newline='') as f:
            reader = csv.reader(f)
            data = list(reader)
        vehicle_capacity = data[0][1]
        loc_x = []
        loc_y = []
        demand = []
        for item in data:
            loc_x.append(item[1])
            loc_y.append(item[3])
            demand.append(item[5])

        return loc_x, loc_y, demand, vehicle_capacity
    
    def save_csv(total_costs = 0, active_arcs = {0:0}, index = "deafulf_index", path = "./data/csv_files/"):
        """
        Function saves calcualtion as csv file
        ------------------
        """
        _file_name = path + index + ".csv"
        with open(_file_name, 'w') as f:
            write = csv.writer(f)
            write.writerow(index)
            write.writerow(active_arcs)
            write.writerow(total_costs)
    # def quantity_of_vehicles(demand, vehicle_capacity = 20):
    #     """ 
    #     Function returns minimal quantity of vehicles
    #     ---------------
    #     Paramteres:
    #     demand - list - list of clients demand. Example: [1, 2, 3]
    #     vehicle_capacity - int - capacity of vehicle. Example: 4
    #     """
    #     if max(demand) > vehicle_capacity:
    #         vehicle_capacity = max(demand)
    #     _num_vehicle = 1
    #     _total_demand = 0
    #     for i, val in enumerate(demand):
    #         _total_demand = val + _total_demand
    #         if i + 1 == len(demand):
    #             return _num_vehicle
    #         if _total_demand + demand[i + 1] >= vehicle_capacity:
    #             _num_vehicle += 1
    #             _total_demand = 0