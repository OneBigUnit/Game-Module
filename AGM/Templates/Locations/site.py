from typing import List

from .area import Area

from ..Actions.actions import Actions
from ..Characters.npc import NPC
from ..Objects.item import Item
from ..AdventureGame.game import AdventureGame


class Site:
  """
  A wrapper containing the necessary information to represent a 1st-class location (site)
  """
  def __init__(self, name: str, area: Area, actions_available: Actions, descriptions: List[str]) -> None:
    self.name = name
    self.area = area
    self.actions_available = actions_available
    self.npcs = []
    self.items = []
    self.mission_clues = []
    self.descriptions = descriptions
    self.game = None  # Added upon game creation

  def add_npc(self, npc: NPC) -> None:
    """
    Adds an NPC to this site object
    """
    self.npcs.append(npc)

  def add_item(self, item: Item) -> None:
    """
    Adds an item to this site object
    """
    self.items.append(item)

  def __str__(self):
    """
    String representation of this site object
    """
    return f"{self.name}"
  
  def remove_npc(self, npc: NPC) -> None:
    """
    Removes an NPC from this site object
    """
    self.npcs.remove(npc)

  def get_npc(self, npc_name: str) -> NPC:
    """
    Searches for and returns and NPC object from this site object from its name
    """
    try:
      npc_index = [npc.name for npc in self.npcs].index(npc_name)
    except ValueError:
      raise IndexError(f"The requested NPC ({npc_name}) does not exist at this site ({self.name})")
    return self.npcs[npc_index]

  def add_game(self, game: AdventureGame) -> None:
    """
    Adds the game object into this site object
    """
    self.game = game
