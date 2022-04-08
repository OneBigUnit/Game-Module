"""
A simple wrapper to contain all the necessary data for an action-group action entry
"""


from typing import List, Callable, Any

from AGM.Tools.TriggerSystems.system import TriggerSystem
from AGM.Tools.TriggerSystems.trigger import Trigger


class Action(TriggerSystem):
  """
  A wrapper containing all the necessary data to form a valid action entry, with extended trigger system behaviours
  """
  def __init__(self, method: Callable, name: str, index: int, triggers: List[Trigger], base_variable_name: str="self") -> None:
    self.method = method
    self.name = name
    self.index = index

    super().__init__(triggers, base_variable_name=base_variable_name)

  def is_available(self, starting_context: Any) -> bool:
    """
    Checks whether the action should currently be available to its user given the user's conditions
    """
    return self.is_triggered(starting_context)
