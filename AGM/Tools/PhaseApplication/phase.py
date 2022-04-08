from __future__ import annotations
from typing import Callable, Any, TYPE_CHECKING

if TYPE_CHECKING:
  from .application import PhaseApplication


class Phase:
  """
  A wrapper to add all data and functionality to a user-defined phase
  """
  def __init__(self, phase: Callable, *args, **kwargs) -> None:
    self.app = None
    self.phase = phase
    self.args = args
    self.kwargs = kwargs
    self.last_result = None
    self.results = []

  def run(self, app: PhaseApplication) -> Any:
    """
    A method to run this phase, taking the phase application as a parameter to pass it into the user-defined callable
    """
    if self.app.is_active:
      if not self.app.is_paused:
        self.last_result = self.phase(app, *self.args, **self.kwargs)
        self.results.append(self.last_result)
        try:
          self.app.skip()
        except IndexError:
          pass
        return self.last_result

  def get_result(self, result_idx: int) -> Any:
    """
    Gets a result at a specified index from the result storage of this phase object
    """
    try:
      return self.results[result_idx]
    except IndexError:
      return None
