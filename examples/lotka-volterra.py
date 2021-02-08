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

# create system
number_of_simulation_steps = 200
lv_system = System("lotka-volterra", number_of_simulation_steps, "weeks")

# create elements
raeuber = Stock("Räuber", 40, lv_system)
beute = Stock("Beute", 500, lv_system)

WACHSTUMSRATE_BEUTE = Parameter("WACHSTUMSRATE_BEUTE", 0.05, lv_system)
VERLUSTRATE_BEUTE = Parameter("VERLUSTRATE_BEUTE", 0.001, lv_system)
ZUWACHSRATE_RAEUBER = Parameter("ZUWACHSRATE_RÄUBER", 0.0002, lv_system)
ENERGIEVERLUSTRATE_RAEUBER = Parameter("ENERGIEVERLUSTRATE_RÄUBER", 0.1, lv_system)

beutezuwachs = Flow("Beutezuwachs", lv_system)
beuteverlust = Flow("Beuteverlust", lv_system)
raeuberzuwachs = Flow("Räuberzuwachs", lv_system)
energieverluste = Flow("Energieverluste", lv_system)

treffen = DynamicVariable("Treffen", lv_system)

# link elements
raeuber.input_elements.extend([raeuberzuwachs, energieverluste])
raeuberzuwachs.input_elements.extend([ZUWACHSRATE_RAEUBER, treffen])
energieverluste.input_elements.extend([ENERGIEVERLUSTRATE_RAEUBER, raeuber])

treffen.input_elements.extend([beute, raeuber])

beute.input_elements.extend([beutezuwachs, beuteverlust])
beutezuwachs.input_elements.extend([beute, WACHSTUMSRATE_BEUTE])
beuteverlust.input_elements.extend([treffen, VERLUSTRATE_BEUTE])

# set calculation rules
raeuber.calc_rule = "Räuberzuwachs - Energieverluste"
raeuberzuwachs.calc_rule = "Treffen * ZUWACHSRATE_RÄUBER"
energieverluste.calc_rule = "ENERGIEVERLUSTRATE_RÄUBER * Räuber"

treffen.calc_rule = "Beute * Räuber"

beute.calc_rule = "Beutezuwachs - Beuteverlust"
beutezuwachs.calc_rule = "WACHSTUMSRATE_BEUTE * Beute"
beuteverlust.calc_rule = "VERLUSTRATE_BEUTE * Treffen"

Simulator.run_simulation(lv_system) # run simulation
# returns a dict
# Key = Name of the system element, Value = List of Values
sim_results = Simulator.get_simulation_results()
# pprint.pprint(sim_results) # print formatted results to console

# export results to various formats
# make sure the subfolder "results" exists or change the relative path
Exporter.export_data(results=sim_results, file_format="csv", \
    system_elements=["Räuber", "Beute"], rel_path="./results/lotka-volterra-results.csv")

Exporter.export_data(results=sim_results, file_format="json", \
    system_elements=["Räuber", "Beute"], rel_path=".\\results\\lotka-volterra-results.json")

Exporter.export_graph(results=sim_results, file_format="png", \
    system_elements=["Räuber", "Beute"], rel_path="results/lotka-volterra-results", \
    title="Lotka-Volterra-Simulation", label_x="t[weeks]", label_y="Number of Animals",
    range_x=[0,number_of_simulation_steps], range_y=[0,600], colors=["red", "blue"],
    line_width=2, legend_pos="upper right")

Exporter.export_graph(results=sim_results, file_format="png", \
    system_elements=["Beute", "Räuber"], rel_path="results\\lotka-volterra-results", \
    title="Lotka-Volterra-Simulation", label_x="t[weeks]", label_y="Number of Animals",
    range_x=[0,number_of_simulation_steps], range_y=[0,600], colors=["green", "orange"],
    line_width=2, legend_pos="upper left")