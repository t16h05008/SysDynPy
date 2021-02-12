from sysdynpy.systemelement import SystemElement

class DynamicVariable(SystemElement):
    """An auxiliary system element to simplify calculation rules.

    Dynamic variables are very similar to flows, but they don't have
    to be connected to a stock. The value of dynamic variables can be calculated
    from stocks and parameters at any time. They don't need an initial value.
    """

    def __init__(self, name, system, var_name, calc_rule, input_elements=[]):
        """Constructor method.

        :param name: The element name. Can not be empty. Must be unique within the system.
        :type name: str
        :param system: The system that this element shall be part of.
        :type system: System
        :param var_name: The name of the variable this element will be assigned to,
            once it is constructed. This is needed because the variable name has to
            be known in other modules to execute the lambda expression that defines
            the calculation rule.
        :type var_name: str
        :param calc_rule: The rule used to calculate the value property.
            Input elements are referenced by their :py:attr:`~var_name` property.
            The calculation rule is stored as a lambda expression. This means that
            all valid python expression are valid as calculation rules.
        :type calc_rule: function
        :param input_elements: The system elements needed to calculate the
            value for this element (usually connected by arrows in a simulation
            diagram), defaults to an empty list
        :type input_elements: list, optional
        """
        super().__init__(name, system, var_name)
        self.calc_rule = calc_rule
        self.input_elements = input_elements or []


    @property
    def calc_rule(self):
        """see :py:meth:`~__init__`
        """
        return self._calc_rule


    @property
    def input_elements(self):
        """see :py:meth:`~__init__`
        """
        return self._input_elements


    @calc_rule.setter
    def calc_rule(self, value):
        self._calc_rule = value
    

    @input_elements.setter
    def input_elements(self, value):
        self._input_elements = value


    def __str__(self):
        s = ""
        s += "{ name: " + self.name
        if hasattr(self, "value"):
            s += ", value: " + str(self.value)
        s += ", system: " + str(self.system.name) \
            + ", var_name: " + str(self.var_name) \
            + " }"
        return s
