import time
import copy
from asteval import Interpreter
import numbers

import sysdynpy.utils as utils



class Simulator(object):
    """This class can be used to run simulations for a given system.

    :param simulation_steps: The number of steps to simulate 
        when run_simulation() is called, defaults to 10
    :type simulation_steps: int, optional
    :param time_unit: Defines the time period of one simulation step.
        The value must be one of the values defines in :code:`VALID_TIME_UNITS`
    :type time_unit: str, optional, defaults to :code:`days`.
    """

    VALID_TIME_UNITS = ("milliseconds", "seconds", "minutes",
        "hours", "days", "weeks", "months", "years")
    """Possible values for the property :code:`time_unit`.
    """
    _aeval = Interpreter()
    """TODO"""

    def __init__(self, simulation_steps = 10, time_unit = "days", dt=0.05):
        self.simulation_steps = simulation_steps
        self.time_unit = time_unit
        self.dt = dt
        self._system_states = []


    def run_simulation(self, system):
        """TODO
        """

        """
        In the initial iteration values for dynamic variables and
        flows are calculated, but nothing else changes. So we need one iteration
        more to get the required number of steps
        """
        print("Simulation started")
        for i in range(int(self.simulation_steps / self.dt)+1):
            
            # make a deep copy of the current system state
            system_backup = copy.deepcopy(system)

            # calculate dynamic variables and flows from parameters and stocks
            # use the backed-up system as source but update the actual system
            for idx, elem in enumerate(system_backup.system_elements):
                if "Flow" in str(type(elem)) or "DynamicVariable" in str(type(elem)):
                    try:
                        # update system state
                        system.system_elements[idx].value = \
                            Simulator._calculate_dynamic_value(elem)
                    except TypeError as t:
                        raise t

            
            if i == 0:
                # in the first iteration only store the initial system state
                system_backup = copy.deepcopy(system)
                self.system_states.append(system_backup)
                continue

            # store copy of system state every 1 / dt steps
            # example: dt = 0.05 --> every 20 steps
            if i % (1 / self.dt) == 0:
                self.system_states.append(system_backup)

            # now calculate stocks
            for idx, elem in enumerate(system.system_elements):
                current_stock_value = system.system_elements[idx].value
                if "Stock" in str(type(elem)):
                    try:
                        change = Simulator._calculate_stock_change(elem)
                        system.system_elements[idx].value = current_stock_value + change * self.dt
                    except TypeError as t:
                        raise t
            
        print("Simulation finished")


    def get_simulation_results(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        if not self.system_states: # empty
            return None
        else:
            result = {}
            # create dict from list of system states
            # for each state
            for state in self.system_states:
                # iterate system elements
                for element in state.system_elements:
                    if element.name not in result:
                        result[element.name] = [element.value]
                    else:
                        result[element.name].append(element.value)
        return result

    
    @classmethod
    def _calculate_dynamic_value(cls, element):
        """Calculates the values for a given element based on the calculation rule.

        This is a recursive function to calculate the value of a Flow or
        dynamic variable. The values of flows or dynamic variables can always be
        deduced from parameters or stocks. But it can not be assumed that a dynamic
        variable or flow **directly** depends on only parameters or stocks.

        :param element: The element to calculate a value for.
        :type element: Flow or DynamicVariable
        :raises TypeError: If the calculation rule does not evaluate to a numerical result
        :return: The calculated value
        :rtype: double
        """
        result = None
        calc_rule = element.calc_rule

        # for each input element
        for idx, inp_elem in enumerate(element.input_elements):
            # check its type
            if "Stock" in str(type(inp_elem)) or "Parameter" in str(type(inp_elem)):
                # if stock or parameter replace name in calculation rule
                calc_rule = \
                    calc_rule.replace(inp_elem.name, str(inp_elem.value))
            else:
                # else call this function again and replace name with result
                # print("calling recursive function for input element " + inp_elem.name + " of element " + element.name)
                calc_rule = \
                    calc_rule.replace(inp_elem.name, str(cls._calculate_dynamic_value(inp_elem)))

        # calculate value
        result = cls._aeval(calc_rule)

        if not isinstance(result, numbers.Number):
            raise TypeError("The result of is not numeric. Is is: " + str(result))
        else:
            return result

    @classmethod
    def _calculate_stock_change(cls, stock):
        """[summary]

        Unlike with _calculate_dynamic_value no recursion is needed here.

        :param stock: [description]
        :type stock: [type]
        """
        result = None
        calc_rule = stock.calc_rule

        # for each input element
        for idx, inp_elem in enumerate(stock.input_elements):
            # replace name in calculation rule
            calc_rule = calc_rule.replace(inp_elem.name, str(inp_elem.value))

        # calculate value
        result = cls._aeval(calc_rule)

        if not isinstance(result, numbers.Number):
            raise TypeError("The result of is not numeric. Is is: " + str(result))
        else:
            return result

    @property
    def simulation_steps(self):
        """int: The number of steps for the simulation.
        """
        return self._simulation_steps


    @property
    def time_unit(self):
        """str: Defines the time period of one simulation step.
        The value must be one of the values defines in :code:`VALID_TIME_UNITS`
        """
        return self._time_unit
    

    @property
    def dt(self):
        """TODO
        """
        return self._dt
    

    @property
    def system_states(self):
        return self._system_states


    @simulation_steps.setter
    def simulation_steps(self, value):
        if value > 0:
            self._simulation_steps = value
        else:
            raise ValueError("simulation_steps must be positive.")


    @time_unit.setter
    def time_unit(self, value):
        if value.strip().lower() in Simulator.VALID_TIME_UNITS:
            self._time_unit = value.strip().lower()
        else:
            raise ValueError("name can not be empty")
    

    @dt.setter
    def dt(self, value):
        if 0 < value and value <= 1:
            self._dt = value

