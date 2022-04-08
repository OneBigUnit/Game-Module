from typing import Any, Optional, Callable


class Trigger:
  """
  A wrapper containing all necessary data to define a trigger within a trigger system
  """
  def __init__(self, target_variable_path: str, target_value: Any, assessment_sequence: Optional[Callable]=None) -> None:
    self.target_variable_path = target_variable_path
    self.target_value = target_value
    self.assessment_sequence = assessment_sequence
