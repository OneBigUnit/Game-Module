from .item import Item


class Weapon(Item):
  """
  A wrapper for any items that are valid for use in combat
  """
  def __init__(self, name: str, cost: int, rarity: int, offense: int, defence: int, attack_range: int) -> None:
    super().__init__(name, cost, rarity)
    self.offense = offense
    self.defence = defence
    self.range = attack_range
