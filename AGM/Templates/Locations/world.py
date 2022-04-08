from .land import Land

from ..AdventureGame.game import AdventureGame


class World:
  """
  A wrapper containing the necessary information to represent a 4th-class location (world)
  """
  def __init__(self, name: str) -> None:
    self.name = name
    self.lands = []
    self.game = None  # Added upon game creation
  
  def get_land(self, name: str) -> Land:
    """
    Searches for and returns a land object within this world object from it's name
    """
    return list(filter(lambda land: land.name == name, self.lands))[0]
  
  def __str__(self) -> str:
    """
    String representation of this land object
    """
    return self.name
  
  def __repr__(self) -> str:
    """
    General representation of this land object
    """
    return f"{self.name} {{{list(self.lands.values())}}}"
  
  def add_land(self, land: Land) -> None:
    """
    Adds a land object into this world object
    """
    self.lands.append(land)

  def add_game(self, game: AdventureGame) -> None:
    """
    Adds the game object into this world object
    """
    self.game = game
    for land in self.lands:
      land.add_game(self.game)
