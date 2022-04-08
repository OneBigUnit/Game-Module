from typing import List


from AGM.Tools.TriggerSystems.system import TriggerSystem
from AGM.Tools.TriggerSystems.trigger import Trigger
from AGM.Tools.ConsoleControl.console import Console
from AGM.Tools.ConsoleControl.text import Text



class Achievement(TriggerSystem):
  """
  A trigger system implementation through which achievements can be created
  """
  def __init__(self, name: str, description: str, triggers: List[Trigger], base_variable_name: str="game") -> None:
    self.is_completed = False
    self.name = name
    self.description = description

    super().__init__(triggers, base_variable_name=base_variable_name)
  
  def achieve(self) -> None:
    """
    A method to set the status of the achievement to completed
    """
    self.is_completed = True
    self.is_active = False
  
  def notify(self) -> None:
    """
    Notifies the user that they have completed this achievement
    """
    Console.get_input(f"\n{Text.green('[ACHIEVEMENT]')} You got an achievement: '{Text.yellow(self.name)}'!\n\nPress enter to continue...\t", cover_character="")
  
  def __str__(self) -> str:
    """
    String representation of the achievement displaying it's status, and other information
    """
    status = "Completed" if self.is_completed else "Incomplete"
    string = f"Name: {self.name}\nDescription: {self.description}\nStatus: {status}"
    if self.is_completed:
      return Text.green(string)
    return Text.red(string)
