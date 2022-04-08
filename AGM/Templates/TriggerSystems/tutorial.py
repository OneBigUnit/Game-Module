from typing import Dict, Callable, Any


from AGM.Tools.TriggerSystems.system import TriggerSystem
from AGM.Tools.TriggerSystems.trigger import Trigger


class Tutorial(TriggerSystem):
  """
  A trigger system implementation through which a tutorial can be created
  """
  def __init__(self, ordered_tutorial_stages: Dict[int, Callable], base_variable_name: str="game") -> None:
    self.current_stage_idx = 1
    self.ordered_stages = ordered_tutorial_stages
    starting_triggers = [Trigger(f"{base_variable_name}.tutorial.current_stage_idx", 1)]

    super().__init__(starting_triggers, base_variable_name=base_variable_name)
  
  def update_trigger(self, *triggers: Trigger) -> None:
    """
    Updates the tutorial to look for the next trigger and stage
    """
    self.current_stage_idx += 1
    if self.current_stage_idx > len(self.ordered_stages):
      self.end()
  
  def run_stage(self, game: Any) -> None:
    """
    Runs the currently selected stage, passing in the game to the tutorial callable
    """
    self.ordered_stages.get(self.current_stage_idx)(self, game)

  def end(self) -> None:
    """
    Ends the tutorial by decactivating it
    """
    self.is_active = False

  def restart(self, activate: bool=True) -> None:
    """
    Restarts the tutorial from the beginning
    """
    self.current_stage_idx = 1
    self.active_trigger_mechanism = [Trigger(f"{self.base_variable_name}.tutorial.current_stage_idx", 1)]
    self.is_active = activate
