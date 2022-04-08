from typing import List

from AGM.Tools.Preservation.preservable import Preservable

from .game import AdventureGame

from ..TriggerSystems.achievements import Achievement


class User(Preservable):
  """
  A preservable implementation of the user and accounts, allowing for achievement tracking
  """
  def __init__(self, username: str, password: str, save_file: str, achievements: List[Achievement]) -> None:
    self.username = username
    self.games = []
    self.achievements = achievements
    
    super().__init__(self.username, save_file, save_password=password)

  def update_achievements(self, game: AdventureGame) -> None:
    """
    Update the user's achievements status
    """
    for achievement in self.achievements:
      if achievement.is_triggered(game) and not achievement.is_completed:
        achievement.achieve()
        achievement.notify()
