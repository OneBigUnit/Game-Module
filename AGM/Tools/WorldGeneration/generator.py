"""
A simple wrapper to contain all the necessary data for a world-generator entry
"""


from typing import Callable

import random


class Generator:
  """
  A wrapper containing all the necessary data for a valid world-generator entry
  """
  def __init__(self, method: Callable) -> None:
    self.all = method()

  def generate(self, n_max, weights=None):
    return random.choices(self.all, weights=weights, k=n_max)
