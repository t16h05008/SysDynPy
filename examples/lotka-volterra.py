import pprint

from sysdynpy.system import *
from sysdynpy.stock import *
from sysdynpy.flow import *
from sysdynpy.dynamicvariable import *
from sysdynpy.parameter import *
from sysdynpy.simulator import *
from sysdynpy.exporter import *

"""
This example implements the Lotka-Volterra model.
The corresponding simulation diagram can be found in the file
"simulation-diagram-lotka-volterra.png".
"""

number_of_simulation_steps = 200

# create system
lv_system = System("lotka-volterra")

# create elements
predators = Stock(name="Predators", value=40, system=lv_system, var_name="predators",
    calc_rule=lambda: increase_in_predators - energy_loss)
prey = Stock(name="Prey", value=500, system=lv_system, var_name="prey", 
    calc_rule=lambda: increase_in_prey - decrease_in_prey)

GROWTH_RATE_PREY = Parameter(name="GROWTH RATE PREY", value=0.05,
system=lv_system, var_name="GROWTH_RATE_PREY")
LOSS_RATE_PREY = Parameter(name="LOSS RATE PREY", value=0.001,
    system=lv_system, var_name="LOSS_RATE_PREY")
GROWTH_RATE_PREDATORS = Parameter(name="GROWTH RATE PREDATORS", value=0.0002,
    system=lv_system, var_name="GROWTH_RATE_PREDATORS")
ENERGY_LOSS_RATE_PREDATORS = Parameter(name="ENERGY LOSS RATE PREDATORS", value=0.1,
    system=lv_system, var_name="ENERGY_LOSS_RATE_PREDATORS")

increase_in_prey = Flow(name="increase in prey", system=lv_system,
    var_name="increase_in_prey", calc_rule=lambda: GROWTH_RATE_PREY * prey)
decrease_in_prey = Flow(name="decrease in prey", system=lv_system,
    var_name="decrease_in_prey", calc_rule=lambda: LOSS_RATE_PREY * encounters)
increase_in_predators = Flow(name="increase in predators", system=lv_system,
    var_name="increase_in_predators", calc_rule=lambda: encounters * GROWTH_RATE_PREDATORS)
energy_loss = Flow(name="energy loss", system=lv_system,
    var_name="energy_loss", calc_rule=lambda: ENERGY_LOSS_RATE_PREDATORS * predators)

encounters = DynamicVariable(name="encounters", system=lv_system, var_name="encounters",
    calc_rule=lambda: prey * predators)

# link elements
predators.input_elements.extend([increase_in_predators, energy_loss])
prey.input_elements.extend([increase_in_prey, decrease_in_prey])

increase_in_prey.input_elements.extend([prey, GROWTH_RATE_PREY])
decrease_in_prey.input_elements.extend([encounters, LOSS_RATE_PREY])
increase_in_predators.input_elements.extend([GROWTH_RATE_PREDATORS, encounters])
energy_loss.input_elements.extend([ENERGY_LOSS_RATE_PREDATORS, predators])

encounters.input_elements.extend([prey, predators])

# run simulation
s1 = Simulator(number_of_simulation_steps, "weeks")
s1.run_simulation(lv_system)
# get_simulation_results() returns a dict
# Key = Name of the system element, Value = List of numerical values
sim_results = s1.get_simulation_results()
# pprint.pprint(sim_results) # print formatted results to console

# export results to various formats
# make sure the subfolder "results" exists or change the relative path
Exporter.export_data(results=sim_results, file_format="csv", \
    system_elements=["Predators", "Prey"], rel_path="./results/lotka-volterra-results.csv")

Exporter.export_data(results=sim_results, file_format="json", \
    system_elements=["Predators", "Prey"], rel_path=".\\results\\lotka-volterra-results.json")

Exporter.export_graph(results=sim_results, file_format="jpg", \
    system_elements=["Predators", "Prey"], rel_path="results/lotka-volterra-results", \
    title="Lotka-Volterra simulation", label_x="t[weeks]", label_y="Number of Animals",
    range_x=[0,number_of_simulation_steps], range_y=[0,600], colors=["red", "blue"],
    line_width=2, legend_pos="upper right")

Exporter.export_graph(results=sim_results, file_format="png", \
    system_elements=["Prey", "Predators"], rel_path="results\\lotka-volterra-results", \
    title="Lotka-Volterra simulation", label_x="t[weeks]", label_y="Number of Animals",
    range_x=[0,number_of_simulation_steps], range_y=[0,600], colors=["green", "orange"],
    line_width=2, legend_pos="upper left")