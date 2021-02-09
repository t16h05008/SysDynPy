import time
import copy
from asteval import Interpreter
import numbers

import sysdynpy.utils as utils



class Simulator(object):
    """Can be used to run simulations for a given system.
    """

    VALID_TIME_UNITS = ("milliseconds", "seconds", "minutes",
        "hours", "days", "weeks", "months", "years")
    """Possible values for the property :code:`time_unit`.
    """
    _aeval = Interpreter()
    """An Interpreter to evaluate python expressions. It is intentionally
    limited to arithmetic operations for security reasons.
    Further documentionen: `asteval <https://github.com/newville/asteval>`__
    """

    def __init__(self, simulation_steps = 10, time_unit = "days", dt=0.05):
        """Constructor method

        :param simulation_steps: The number of steps to simulate
            when run_simulation() is called, defaults to 10
        :type simulation_steps: int
        :param time_unit: Defines the time period of one simulation step.
            The value must be one of the values defines in :code:`VALID_TIME_UNITS`
            , defaults to "days"
        :type time_unit: str
        :param dt: The interval between calculations. Must be a number between
            zero and one. The reciprocal of this argument is the number of 
            calculation steps per simulation step. One means that the system 
            element values are calculated once per simulation step. Smaller 
            numbers result in higher accuracy but longer calculation times while 
            greater numbers lead to faster calculations but lower accuracy.
            Defaults to 0.05.

            |  Example: 
            |  0.05 means the reciprocal is 1 / 0.05 = 20. So by default
               20 calculations are done per simulation step.
        :type dt: float
        """
        self.simulation_steps = simulation_steps
        self.time_unit = time_unit
        self.dt = dt
        self._system_states = []
        """ Stores the system state after each simulation step.
        
        :type: list
        """


    def run_simulation(self, system):
        """Runs a simulation for the given system.

        Once the simulation is finished, results are available by calling
        :py:meth:`~get_simulation_results`

        :param system: The system to run a simulation for.
        :type system: System
        """

        print("Simulation started")
        """
        In the initial iteration values for dynamic variables and
        flows are calculated, but nothing else changes. So we need one iteration
        more to get the required number of steps
        """
        
        for i in range(int(self.simulation_steps / self.dt)+1):
            
            # make a deep copy of the current system state
            system_backup = copy.deepcopy(system)

            # calculate dynamic variables and flows from parameters and stocks
            # use the backed-up system as source but update the actual system
            for idx, elem in enumerate(system_backup._system_elements):
                if "Flow" in str(type(elem)) or "DynamicVariable" in str(type(elem)):
                    try:
                        # update system state
                        system._system_elements[idx].value = \
                            Simulator._calculate_dynamic_value(elem)
                    except TypeError as t:
                        raise t

            
            if i == 0:
                # in the first iteration only store the initial system state
                system_backup = copy.deepcopy(system)
                self._system_states.append(system_backup)
                continue

            # store copy of system state every 1 / dt steps
            # example: dt = 0.05 --> every 20 steps
            if i % (1 / self.dt) == 0:
                self._system_states.append(system_backup)

            # now calculate stocks
            for idx, elem in enumerate(system._system_elements):
                current_stock_value = system._system_elements[idx].value
                if "Stock" in str(type(elem)):
                    try:
                        change = Simulator._calculate_stock_change(elem)
                        system._system_elements[idx].value = current_stock_value + change * self.dt
                    except TypeError as t:
                        raise t
            
        print("Simulation finished")


    def get_simulation_results(self):
        """Provides the trajectories of all system elements during the
        simulation. Must be called after the simulation.

        :return: 
            A dictionary where each key corresponds to the name of a
            system element. The values are lists. For each simulation step
            a list contains the value of the system element (key) at that
            simulation step.

            Example:

            .. code-block:: python

                {
                    someStockName: [10, 7.5, 5, 3.5, 2.5, 3, 3],
                    someFlowName: [0, -2.5, -2, -1.5, -1, 0, 0],
                    someParameterName: [3, 3, 3, 3, 3, 3, 3]
                }
        :rtype: None or dict
        """
        if not self._system_states: # empty
            return None
        else:
            result = {}
            # create dict from list of system states
            # for each state
            for state in self._system_states:
                # iterate system elements
                for element in state._system_elements:
                    if element.name not in result:
                        result[element.name] = [element.value]
                    else:
                        result[element.name].append(element.value)
        return result

    
    @classmethod
    def _calculate_dynamic_value(cls, element):
        """Calculates the values for a given element based on the calculation rule.

        This is a recursive function to calculate the value of a flow or
        dynamic variable. The values of flows or dynamic variables can always be
        deduced from parameters or stocks. But it can not be assumed that a dynamic
        variable or flow **directly** depends on only parameters or stocks.

        :param element: The element to calculate a value for.
        :type element: Flow or DynamicVariable
        :raises TypeError: If the calculation rule does not evaluate to a numerical result
        :return: The calculated value
        :rtype: float
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
        """Calculates the values for a given stock based on the calculation rule.

        Unlike with :py:meth:`~_calculate_dynamic_value` no recursion is needed here.

        :param stock: The stock to calculate a value for.
        :type stock: Stock
        :raises TypeError: If the calculation rule does not evaluate to a numerical result
        :return: The calculated value
        :rtype: float
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
        """see :py:meth:`~__init__`
        """
        return self._simulation_steps


    @property
    def time_unit(self):
        """see :py:meth:`~__init__`
        """
        return self._time_unit
    

    @property
    def dt(self):
        """see :py:meth:`~__init__`
        """
        return self._dt
    

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
            raise ValueError("Given time unit " + value + " is not allowed. " \
                + "Allowed values are: " + str(Simulator.VALID_TIME_UNITS))
    

    @dt.setter
    def dt(self, value):
        if 0 < value and value <= 1:
            self._dt = value

