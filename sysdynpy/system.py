class System(object):
    """This class represents a System Dynamics system/model.

    :param name: The system name
    :type name: str, required
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
    

    def __init__(self, name, simulation_steps = 10, time_unit = "days", dt=0.05):
        """Constructor method
        """
        self.name = name
        self.simulation_steps = simulation_steps
        self.time_unit = time_unit
        self.dt = dt
        self._system_elements = []
        """private list of system elements
        """


    def show_system_elements(self):
        """Creates a string with information about the system elements.

        This includes the properties :code:`name` and :code:`value`. Depending on the system
        element :code:`calc_rule` and :code:`input_elements` are given as additional
        information. :code:`input_elements` only shows the name of all direct input
        elements to prevent recursion.
        The string is printed to the console.
        """
        s = ""
        s += "==== " + self.name + " ====\n"
        for element in self.system_elements:
            s += "{ name: " + element.name \
                + ", value: " + str(element.value)
            if hasattr(element, "calc_rule"):
                s += ", calc_rule: [" + element.calc_rule + "]"
            if hasattr(element, "input_elements"):
                s += ", input_elements: ["
                for idx, input_element in enumerate(element.input_elements):
                    if idx < len(element.input_elements)-1:
                        s += "{ name: " + input_element.name + "}, "
                    else:
                        s += "{ name: " + input_element.name + "}"
                s += "]"
            s += "}\n"
        print(s)

    # TODO saveSimulationResults csv, jpg/png
    # TODO "print"

    # TODO "export"


    @property
    def name(self):
        """str: The name of the system."""
        return self._name


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
    def system_elements(self):
        """list: A list that maintains all elements currently in the system."""
        return self._system_elements


    @name.setter
    def name(self, value):
        if len(value):
            self._name = value
        else:
            raise ValueError("name can not be empty")


    @simulation_steps.setter
    def simulation_steps(self, value):
        if value > 0:
            self._simulation_steps = value
        else:
            raise ValueError("simulation_steps must be positive.")


    @time_unit.setter
    def time_unit(self, value):
        if value.strip().lower() in System.VALID_TIME_UNITS:
            self._time_unit = value.strip().lower()
        else:
            raise ValueError("name can not be empty")


    def __str__(self):
        """Creates and returns a string representation of the system.

        :return: The result string
        :rtype: str
        """
        s = ""
        s += "{ name: " + self.name \
            + ", simulation_steps: " + str(self.simulation_steps) \
            + ", time_unit: " + self.time_unit + " }"
        return s
