from typing import Callable, List

import inspect

from AGM.Tools.TriggerSystems.trigger import Trigger

from .action import Action as ActionContainer


class Actions:
  def ActionGroup() -> Callable:
    """
    A class decorator to add all functionality and behaviours to the user-defined 'child' action group class
    """
    def _ActionGroup(UnmodifiedClass):
      ModifiedClass = type(UnmodifiedClass.__name__, (  # Convert the unmodified class into a new dynamically generated class that inherits from this class
        Actions, 
      ), dict(UnmodifiedClass.__dict__))
      return ModifiedClass
    return _ActionGroup

  def Action(index: int, name: str, triggers: List[Trigger], base_variable_name: str="self") -> Callable:
    """
    A decorator for converting a user-defined function into a valid menu option
    """
    def _Action(method):
      return ActionContainer(method, name, index, triggers, base_variable_name=base_variable_name)  # Return a built action wrapper
    return _Action

  def get_actions(self) -> List[ActionContainer]:
    """
    A mangled helper method to gather the user-defined options from the 'child' class
    """
    options = {name: option for name, option in inspect.getmembers(self.__class__, predicate=lambda member: isinstance(member, ActionContainer))}  # Get actions as invalid dictionary
    return {option.name: option.method for option in sorted(list(options.values()), key=lambda option: option.index)}  # Order them into a valid dictionary and then return
