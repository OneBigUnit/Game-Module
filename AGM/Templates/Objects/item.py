class Item:
  """
  A wrapper and base-class for all items and objects in the world
  """
  def __init__(self, name: str, cost: int, rarity: int, is_raw_currency: bool=False) -> None:
    self.name = name
    self.cost = cost
    self.rarity = rarity
    self.is_raw_currency = is_raw_currency
    self.sellable = True
