from sysdynpy.system import *
from sysdynpy.stock import *
from sysdynpy.flow import *
from sysdynpy.dynamicvariable import *
from sysdynpy.parameter import *

# This example implements the Lotka-Volterra model.

# create system
lv_system = System("lotka-volterra", 7, "weeks")

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
raeuber.calc_rule = "Räuberzuwachs * Energieverluste"
raeuberzuwachs.calc_rule = "Treffen * ZUWACHSRATE_RÄUBER"
energieverluste = "ENERGIEVERLUSTRATE_RÄUBER * Räuber"

treffen.calc_rule = "Beute * Räuber"

beute.calc_rule = "Beutezuwachs - Beuteverlust"
beutezuwachs.calc_rule = "WACHSTUMSRATE_BEUTE * Beute"
beuteverlust.calc_rule = "VERLUSTRATE_BEUTE * Treffen"

lv_system.show_system_elements()

#lv_system.run_simulation()
#lv_system.export_simulation_results()
#lv_system.visualize_simulation_results(raeuber, beute)
