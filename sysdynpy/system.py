class System(object):
    """This class represents a System Dynamics system/model.

    :param name: The system name
    :type name: str, required

    """

    def __init__(self, name=""):
        """Constructor method
        """
        self.name = name
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


    @property
    def name(self):
        """str: The name of the system."""
        return self._name


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