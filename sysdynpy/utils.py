from abc import ABC, ABCMeta, abstractmethod
from asteval import Interpreter
import re
import numbers

aeval = Interpreter()

"""This module provides utility methods and classes for internal use
"""

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


def _validate_calc_rule(calc_rule, element):
    """Validates the syntax for a given calculation rule.

    There are two requirements:
        1. Each input element has to be used in the calculation rule
        2. Only basic arithmetic operations are allowed (for now).
    
    Because input elements can be named like "some-input+element" splitting
    the string at arithmetic operators is not possible. Instead this method
    replaces each input element by its index in the list.

    "some-element-name*some-other+name" --> "0*1" (or "1*0")

    Once the string is transformed like this it is possible to check if all
    characters are either numbers or one of the supported arithmetic operations.

    :param value: The calculation rule to validate
    :type value: str
    :param element: The system element to validate the calculation rule for.
    :type element: Subclass of SystemElement
    :raises ValueError: If the calculation does not use all input elements
    :raises ValueError: If an unsupported mathematical operation is given.
        Supported operations are + - * and /.
    :returns: nothing.
    :rtype: None
    """

    input_elements = element.input_elements

    calc_rule = calc_rule.strip()

    # iterate input elements
    for idx, val in enumerate(input_elements):
        # check if element is in calc_rule
        if re.search(r'\b' + val.name + r'\b', calc_rule):
            # replace element by index
            calc_rule = calc_rule.replace(val.name, str(idx))
        else:
            # element not in calc_rule
            raise ValueError("The calculation rule must use all input elements." +
                                " Element name: "+ element.name)

    # remove spaces
    calc_rule = calc_rule.replace(" ", "")
    # only allow + - * / as additional characters
    if not re.match('^[0-9\+\-\*\/]*$', calc_rule):
        raise ValueError("Unsupported mathematical operation."\
            " Only + - * and / are allowed.")


def _calculate_dynamic_value(element):
    """Calculates the values for a given element based on the calculation rule.

    This is a recursive function to calculate the value of a Flow or
    dynamic variable. The values of flows or dynamic variables can always be
    deduced from parameters or stocks. But it can not be assumed that a dynamic
    variable or flow **directly** depends on only parameters or stocks.

    :param element: The element to calculate a value for.
    :type element: Flow or DynamicVariable
    :raises TypeError: If the calculation rule does not evaluate to a numerical result
    :return: The calculated value
    :rtype: double
    """
    result = None
    calc_rule = element.calc_rule

    # for each input element
    for idx, inp_elem in enumerate(element.input_elements):
        # check its type
        if "Stock" in str(type(inp_elem)) or "Parameter" in str(type(inp_elem)):
            # if stock or parameter replace name in calculation rule
            calc_rule = \
                calc_rule.replace(inp_elem.name, str(inp_elem.value))
        else:
            # else call this function again and replace name with result
            # print("calling recursive function for input element " + inp_elem.name + " of element " + element.name)
            calc_rule = \
                calc_rule.replace(inp_elem.name, str(_calculate_dynamic_value(inp_elem)))

    # calculate value
    result = aeval(calc_rule)

    if not isinstance(result, numbers.Number):
        raise TypeError("The result of is not numeric. Is is: " + str(result))
    else:
        return result


def _calculate_stock_value(stock):
    """[summary]

    Unlike with _calculate_dynamic_value no recursion is needed here.

    :param stock: [description]
    :type stock: [type]
    """
    result = None
    calc_rule = stock.calc_rule

    # for each input element
    for idx, inp_elem in enumerate(stock.input_elements):
        # replace name in calculation rule
        calc_rule = calc_rule.replace(inp_elem.name, str(inp_elem.value))

    # calculate value
    result = aeval(calc_rule)

    if not isinstance(result, numbers.Number):
        raise TypeError("The result of is not numeric. Is is: " + str(result))
    else:
        return result

