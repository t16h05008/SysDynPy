from sysdynpy.systemelement import SystemElement
from sysdynpy.system import System
import sysdynpy.utils as utils

class Stock(SystemElement):
    """Represents the system dynamics element 'Stock'.

    Stocks are also known as levels.
    """


    def __init__(self, name, value, system, input_elements=[]):
        """Constructor method.

        :param name: The element name. Can not be empty. Must be unique within the system.
        :type name: str
        :param value: The numeric value that is used in calculations.
        :type value: int or float
        :param system: The system that this element shall be part of.
        :type system: System
        :param input_elements: The system elements needed to calculate the
            value for this element (usually connected by arrows in a simulation
            diagram), defaults to an empty list
        :type input_elements: list, optional
        """
        super().__init__(name, system)
        self.value = value
        self.input_elements = input_elements or []


    @property
    def calc_rule(self):
        """The rule to use to calculate the value attribute.

        Other system elements can be references by their name attribute.
        See :py:func:`~sysdynpy.utils._validate_calc_rule` for details about
        the syntax you can use.

        :type: string
        """
        return self._calc_rule


    @property
    def input_elements(self):
        """see :py:meth:`~__init__`
        """
        return self._input_elements


    @calc_rule.setter
    def calc_rule(self, value):
        try:
            utils._validate_calc_rule(value, self)
        except ValueError as v:
            raise v
        else:
            self._calc_rule = value


    @input_elements.setter
    def input_elements(self, value):
        self._input_elements = value


    def __str__(self):
        s = ""
        s += "{ name: " + self.name \
            + ", value: " + str(self.value) \
            + ", system: " + str(self.system) \
            + " }"
        return s


