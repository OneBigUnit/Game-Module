from .land import Land
from .site import Site

from ..AdventureGame.game import AdventureGame


class Area:
  """
  A wrapper containing the necessary information to represent a 2nd-class location (area)
  """
  def __init__(self, name: str, land: Land) -> None:
    self.name = name
    self.land = land
    self.sites = []
    self.game = None  # Added upon game creation
  
  def add_site(self, site: Site) -> None:
    """
    Adds a site object into this area object
    """
    self.sites.append(site)
  
  def get_site(self, name: str) -> Site:
    """
    Searches for and returns a site object within this area object from it's name
    """
    return list(filter(lambda site: site.name == name, self.sites))[0]

  def __str__(self) -> str:
    """
    String representation of this area object
    """
    return f"{self.name}"

  def add_game(self, game: AdventureGame) -> None:
    """
    Adds the game object into this area object and its sites
    """
    self.game = game
    for site in self.sites:
      site.add_game(self.game)
