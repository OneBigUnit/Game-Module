from .item import Item


class Artefact(Item):
  """
  A wrapper for a generally rare game object that has sentimental significance to the world
  """
  def __init__(self, name: str, cost: int, rarity: int) -> None:
    super().__init__(name, cost, rarity)
