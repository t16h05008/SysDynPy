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
"simulation-diagram-lotka-volterra_german.png".
"""

number_of_simulation_steps = 200

# create system
lv_system = System("lotka-volterra")

# create elements
raeuber = Stock(name="Räuber", value=40, system=lv_system, var_name="raeuber",
    calc_rule=lambda: raeuberzuwachs - energieverluste)
beute = Stock(name="Beute", value=500, system=lv_system, var_name="beute",
    calc_rule=lambda: beutezuwachs - beuteverlust)

WACHSTUMSRATE_BEUTE = Parameter(name="WACHSTUMSRATE BEUTE", value=0.05,
    system=lv_system, var_name="WACHSTUMSRATE_BEUTE")
VERLUSTRATE_BEUTE = Parameter(name="VERLUSTRATE BEUTE", value=0.001,
    system=lv_system, var_name="VERLUSTRATE_BEUTE")
ZUWACHSRATE_RAEUBER = Parameter(name="ZUWACHSRATE RÄUBER", value=0.0002,
    system=lv_system, var_name="ZUWACHSRATE_RAEUBER")
ENERGIEVERLUSTRATE_RAEUBER = Parameter(name="ENERGIEVERLUSTRATE RÄUBER", value=0.1,
    system=lv_system, var_name="ENERGIEVERLUSTRATE_RAEUBER")

beutezuwachs = Flow(name="Beutezuwachs", system=lv_system,
    var_name="beutezuwachs", calc_rule=lambda: WACHSTUMSRATE_BEUTE * beute)
beuteverlust = Flow(name="Beuteverlust", system=lv_system,
    var_name="beuteverlust", calc_rule=lambda: VERLUSTRATE_BEUTE * treffen)
raeuberzuwachs = Flow(name="Raeuberzuwachs", system=lv_system,
    var_name="raeuberzuwachs", calc_rule=lambda: treffen * ZUWACHSRATE_RAEUBER)
energieverluste = Flow(name="Energieverluste", system=lv_system,
    var_name="energieverluste", calc_rule=lambda: ENERGIEVERLUSTRATE_RAEUBER * raeuber)

treffen = DynamicVariable(name="Treffen", system=lv_system, var_name="treffen",
    calc_rule=lambda: beute * raeuber)

# link elements
raeuber.input_elements.extend([raeuberzuwachs, energieverluste])
beute.input_elements.extend([beutezuwachs, beuteverlust])

beutezuwachs.input_elements.extend([beute, WACHSTUMSRATE_BEUTE])
beuteverlust.input_elements.extend([treffen, VERLUSTRATE_BEUTE])
raeuberzuwachs.input_elements.extend([ZUWACHSRATE_RAEUBER, treffen])
energieverluste.input_elements.extend([ENERGIEVERLUSTRATE_RAEUBER, raeuber])

treffen.input_elements.extend([beute, raeuber])

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
    system_elements=["Räuber", "Beute"], rel_path="./results/lotka-volterra-results.csv")

Exporter.export_data(results=sim_results, file_format="json", \
    system_elements=["Räuber", "Beute"], rel_path=".\\results\\lotka-volterra-results.json")

Exporter.export_graph(results=sim_results, file_format="jpg", \
    system_elements=["Räuber", "Beute"], rel_path="results/lotka-volterra-results", \
    title="Lotka-Volterra-Simulation", label_x="t[weeks]", label_y="Number of Animals",
    range_x=[0,number_of_simulation_steps], range_y=[0,600], colors=["red", "blue"],
    line_width=2, legend_pos="upper right")

Exporter.export_graph(results=sim_results, file_format="png", \
    system_elements=["Beute", "Räuber"], rel_path="results\\lotka-volterra-results", \
    title="Lotka-Volterra-Simulation", label_x="t[weeks]", label_y="Number of Animals",
    range_x=[0,number_of_simulation_steps], range_y=[0,600], colors=["green", "orange"],
    line_width=2, legend_pos="upper left")