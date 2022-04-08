"""
A collection of custom errors for the I/O Utilities Tool Kit
"""


class InvalidChoiceError(RuntimeError):
  """
  An exception raised when an invalid input choice is made
  """
  def __init__(self, msg: str="Invalid Choice Input") -> None:
    self.message = msg
    super().__init__(self.message)
