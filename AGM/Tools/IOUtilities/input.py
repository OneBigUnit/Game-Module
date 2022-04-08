from typing import Union, Dict, List, Any, Optional

from .errors import InvalidChoiceError

from ..ConsoleControl.text import Text
from ..ConsoleControl.console import Console


class Input:
  """
  A collection of utilities that account for facilitated input
  """
  @staticmethod
  def get_inputted_item_from_iterable(sentence: str, items: Union[List[Any], Dict[Any, Any]], formatted_override_iterable: Optional[Union[List[Any], Dict[Any, Any]]]=None, start_buffer: bool=True) -> Any:
    """
    Takes an iterable, formats output, and selects an item from that iterable from user input
    """
    if not (isinstance(items, dict) or isinstance(items, list)):
      raise TypeError("The items parameter supplied was not of a valid type")
    if formatted_override_iterable is None:
      formatted_override_iterable = items

    buffer = ("\n" + Text.cyan("=" * 64) + "\n") if start_buffer else ""
    INDEX_PROMPT = f"{buffer}\n" + "\n".join([f"{idx + 1}) {item}" for idx, item in enumerate(formatted_override_iterable)])  # Format output
    try:
      item_index = int(Console.get_input(f"{INDEX_PROMPT}\n\n{sentence}", input_zone=True)) - 1  # Get user input
    except ValueError:
      raise TypeError("That input is not an integer") from None
    
    try:  # Select the specified item from the iterable
      if isinstance(items, list):
        return items[item_index]
      else:
        return items.get(list(items.keys())[item_index])
    except IndexError:
      raise InvalidChoiceError("That integer does not correspond to an option") from None
