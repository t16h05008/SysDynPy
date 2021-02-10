from sysdynpy.systemelement import SystemElement
from sysdynpy.system import System
import sysdynpy.utils as utils

class Parameter(SystemElement):
    """Stores fixed values.

    Parameters don't have input elements. That means, the value of a parameter,
    once set, will not change during the simulation.
    """

    def __init__(self, name, value, system):
        """Constructor method.

        :param name: The element name. Can not be empty. Must be unique within the system.
        :type name: str
        :param value: The numeric value that is used in calculations.
        :type value: int or float
        :param system: The system that this element shall be part of.
        :type system: System
        """
        super().__init__(name, system)
        self.value = value


    def __str__(self):
        s = ""
        s += "{ name: " + self.name \
            + ", value: " + str(self.value) \
            + ", system: " + str(self.system) \
            + " }"
        return s