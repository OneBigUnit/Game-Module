class Race:
  """
  A wrapper for all character races in the world
  """
  def __init__(self, name: str, offense: int, defence: int, agility: int) -> None:
    self.name = name
    self.offense = offense
    self.defence = defence
    self.agility = agility
