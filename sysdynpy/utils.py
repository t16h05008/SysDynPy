from abc import ABC, ABCMeta, abstractmethod
import re

# utility functions and classes

class SubclassOnlyABC(object):
    """Helper class to prevent instantiation.
    The class SysDynPy is declared as abstract and should not be instantiated.
    However, because there are no abstract methods present, it could be
    instantiated.
    By deriving SysDynPy from this class we ensure that no instances can be
    created. This is done by overriding the __new__ method.
    For more info see: https://stackoverflow.com/questions/50099600/abstract-classes-without-abstract-methods-creating-objects-in-python
     """
    __metaclass__ = ABCMeta

    def __new__(cls, *args, **kwargs):
        if cls.__bases__ == (SubclassOnlyABC,):
            msg = 'Abstract class {} cannot be instantiated'.format(cls.__name__)
            raise TypeError(msg)
        return super(SubclassOnlyABC, cls).__new__(cls)


def _check_if_system_element_name_is_unique(name, system):
    for element in system.system_elements:
        if element.name == name:
            raise ValueError("A system element with this name already exists" \
            + "in system '" + system.name + "'")


def _validate_calc_rule(calc_rule, input_elements):
    """ TODO """

    calc_rule = calc_rule.strip()

    # iterate input elements
    for idx, val in enumerate(input_elements):
        # check if element is in calc_rule
        if re.search(r'\b' + val.name + r'\b', calc_rule):
            # replace element by index
            calc_rule = calc_rule.replace(val.name, str(idx))
        else:
            # element not in calc_rule
            raise ValueError("The calculation rule must use all input elements.")

    # remove spaces
    calc_rule = calc_rule.replace(" ", "")
    print(calc_rule)
    # only allow + - * / as additional characters
    if not re.match('^[0-9\+\-\*\/]*$', calc_rule):
        raise ValueError("Unsupported mathematical operation."\
            " Only + - * and / are allowed.")



#calc_rule_split = re.split('\+|\-|\*|\/', calc_rule)