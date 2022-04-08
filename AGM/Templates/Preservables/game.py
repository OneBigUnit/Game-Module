from typing import Optional

from AGM.Tools.Preservation.preservable import Preservable
from AGM.Tools.ConsoleControl.console import Console

from .user import User

from ..TriggerSystems.tutorial import Tutorial
from ..Characters.player import Player
from ..Characters.npc import NPC
from ..Locations.world import World


class AdventureGame(Preservable):
  """
  A preservable implementation of the game class
  """
  def __init__(self, name: str, path: str, user: User, player: Player, world: World, tutorial: Optional[Tutorial]=None) -> None:
    self.day = 1
    self.name = name
    self.world = world
    self.player = player
    self.tutorial = tutorial
    self.playing = True
    self.killed_npcs = []
    self.user = user
    self.world.game = self

    super().__init__(f"({self.user.username}) {self.name}", path)
  
  def __str__(self) -> str:
    """
    String representation of the game object, used in file creation
    """
    return f"Game Save - {self.save_name} (Day {self.day})"

  def run(self) -> None:
    """
    The game loop which runs and manages the game
    """
    Console.clear_now()
    while self.playing:
      self.player.adjust_available_actions()
      if self.tutorial is not None:
        if self.tutorial.is_triggered(self):
          self.tutorial.run_stage(self)

      self.player.do_action()
      self.user.update_achievements(self)
      
      self.save()
      self.user.save()

  def add_killed_npc(self, npc: NPC) -> None:
    """
    Adds an NPC to the dead-NPC respawn queue, to register NPC deaths and hence respawns
    """
    self.killed_npcs.append((npc, self.day))
  
  def next_day(self) -> None:
    """
    Advances the day in-game, and updates the game state accordingly
    """
    self.day += 1
    self.player.reset_todays_destinations()
    for npc_data in filter(lambda data: self.day - data[1] == data[0].respawn_after_days, self.killed_npcs):
      self.killed_npcs.remove(npc_data)
      npc_data[0].respawn()
