"""
A collection of custom errors for the Phase Application Tool Kit
"""


class PhaseError(ValueError):
  """
  An exception raised when a phase is flagged as invalid
  """
  def __init__(self, msg: str="Phase Invalid") -> None:
    self.message = msg
    super().__init__(self.message)


class PhaseTransitionError(IndexError):
  """
  An exception raised when movement between phases fails or is disallowed
  """
  def __init__(self, msg: str="Phase Transition Failed") -> None:
    self.message = msg
    super().__init__(self.message)
