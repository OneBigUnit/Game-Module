from typing import Optional, List

from .race import Race

from ..AdventureGame.game import AdventureGame
from ..Actions.actions import Actions
from ..Locations.site import Site
from ..Objects.item import Item
from ..Objects.weapon import Weapon


class NPC:
  """
  The class containing all data about each non-playter character (NPC) in the game
  """
  def __init__(
    self, name: str, gender: str, race: Race, starting_site: Site, action_set: Actions, 
    can_move_automatically: bool=True, tolerance: int=50, 
    offense_modifier: int=0, defence_modifier: int=0, agility_modifier: int=0, starting_health: int=100, 
    max_item_generation: int=0, max_artefact_generation: int=0, max_weapon_generation: int=0, starting_currency: int=1000, 
    max_health: Optional[int]=None, base_inventory: Optional[List[Item]]=None, respawn_after_days: int=3, unarmed_weapon: Optional[Weapon]=None
  ) -> None:
    self.name = name
    self.gender = gender
    self.race = race
    
    self.tolerance = tolerance
    self.currency = starting_currency
    self.offense = self.__cap_value(race.offense + offense_modifier)
    self.defence = self.__cap_value(race.defence + defence_modifier)
    self.agility = self.__cap_value(race.agility + agility_modifier)
    self.health = starting_health
    if max_health is None:
      self.max_health = self.health
    else:
      self.max_health = max_health
    
    self.current_site = starting_site
    self.current_area = self.current_site.area
    self.current_planet = self.current_area.planet
    self.galaxy = self.current_planet.galaxy
    
    self.max_items = max_item_generation
    self.max_artefacts = max_artefact_generation
    self.max_weapons = max_weapon_generation
    if base_inventory is None:
      self.base_inventory = []
    else:
      for item in base_inventory:
        item.sellable = False
      self.base_inventory = base_inventory
    self.inventory = self.base_inventory
    self.__populate_inventory(self.max_artefacts, self.max_weapons)

    self.can_move_automatically = can_move_automatically
    self.interaction_options = action_set.get_actions()
    self.respawn_after_days = 3
    if unarmed_weapon is None:
      self.unarmed_weapon = Weapon()
    else:
      self.unarmed_weapon = unarmed_weapon
  
  @staticmethod
  def __cap_value(value: int, lower: int=0, upper: int=100) -> int:
    """
    A mangled helper method to limit the range of an integer value between given bounds
    """
    if lower is not None and upper is not None:
      if upper < lower:
        raise ValueError("Upper bound cannot be lower than lower bound") from None
    if lower is not None:
      if value < lower:
        return lower
    if upper is not None:
      if value > upper:
        return upper
    return value

  def __populate_inventory(self) -> None:
    """
    A mangled helper method to add random items to this NPCs inventory
    """
    # Setup item generation weights
    item_probability_weights = [(1 - item.rarity) for item in self.item_generator.all]
    artefact_probability_weights = [(1 - artefact.rarity) for artefact in self.artefact_generator.all]
    weapon_probability_weights = [(1 - weapon.rarity) for weapon in self.weapon_generator.all]

    added_inventory = [  # Generate items
      *self.item_generator.generate(self.max_items, item_probability_weights), 
      *self.artefact_generator.generate(self.max_artefacts, artefact_probability_weights), 
      *self.weapon_generator.generate(self.max_weapons, weapon_probability_weights)
    ]
    self.inventory = [*self.inventory, *added_inventory]  # Add to the existing inventory
  
  def respawn(self) -> None:
    """
    Respawn this NPC
    """
    self.health = self.max_health
    self.inventory = self.base_inventory
    self.__populate_inventory()
    self.current_site.add_npc(self)
  
  def kill(self, game: AdventureGame, respawn_later: bool=True) -> None:
    """
    Kills this NPC and registers the death to the game if enabled
    """
    if respawn_later:
      game.add_killed_npc(self)  # Register the death to the game
    self.health = 0
    self.current_site.remove_npc(self)
