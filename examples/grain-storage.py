import pprint

from sysdynpy.system import *
from sysdynpy.stock import *
from sysdynpy.flow import *
from sysdynpy.dynamicvariable import *
from sysdynpy.parameter import *
from sysdynpy.simulator import *
from sysdynpy.exporter import *

"""
This example implements the grain storage system presented in:
Bala, B. K., Arshad, F. M. & Noh, K. M. (2017)
System dynamics. Modelling and simulation (Springer texts in business and economics).
Singapore: Springer.
Page 75-77

The corresponding simulation diagram can be found in the file
"simulation-diagram-grain-storage.png".
Note that elements are named slightly different.
"""

# create system
number_of_simulation_steps = 100
gs_system = System("Grain Stock Storage")

# create elements
grain_on_order = Stock(name="grain on order", value=10000, system=gs_system,
    var_name="grain_on_order", calc_rule=lambda: procurement_rate-receiving_rate)
grain_stock = Stock(name="grain stock", value=1000, system=gs_system,
    var_name="grain_stock", calc_rule=lambda: receiving_rate - release_rate)

ADJUSTMENT_DELAY = Parameter(name="ADJUSTMENT DELAY", value=5, system=gs_system,
    var_name="ADJUSTMENT_DELAY")
DESIRED_GRAIN_STOCK = Parameter(name="DESIRED GRAIN STOCK", value=6000, system=gs_system,
    var_name="DESIRED_GRAIN_STOCK")
RECEIVING_DELAY = Parameter(name="RECEIVING DELAY", value=10, system=gs_system,
    var_name="RECEIVING_DELAY")
RELEASE_FRACTION = Parameter(name="RELEASE FRACTION", value=0.025, system=gs_system,
    var_name="RELEASE_FRACTION")

procurement_rate = Flow(name="procurement rate", system=gs_system, var_name="procurement_rate",
    calc_rule=lambda: (DESIRED_GRAIN_STOCK - grain_stock)/ADJUSTMENT_DELAY)
receiving_rate = Flow(name="receiving rate", system=gs_system,
    var_name="receiving_rate", calc_rule=lambda: grain_on_order/RECEIVING_DELAY)
release_rate = Flow(name="release rate", system=gs_system,
    var_name="release_rate", calc_rule=lambda: grain_stock*RELEASE_FRACTION)

# link elements
grain_on_order.input_elements.extend([procurement_rate, receiving_rate])
grain_stock.input_elements.extend([receiving_rate, release_rate])

procurement_rate.input_elements.extend([ADJUSTMENT_DELAY, DESIRED_GRAIN_STOCK, grain_stock])
receiving_rate.input_elements.extend([grain_on_order, RECEIVING_DELAY])
release_rate.input_elements.extend([grain_stock, RELEASE_FRACTION])

# run simulation
s1 = Simulator(number_of_simulation_steps, "weeks")
s1.run_simulation(gs_system) 
# get_simulation_results() returns a dict
# Key = Name of the system element, Value = List of Values
sim_results = s1.get_simulation_results()
# pprint.pprint(sim_results) # print formatted results to console

# export results to various formats
# make sure the subfolder "results" exists or change the relative path
Exporter.export_data(results=sim_results, file_format="csv", \
    system_elements=["procurement rate", "receiving rate", "grain stock", "DESIRED GRAIN STOCK"], \
    rel_path="./results/grain-stock-storage-results.csv")

Exporter.export_data(results=sim_results, file_format="json", \
    system_elements=["procurement rate", "receiving rate", "grain stock", "DESIRED GRAIN STOCK"], \
    rel_path=".\\results\\grain-stock-storage-results.json")

Exporter.export_graph(results=sim_results, file_format="png", \
    system_elements=["procurement rate", "receiving rate", "grain stock", "DESIRED GRAIN STOCK"], \
    rel_path="results/grain-stock-storage-results.png", \
    title=gs_system.name, label_x="t[weeks]", label_y="Grain",
    range_x=[0,number_of_simulation_steps], range_y=[-500,8100], colors=["blue", "red", "purple", "green"],
    line_width=2, legend_pos="upper right")