"""
A metaclass implementation of the singleton design pattern
"""


from typing import Any


class Singleton(type):  # Metaclass
  """
  A metaclass to convert every phase application object into a singleton
  """
  _instances = {}
  def __call__(cls, *args, **kwargs) -> Any:
    """
    An extended implementation of the __call__ inbuilt method, to detect when to return an old or new class upon attempted creation of a singleton
    """
    if cls not in cls._instances:  # If identical class hasn't already been created, return the class as normal
      cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
    return cls._instances.get(cls)  # Otherwise return the identical class
