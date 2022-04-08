"""
A collection of tools that allows for simple but powerful UI menu integration
"""


from typing import List, Any, Callable

import functools
import inspect

from .option import MenuOption
from .errors import InvalidMenuOperation

from ..DesignPatterns.singleton import Singleton
from ..ConsoleControl.console import Console


class Menu:
  """
  Provides an interface through which UI menus can be created
  """
  def __init__(self) -> None:
    self.menu_title = self.__class__.menu_title
    self.menu_prompt = self.__class__.menu_prompt
    self.options_list = self.__get_options_list()

  def __get_options_list(self) -> List[MenuOption]:
    """
    A mangled helper method to gather the user-defined options from the 'child' class
    """
    options = {name: option for name, option in inspect.getmembers(self.__class__, predicate=lambda member: isinstance(member, MenuOption))}  # Get options as a dictionary
    return list(sorted(list(options.values()), key=lambda option: option.index))  # Order them into a list and then return

  def show(self, buffer: bool=True) -> None:
    """
    Shows the menu UI in the console
    """
    Console.clear_now() if not buffer else None  # Clear the terminal if no buffer is wanted
    formatting_buffer = "\n" if buffer else ""
    print(f"{formatting_buffer}{self.menu_title}\n")

    for idx, option in enumerate(self.options_list):
      print(f"{idx + 1}) {option.name.title()}")

  def prompt(self) -> Any:
    """
    Prompt input from ther user chosing their desired menu option, and run and return that menu option
    """
    try:
      option_index = int(input(self.menu_prompt)) - 1
    except ValueError:
      raise TypeError("That input is not an integer") from None

    if option_index < 0:
        raise InvalidMenuOperation("That integer does not correspond to a menu option") from None

    try:
      option = self.options_list[option_index]
    except IndexError:
      raise InvalidMenuOperation("That integer does not correspond to a menu option") from None

    return option.method(self)  # Run and return the chosen option

  def run(self, buffer: bool=True) -> Any:
    """
    A compact method to first show the menu UI, and then prompt input and run the chosen option
    """
    self.show(buffer=buffer)  # Show UI
    return self.prompt()  # Input and run and return option chosen

  def loop(method: Callable) -> Callable:
    """
    A decorator for the user to declare whether the menu should be re-run after that option is run
    """
    @functools.wraps(method)
    def _loop(self, *method_args, **method_kwargs):
      method(self, *method_args, **method_kwargs)
      return self.run()
    return _loop

  def MenuItem(index: int, name: str) -> Callable:
    """
    A decorator for converting a user-defined function into a valid menu option
    """
    def _MenuItem(method):
      return MenuOption(method, name, index)  # Return a built menu option
    return _MenuItem

  def UIMenu(title, prompt="\nInput:\t", *args, **kwargs) -> Callable:
    """
    A class decorator to add all functionality and behaviours to the user-defined 'child' menu class
    """
    
    def _MenuClass(UnmodifiedClass):
      ModifiedClass = Singleton(UnmodifiedClass.__name__, (  # Convert the unmodified class into a singleton that inherits from this class
        Menu, 
      ), {
        **dict(UnmodifiedClass.__dict__), 
        **{"menu_title": title, "menu_prompt": prompt}
      })
      return ModifiedClass
    return _MenuClass
