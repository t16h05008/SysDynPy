from sysdynpy.systemelement import SystemElement
from sysdynpy.system import System
import sysdynpy.utils as utils

class Parameter(SystemElement):
    """Stores fixed values.

    Parameters don't have input elements. That means, the value of a parameter,
    once set, will not change during the simulation.
    """

    @utils.extend_docstring(SystemElement.__init__) # prepend docstring from superclass
    def __init__(self, name, value, system):
        """
        :param value: The numeric value that is used in calculations.
        :type value: int or float
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