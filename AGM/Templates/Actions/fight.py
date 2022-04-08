from typing import Union, Optional

import random

from AGM.Tools.IOUtilities.input import Input
from AGM.Tools.ConsoleControl.console import Console

from ..Objects.weapon import Weapon
from ..Characters.player import Player
from ..Characters.npc import NPC


class Fight:
  """
  An non-linear implementation for fighting mechanics taking into account all applicable combatant statistics
  """
  def __init__(self, player: Player, npc: NPC) -> None:
    self.player = player
    self.npc = npc
    self.participants = (
      self.player, 
      self.npc
    )
    self.is_active = True
  
  def run_round(self) -> Union[Player, NPC]:
    """
    Runs and manages a single round of combat, including all performance and damage calculations, and display
    """
    if not len([item for item in self.player.inventory if isinstance(item, Weapon)]):  # If player has no weapon items
      player_inventory = [self.player.unarmed_weapon]
    else:
      player_inventory = [item for item in self.player.inventory if isinstance(item, Weapon)]
    if not len([item for item in self.npc.inventory if isinstance(item, Weapon)]):  # If NPC has no weapon items
      npc_inventory = [self.npc.unarmed_weapon]
    else:
      npc_inventory = [item for item in self.npc.inventory if isinstance(item, Weapon)]

    # Selecting weapons from all available
    player_weapon = Input.get_inputted_item_from_iterable("Enter the number corresponding to the action you wish to take.", 
    player_inventory, formatted_override_iterable=[f"Use your {item.name}" for item in player_inventory])
    npc_weapon = random.choices(npc_inventory, weights=[item.offense + item.defence for item in npc_inventory], k=1)[0]

    # Calculate combatant performances (luck and statistic factors)
    player_performance = (((self.player.offense + 100) / 200) * ((player_weapon.offense + 100) / 200) + 
    ((self.player.defence + 100) / 200) * ((player_weapon.defence + 100) / 200) + 
    ((self.player.agility + 100) / 200) * ((player_weapon.range + 100) / 400) + random.uniform(0, 1.5)) * 25
    npc_performance = (((self.npc.offense + 100) / 200) * ((npc_weapon.offense + 100) / 200) + 
    ((self.npc.defence + 100) / 200) * ((npc_weapon.defence + 100) / 200) + 
    ((self.npc.agility + 100) / 200) * ((npc_weapon.range + 100) / 400) + random.uniform(0, 1.5)) * 25

    print(f"\nYou used: {player_weapon.name}\n{self.npc.name} used: {npc_weapon.name}")  # Display weapon information

    # Display performance information
    if player_performance > npc_performance:
      print(f"\nYou performed better than {self.npc.name} this round!")
    elif player_performance < npc_performance:
      print(f"\n{self.npc.name} performed better than you this round!")

    # Calculate damages
    npc_damage_taken = int(round(self.__cap_value((self.player.offense + player_weapon.offense) * random.uniform(0.8, 1.2) * 0.5 - (self.npc.defence + npc_weapon.defence) * random.uniform(0.8, 1.2) * 0.5)))
    player_damage_taken = int(round(self.__cap_value((self.npc.offense + npc_weapon.offense) * random.uniform(0.8, 1.2) * 0.5 - (self.player.defence + player_weapon.defence) * random.uniform(0.8, 1.2) * 0.5)))

    # Deal out and display damage and performance values
    if player_performance > npc_performance:
      player_damage_taken /= 2
      if self.__do_damage(self.npc, npc_damage_taken):
        return self.player
      if self.__do_damage(self.player, player_damage_taken):
        return self.npc
      self.show_status(player_damage_taken, npc_damage_taken)
    elif player_performance < npc_performance:
      npc_damage_taken /= 2
      if self.__do_damage(self.player, player_damage_taken):
        return self.npc
      if self.__do_damage(self.npc, npc_damage_taken):
        return self.player
      self.show_status(player_damage_taken, npc_damage_taken)
    else:
      self.show_status(player_damage_taken, npc_damage_taken, override_message=f"\nYou and {self.npc.name} were evenly matched for that round, and so neither you nor {self.npc.name} got damaged!\n\nPress enter to continue...\t")

  def run(self) -> Union[Player, NPC]:
    """
    Manage and run the rounds of combat
    """
    while self.is_active:
      results = self.run_round()
      if results:
        break
    return results
  
  def show_status(self, player_damage_taken: int, npc_damage_taken: int, override_message: Optional[str]=None) -> None:
    """
    Neatly display the current status of the fight
    """
    if override_message:
      Console.get_input(override_message)
    else:
      Console.get_input(f"\nYou dealt {npc_damage_taken} damage, but lost {player_damage_taken} health that round!\nYou now have {self.player.health} health left!\n\nPress enter to continue...\t")
  
  @staticmethod
  def __do_damage(target: Union[Player, NPC], damage: int) -> bool:
    """
    Deal damage to the target and return whether the target is dead of not
    """
    target.health -= damage
    if target.health <= 0:
      return True
    return False
  
  @staticmethod
  def __cap_value(value: int, lower: Optional[int]=0, upper: Optional[int]=None) -> int:
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
