"""
A simple wrapper to contain all the necessary data for a menu option entry
"""


from typing import Callable


class MenuOption:
  """
  A wrapper containing all the necessary data for a valid menu option
  """
  def __init__(self, method: Callable, name: str, index: int) -> None:
    self.method = method
    self.name = name
    self.index = index
