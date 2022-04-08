"""
A collection of custom errors for the UI Menus Tool Kit
"""


class InvalidMenuOperation(Exception):
  """
  An exception raised when an invalid operation is called on the menu object
  """
  def __init__(self, msg: str="Invalid Menu Operation") -> None:
    self.message = msg
    super().__init__(self.message)
