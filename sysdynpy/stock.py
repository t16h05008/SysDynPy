from sysdynpy.systemelement import SystemElement
from sysdynpy.system import System
import sysdynpy.utils as utils

class Stock(SystemElement):
    """TODO"""

    def __init__(self, name, value, system):
        """ TODO """
        super().__init__(name, value, system)
        self._input_elements = []

        utils._check_if_system_element_name_is_unique(self.name, self.system)

        # add to list of elements in system class
        system.system_elements.append(self)


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


