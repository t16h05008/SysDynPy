from abc import ABC, abstractmethod
from sysdynpy.system import System
import sysdynpy.utils as utils

class SystemElement(utils.SubclassOnlyABC):
    """some class """

    def __init__(self, name, value, system):
        self.name = name
        self.value = value
        self.system = system

    @property
    def name(self):
        """ TODO """
        return self._name
    
    @property
    def value(self):
        """ TODO """
        return self._value
    
    @property
    def system(self):
        """ TODO """
        return self._system

    @name.setter
    def name(self, value):
        """ TODO
        string
        """
        if len(value):
            self._name = value
        else:
            raise ValueError("name can not be empty")
    
    @value.setter
    def value(self, value):
        """ TODO
        double
        """
        self._value = value

    @system.setter
    def system(self, value):
        """ TODO
        System
        """
        self._system = value
    

    def __del__(self):
        """Removes element from system elements list
        This method get executed when the object gets destroyed
        by the garbage collector. The object remains in the list
        until this happens, even after the reference has been deleted
        using the "del" keyword. 
        """
        existing_system_elements = self.system.system_elements
        if self in existing_system_elements:
            existing_system_elements.remove(self)
