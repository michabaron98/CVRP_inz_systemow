import numpy as np
from CVRP import Cvrp
rnd = np.random
rnd.seed(0)

n = 5 #liczba klientow
Q = 50 #pojemnosc pojazdow
N = [i for i in range(1, n+1)] #indeksy klinetow
V = [0] + N #indeksy pojazdow
q = {i: rnd.randint(1, Q+1) for i in N} #zapotrzebowanie klientow

loc_x = rnd.rand(n)*200
loc_y = rnd.rand(n)*100

arcs, costs = Cvrp.generate_arcs_and_costs(loc_x, loc_y)
print(arcs)
print(costs)
saving = Cvrp.generate_saving_matrix(arcs, costs)
print(f"saving: {saving}")
routes, demands = Cvrp.generate_routes(saving, q, Q)
full_cost = Cvrp.routes_full_cost(routes, costs)
print(f"routes: {routes}")
print(f"q: {q}")
Cvrp.plotting_solution(loc_x, loc_y, [3,4,5,6,7] ,Q, routes, index = "calc_code", )