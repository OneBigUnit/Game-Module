"""
A tool that allows for single-line custom error generation
"""


from typing import Optional


class Error:
  """
  A class to dynamically generate a custom error type
  """
  def __init__(self, name, default_message: str="An error occured") -> None:
    self.name = f"{name}"
    self.default_msg = default_message
    self.exception = type(self.name, (Exception, ), {"__init__": self.__patch_init})  # Dynamically generate an exception from the given data and store as an attribute

  def throw(self, msg: Optional[str]=None) -> None:
    """
    Raises the custom error with message support
    """
    if msg is None:
      msg = self.default_msg
    raise self.exception(msg)

  def __patch_init(self, msg: Optional[str]=None) -> None:
    """
    A mangled method used as the __init__ method of the dynamically generated exception atrtribute of each error object
    """
    if msg is None:
      msg = self.default_msg
    self.message = msg

  def __str__(self) -> str:
    return f"{self.name} Exception"
