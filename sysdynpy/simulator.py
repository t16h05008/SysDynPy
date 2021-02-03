import time
import copy
from asteval import Interpreter

import numbers
import sysdynpy.utils as utils



class Simulator(utils.SubclassOnlyABC):
    """This abstract class can be used to run simulations for a given system.
    """


    aeval = Interpreter()
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
                        system.system_elements[idx].value = \
                            cls._calculate_dynamic_value(elem)
                    except TypeError as t:
                        raise t
            
            # now calculate stocks
            for idx, elem in enumerate(system.system_elements):
                current_stock_value = system.system_elements[idx].value
                if "Stock" in str(type(elem)):
                    try:
                        change = cls._calculate_stock_value(elem)
                        system.system_elements[idx].value = current_stock_value + change
                    except TypeError as t:
                        raise t
            
            system.show_system_elements()
            time.sleep(1)
    
    @staticmethod
    def _calculate_dynamic_value(element):
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
                    calc_rule.replace(inp_elem.name, str(Simulator._calculate_dynamic_value(inp_elem)))

        # calculate value
        result = Simulator.aeval(calc_rule)

        if not isinstance(result, numbers.Number):
            raise TypeError("The result of is not numeric. Is is: " + str(result))
        else:
            return result

    @staticmethod
    def _calculate_stock_value(stock):
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
        result = Simulator.aeval(calc_rule)

        if not isinstance(result, numbers.Number):
            raise TypeError("The result of is not numeric. Is is: " + str(result))
        else:
            return result
