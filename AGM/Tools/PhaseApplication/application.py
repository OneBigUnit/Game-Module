from typing import Dict, Callable, Any

from .phase import Phase
from .errors import PhaseError, PhaseTransitionError

from ..DesignPatterns.singleton import Singleton


class PhaseApplication:
  """
  Provides an interface through which layer-styled application can be created
  """
  def __init__(self) -> None:
    self.phases = self.__class__.get_phases()
    for phase in self.phases:
      self.phases.get(phase).app = self
    self.current_phase_index = 0
    self.is_paused = False
    self.is_active = True
    self.last_result = None

  @classmethod
  def get_phases(cls) -> Dict[str, Callable]:
    """
    A helper method to get all the user-defined phases from the 'child' class
    """
    return {name: phase for name, phase in cls.__dict__.items() if (
      not name.startswith("__")
    )}

  def run(self) -> None:
    """
    Runs the currently active phase in the application
    """
    if not self.is_valid_index(self.current_phase_index):
      raise PhaseError(f"Phase application phase index was invalid: {self.current_phase_index!r}") from None
    self.last_result = self.run_active_phase()

  def run_active_phase(self) -> Any:
    """
    A helper method to run the currently active phase in the application
    """
    return self.get_phase(self.current_phase_index).run(self)

  def start(self) -> None:
    """
    Resets and runs the application from the beginning
    """
    self.is_active = True
    self.reset()
    self.run()

  def pause(self) -> None:
    """
    Pauses the default consecutive phase execution
    """
    self.is_paused = True

  def resume(self) -> None:
    """
    Resumes the default consecutive phase execution
    """
    self.is_paused = False

  def reset(self) -> None:
    """
    A helper method to reset the application back to it's original state
    """
    self.current_phase_index = 0
    self.is_paused = False

  def skip(self, n: int=1) -> None:
    """
    Skips the specified number of phases, and rewinds on a negative argument
    """
    if not isinstance(n, int):
      raise PhaseTransitionError(f"Cannot skip by a non-integer: {n!r}")
    if n < 0:
      return self.rewind(abs(n))
    if not self.is_valid_index(self.current_phase_index + n):
      raise PhaseTransitionError(f"Cannot skip enough: Attempted to skip {n} Phases") from None
    self.current_phase_index += n
    self.run_active_phase()

  def rewind(self, n: int=1) -> None:
    """
    Rewinds the specified number of phases, and skips on a negative argument
    """
    if not isinstance(n, int):
      raise PhaseTransitionError(f"Cannot rewind by a non-integer: {n!r}")
    if n < 0:
      return self.skip(abs(n))
    if not self.is_valid_index(self.current_phase_index - n):
      raise PhaseTransitionError(f"Cannot rewind enough: Attempted to rewind {n} Phases") from None
    self.current_phase_index -= n
    self.run_active_phase()

  def go_to(self, phase_index: int) -> None:
    """
    Directly changes the current phase to the specified index
    """
    if not isinstance(phase_index, int):
      raise PhaseTransitionError(f"Cannot go to phase using a non-integer: {phase_index!r}")
    if not self.is_valid_index(phase_index):
      raise PhaseTransitionError(f"Cannot go to phase with index: {phase_index!r}")
    self.current_phase_index = phase_index
    self.run_active_phase()

  def exit(self) -> None:
    """
    Deactivates the application
    """
    self.is_active = False

  def is_valid_index(self, index: int) -> bool:
    """
    A helper method to check the validity of an inputted index
    """
    return index >= 0 and index <= len(self.phases)

  def get_phase(self, index: int) -> Phase:
    """
    Fetches a specified phase from its index
    """
    try:
      if index < 0:
        raise PhaseError("A phase cannot have a negative index")
      return list(self.phases.values())[index]
    except IndexError:
      raise PhaseError(f"Phase at index '{index}' does not exist") from None
    except TypeError:
      raise PhaseError(f"Phase index {index!r} was invalid") from None

  def phase(phase: Callable) -> Phase:
    """
    A simple decorator to convert a user-defined callable into a valid phase object
    """
    return Phase(phase)

  def Application(*args, **kwargs) -> Callable:
    """
    A class decorator to add all functionality and behaviours to the user-defined 'child' application class
    """
    
    def _ApplicationClass(UnmodifiedClass):
      ModifiedClass = Singleton(UnmodifiedClass.__name__, (  # Convert the unmodified class into a singleton that inherits from this class
        PhaseApplication, 
      ), dict(UnmodifiedClass.__dict__))
      return ModifiedClass
    return _ApplicationClass

  def restart(self) -> None:  # Alias
    """
    An alias for the self.start() method, which restarts the execution of the application
    """
    self.start()
