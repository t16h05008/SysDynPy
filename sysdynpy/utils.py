from abc import ABC, ABCMeta, abstractmethod
import re

"""This module provides utility methods and classes for internal use.
"""

class SubclassOnlyABC(object):
    """Helper class to prevent instantiation.
    Some classes are declared as abstract and should not be instantiated.
    However, if there are no abstract methods present, they could be
    instantiated.
    
    By deriving these classes from this class we ensure that no instances can be
    created. This is done by overriding the __new__ method.
     """
    __metaclass__ = ABCMeta

    def __new__(cls, *args, **kwargs):
        if cls.__bases__ == (SubclassOnlyABC,):
            msg = 'Abstract class {} cannot be instantiated'.format(cls.__name__)
            raise TypeError(msg)
        return super(SubclassOnlyABC, cls).__new__(cls)


