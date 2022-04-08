"""
A collection of custom errors for the Preservation Tool Kit
"""


class VerificationError(AssertionError):
  """
  An exception raised when verification is failed
  """
  def __init__(self, msg: str="Verification Failed") -> None:
    self.message = msg
    super().__init__(self.message)


class AccessError(RuntimeError):
  """
  An exception raised when data access fails or is disallowed
  """
  def __init__(self, msg: str="Data Access Failed") -> None:
    self.message = msg
    super().__init__(self.message)


class SaveError(RuntimeError):
  """
  An exception raised when data saving or writing fails or is disallowed
  """
  def __init__(self, msg: str="Data Save Failed") -> None:
    self.message = msg
    super().__init__(self.message)
