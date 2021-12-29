import numpy as np
import matplotlib.pyplot as plt

class Cvrp():
    
    def ploting_points(loc_x = [0], loc_y = [0], demand = [10], vehicle_capacity = 20):
        """
        Method returns graph of points in a coordinate network and save it into png file
        ---------
        Parameters:
        loc_x - list - List of x coordinates of points
        loc_y - list - List of y coordinates of points
        demand - list - List of demand of every client
        vehicle_capacity - number of item which can take a vehilce.
        """
        if max(demand) > vehicle_capacity:
            vehicle_capacity = max(demand)
        _n = len(loc_x)
        _N = [i for i in range(1, _n+1)] #indeksy klinetow
        #_V = [0] + _N # indeksy pojazdow    
        plt.scatter(loc_x[1:], loc_y[1:], c='b')
        for i in _N:
            plt.annotate('$q_%d=%d$' % (i, demand[i]), (loc_x[i]+2, loc_y[i]))
        plt.plot(loc_x[0], loc_y[0], c='r', marker='s')
        plt.axis('equal')
        plt.savefig('points.png')

    def generate_arcs_and_costs(loc_x = [0], loc_y = [0]):
        """
        Function returns a list of arcs  and list of costs
        ---------
        Parameters:
        loc_x - list - List of x coordinates of points
        loc_y - list - List of y coordinates of points
        """
        _n = len(loc_x)
        _N = [i for i in range(1, _n+1)] #indeksy klinetow
        _V = [0] + _N # indeksy pojazdow   
        _rows = [(i, j) for i in _V for j in _V if i != j] #zestawienie łuków
        _costs = {(i, j): np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j]) for i, j in _rows}#koszt przejazdu
        return _rows, _costs

    def quantity_of_vehicles(demand, vehicle_capacity = 20):
        """ 
        Function returns minimal quantity of vehicles
        ---------------
        Paramteres:
        demand - list - list of clients demand. Example: [1, 2, 3]
        vehicle_capacity - int - capacity of vehicle. Example: 4
        """
        if max(demand) > vehicle_capacity:
            vehicle_capacity = max(demand)
        _num_vehicle = 1
        _total_demand = 0
        for i, val in demand:
            _total_demand = val + _total_demand
            if i == len(demand):
                return _num_vehicle
            if _total_demand + demand[i + 1] >= vehicle_capacity:
                _num_vehicle += 1
                _total_demand = 0