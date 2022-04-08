"""
A collection of tools relating to console manipulation
"""


from typing import Callable, Optional

import functools
import termios
import tty
import sys
import os
import string

from .cursor import Cursor


class Console:
  """
  A static class containing different functionality relating to the console
  """
  @staticmethod
  def get_key() -> str:
    """
    Waits for input, and returns the first key pressed after being called as a string
    """
    file_descriptors = termios.tcgetattr(sys.stdin)  # Store the original file descriptors
    tty.setcbreak(sys.stdin)  # Sets the console to cbreak (rare) mode, to deal with single character input
    key = sys.stdin.read(1)[0]  # Hangs until a key is pressed
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, file_descriptors)  # Reset the console mode back to its original state
    return key

  @staticmethod
  def clear(method: Callable) -> Callable:
    """
    A decorator to clear the console before running the callable argument
    """
    @functools.wraps(method)
    def _clear(*method_args, **method_kwargs):
      Console.clear_now()
      method(*method_args, **method_kwargs)
    return _clear
  
  @staticmethod
  def clear_now() -> None:
    """
    Clear the console
    """
    os.system("clear")  # Clear the console
  
  @staticmethod
  def get_input(*args, cover_character: Optional[str]=None, end: str="", sep: str=" ", input_zone: bool=False) -> str:
    """
    A re-written, extended version of the inbuilt 'input' function, to get input from the user via the console, after pressing enter
    """
    msg = sep.join([str(arg) for arg in args])
    original_cover_character = cover_character
    raw_input = []  # The actual user input
    cover_characters = []  # The printed list of characters
    print(msg, "\n\nInput:\t" if input_zone else "", end=end, flush=True)

    while True:
      current_character = Console.get_key()
      if original_cover_character is None:
        cover_character = current_character

      if ord(current_character) == 10:  # Enter
        break
      elif ord(current_character) == 127:  # Backspace
        try:
          del raw_input[-1]
          del cover_characters[-1]
        except IndexError:  # No characters left to delete
          continue
      elif ord(current_character) == 9:  # Tab
        cover_characters.append(cover_character)
        raw_input.append("\t")
      elif ord(current_character) == 32:  # Space
        cover_characters.append(cover_character)
        raw_input.append(" ")
      elif current_character not in string.printable:  # Not a recognized character
        continue
      else:  # A non-special, recognized character
        cover_characters.append(cover_character)
        raw_input.append(current_character)
      Cursor.clear_line()
      Cursor.carriage_return()
      print("Input:\t" if input_zone else msg.split("\n")[-1], "".join(cover_characters), end="", flush=True)  # Re-print the final line of the covered input
    print()  # Print a newline (\n) character to finish for formatting purposes only
    return "".join(raw_input)
