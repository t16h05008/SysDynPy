from abc import ABC, abstractmethod
from sysdynpy.system import System
import sysdynpy.utils as utils

class SystemElement(utils.SubclassOnlyABC):
    """An **abstract** class for generic system elements. Concrete system elements
    like stacks or flows are derived from this class.
    """

    def __init__(self, name, system):
        # \u00A0 is a non-printable character. It does not appear in the docs,
        # but can be used to exclude the paragraph in between from subclass
        # docstrings. This is done in the class 'extend_docstring' in the utils
        # module.
        """Constructor method.
        \u00A0
        As this is an abstract class this constructor **can not be called** directly.
        But it provides a way to bundle code that needs to run when a subclass
        instance is created.
        \u00A0

        :param name: The element name. Can not be empty. Must be unique within the system.
        :type name: str
        :param system: The system that this element shall be part of.
        :type system: System
        """
        self.name = name
        self.system = system

        utils._check_if_system_element_name_is_unique(self.name, self.system)
        # add to list of elements in system class
        system._system_elements.append(self)


    @property
    def name(self):
        """see :py:meth:`~__init__`
        """
        return self._name
    

    @property
    def value(self):
        """The numeric value that is used in calculations.

        :type: int or float
        """
        return self._value
    

    @property
    def system(self):
        """see :py:meth:`~__init__`
        """
        return self._system


    @name.setter
    def name(self, value):
        if len(value):
            self._name = value
        else:
            raise ValueError("name can not be empty")
    

    @value.setter
    def value(self, value):
        self._value = value


    @system.setter
    def system(self, value):
        self._system = value


    def __str__(self):
        s = ""
        s += "{ name: " + self.name \
            + " }"
        return s