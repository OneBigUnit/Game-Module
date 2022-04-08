from typing import List, Any


from .trigger import Trigger


class TriggerSystem:
  """
  A parent class that allows for conditional trigger systems to be made
  """
  def __init__(self, starting_triggers: List[Trigger], base_variable_name: str="self") -> None:
    self.triggers = starting_triggers
    self.base_variable_name = base_variable_name
    self.is_active = True

  def __fetch_and_assess_buried_variable(self, starting_context: Any, trigger_idx: int) -> bool:
    """
    A mangled helper method to iteratively retrieve the value of a variable given it's string path and a starting context, and evaluate it against given conditions
    """
    if self.triggers[trigger_idx].target_variable_path[0] == self.base_variable_name:
      self.triggers[trigger_idx].target_variable_path = self.triggers[trigger_idx].target_variable_path[1:]  # Trim the string path as appropriate

    context = starting_context
    for variable_name in self.triggers[trigger_idx].target_variable_path:  # Iterate through the string path to find the value
      context = getattr(context, variable_name)
    raw_variable_value = context

    if self.triggers[trigger_idx].assessment_sequence is None:  # If no special assessment sequence is found
      return raw_variable_value == self.triggers[trigger_idx].target_value  # Use __eq__ as a default assessment
    else:
      try:
        return self.triggers[trigger_idx].assessment_sequence(raw_variable_value, self.triggers[trigger_idx].target_value)  # Otherwise, use the supplied assessment sequence
      except Exception:
        raise RuntimeError(f"The supplied assessment sequence was invalid for the path: {'.'.join(self.triggers[trigger_idx].target_variable_path)}")

  def is_triggered(self, starting_context: Any) -> bool:
    """
    Checks to see if all rerquirements are met at this time to trigger the system
    """
    if not self.is_active:
      return False
    starting_contexts = [starting_context for trigger in range(len(self.triggers))]  # Starting context should be the same for all assessments
    return all([self.__fetch_and_assess_buried_variable(starting_context, trigger_idx) for trigger_idx, starting_context in enumerate(starting_contexts)])  # Check whether all triggers are activated
