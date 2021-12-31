import numpy as np
import matplotlib.pyplot as plt

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
        
        _saving_sorted = {k: v for k, v in sorted(_saving.items(), key=lambda item: item[1])}
        return _saving_sorted

    def plotting_solution(loc_x=[0], loc_y=[0], demand=[10], vehicle_capacity=20, active_arcs = {0:0}):
        """
        Method returns graph of solution in a coordinate network and save it as png file
        ---------
        Parameters:
        loc_x - list - List of x coordinates of points
        loc_y - list - List of y coordinates of points
        demand - list - List of demand of every client
        vehicle_capacity - number of item which can take a vehilce.
        active_arcs - dict - Dictionary of active arcs
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
        plt.savefig("Solution.png")


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
