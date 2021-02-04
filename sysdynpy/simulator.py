import time
import copy
from asteval import Interpreter

import numbers
import sysdynpy.utils as utils



class Simulator(utils.SubclassOnlyABC):
    """This abstract class can be used to run simulations for a given system.
    """


    _aeval = Interpreter()
    _system_states = []

    @classmethod
    def run_simulation(cls, system):
        """TODO
        """

        """
        In the initial iteration values for dynamic variables and
        flows are calculated, but nothing else changes. So we need one iteration
        more to get the required number of steps
        """
        for i in range(int(system.simulation_steps / system.dt)+1):

            # make a deep copy of the current system state
            system_backup = copy.deepcopy(system)

            # calculate dynamic variables and flows from parameters and stocks
            # use the backed-up system as source but update the actual system
            for idx, elem in enumerate(system_backup.system_elements):
                if "Flow" in str(type(elem)) or "DynamicVariable" in str(type(elem)):
                    try:
                        # update system state
                        system.system_elements[idx].value = \
                            cls._calculate_dynamic_value(elem)
                    except TypeError as t:
                        raise t

            
            if i == 0:
                # in the first iteration only store the initial system state
                system_backup = copy.deepcopy(system)
                cls._system_states.append(system_backup)
                continue

            # store copy of system state every 1 / dt steps
            # example: dt = 0.05 --> every 20 steps
            if i % (1 / system.dt) == 0:
                cls._system_states.append(system_backup)

            # now calculate stocks
            for idx, elem in enumerate(system.system_elements):
                current_stock_value = system.system_elements[idx].value
                if "Stock" in str(type(elem)):
                    try:
                        change = cls._calculate_stock_change(elem)
                        system.system_elements[idx].value = current_stock_value + change * system.dt
                    except TypeError as t:
                        raise t
            
            

    @classmethod
    def get_simulation_results(cls):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        if not cls._system_states: # empty
            return None
        else:
            result = {}
            # create dict from list of system states
            # for each state
            for state in cls._system_states:
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
