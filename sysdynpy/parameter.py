from sysdynpy.systemelement import SystemElement
from sysdynpy.system import System
import sysdynpy.utils as utils

class Parameter(SystemElement):
    """TODO"""

    def __init__(self, name, value, system):
        """ TODO """
        super().__init__(name, value, system)


    def __str__(self):
        s = ""
        s += "{ name: " + self.name \
            + ", value: " + str(self.value) \
            + ", system: " + str(self.system) \
            + " }"
        return s