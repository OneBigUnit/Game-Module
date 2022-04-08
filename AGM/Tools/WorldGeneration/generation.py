from typing import Callable, List

import inspect

from .generator import Generator as WorldGenerator


class Generation:
  def GeneratorGroup() -> Callable:
    """
    A class decorator to add all functionality and behaviours to the user-defined 'child' generator-group class
    """
    def _GeneratorGroup(UnmodifiedClass):
      ModifiedClass = type(UnmodifiedClass.__name__, (  # Convert the unmodified class into a new dynamically generated class that inherits from this class
        Generation, 
      ), dict(UnmodifiedClass.__dict__))
      return ModifiedClass
    return _GeneratorGroup

  def Generator() -> Callable:
    """
    A decorator for converting a user-defined function into a valid menu option
    """
    def _Generator(method):
      return WorldGenerator(method)  # Return a built action wrapper
    return _Generator

  def get_actions(self) -> List[WorldGenerator]:
    """
    A mangled helper method to gather the user-defined options from the 'child' class
    """
    options = {name: option for name, option in inspect.getmembers(self.__class__, predicate=lambda member: isinstance(member, WorldGenerator))}  # Get actions as a dictionary
    return list(options.values())  # Order them into a valid list and then return
