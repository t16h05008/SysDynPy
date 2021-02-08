from sysdynpy.systemelement import SystemElement
from sysdynpy.system import System
import sysdynpy.utils as utils

class Flow(SystemElement):
    """TODO"""

    def __init__(self, name, system):
        """ TODO """
        super().__init__(name, None, system)
        self.input_elements = []


    @property
    def calc_rule(self):
        """ TODO """
        return self._calc_rule

    @property
    def input_elements(self):
        """ TODO """
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
            + ", calc_rule: " + self.calc_rule \
            + " }"
        return s
