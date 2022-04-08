from .world import World
from .area import Area

from ..AdventureGame.game import AdventureGame


class Land:
  """
  A wrapper containing the necessary information to represent a 3rd-class location (land)
  """
  def __init__(self, name: str, world: World) -> None:
    self.name = name
    self.world = world
    self.areas = []
    self.game = None  # Added upon game creation
  
  def add_area(self, area: Area) -> None:
    """
    Adds an area object into this land object
    """
    self.areas.append(area)
  
  def get_area(self, name: str) -> Area:
    """
    Searches for and returns a area object within this land object from it's name
    """
    return list(filter(lambda area: area.name == name, self.areas))[0]  # Retrives the first occurrance
  
  def __str__(self) -> str:
    """
    String representation of this land object
    """
    return f"{self.name}"

  def add_game(self, game: AdventureGame) -> None:
    """
    Adds the game object into this land object and its areas
    """
    self.game = game
    for area in self.areas:
      area.add_game(self.game)
