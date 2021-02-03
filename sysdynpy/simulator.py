import time
import copy
import sysdynpy.utils as utils

class Simulator(utils.SubclassOnlyABC):
    """This abstract class can be used to run simulations for a given system.
    """

    system_states = []

    @classmethod
    def run_simulation(cls, system):
        """TODO
        """

        for i in range(system.simulation_steps):
            print("Starting simulation step " + str(i+1) + " of "
                + str(system.simulation_steps))
            # make a deep copy of the current system state
            system_backup = copy.deepcopy(system)

            # calculate dynamic variables and flows from parameters and stocks
            # use the backed-up system as source but update the actual system
            for idx, elem in enumerate(system_backup.system_elements):
                if "Flow" in str(type(elem)) or "DynamicVariable" in str(type(elem)):
                    try:
                        # update system state
                        system.system_elements[idx].value = utils._calculate_dynamic_value(elem)
                    except TypeError as t:
                        raise t
            
            # now calculate stocks
            for idx, elem in enumerate(system.system_elements):
                current_stock_value = system.system_elements[idx].value
                if "Stock" in str(type(elem)):
                    try:
                        change = utils._calculate_stock_value(elem)
                        system.system_elements[idx].value = current_stock_value + change
                    except TypeError as t:
                        raise t
            
            system.show_system_elements()
            time.sleep(1)