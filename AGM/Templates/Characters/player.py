from typing import Optional

from AGM.Tools.IOUtilities.input import Input

from ..AdventureGame.game import AdventureGame
from ..Locations.world import World
from ..Locations.land import Land
from ..Actions.actions import Actions
from ..Objects.weapon import Weapon


class Player:
  """
  The class containing all data about the player (PC) in the game
  """
  def __init__(self, game: AdventureGame, name: str, world: World, action_set: Actions, starting_land: Optional[Land]=None, unarmed_weapon: Optional[Weapon]=None) -> None:
    self.game = game
    self.name = name
    
    self.current_land = starting_land
    self.current_area = None
    self.current_site = None
    self.world = world
    
    self.possible_actions
    self.possible_actions = action_set
    self.available_actions = {}
    
    self.current_npc = None
    self.inventory = []
    self.currency = 0
    self.health = 120
    self.max_health = 120
    self.offense = 50
    self.defence = 50
    self.agility = 50
    if unarmed_weapon is None:
      self.unarmed_weapon = Weapon()
    else:
      self.unarmed_weapon = unarmed_weapon
    
    self.adjust_available_actions()
  
  def do_action(self) -> None:
    """
    Carry out an inputted action
    """
    Input.get_inputted_item_from_iterable("Enter the number corresponding to the action you wish to choose.", self.available_actions)(self)
  
  def respawn(self) -> None:
    """
    Respawns the player
    """
    self.health = self.max_health
  
  def adjust_available_actions(self) -> None:
    """
    Updates the available actions the player can take given their situation
    """
    if self.current_site is not None:
      self.available_actions = {action.name: action.method for action in list(self.possible_actions.get_actions().values())}
