"""
A collection of tools relating to cursor manipulation
"""


class Cursor:
  """
  A static class containing different functionality relating to the cursor
  """
  @staticmethod
  def up(n: int=1) -> None:
    """
    Move the cursor up 'n' spaces
    """
    print(f"\033[{n}A", end="", flush=True)

  @staticmethod
  def down(n: int=1) -> None:
    """
    Move the cursor down 'n' spaces
    """
    print(f"\033[{n}B", end="", flush=True)

  @staticmethod
  def forward(n: int=1) -> None:
    """
    Move the cursor forward 'n' spaces
    """
    print(f"\033[{n}C", end="", flush=True)

  @staticmethod
  def back(n: int=1) -> None:
    """
    Move the cursor back 'n' spaces
    """
    print(f"\033[{n}D", end="", flush=True)

  @staticmethod
  def clear_line() -> None:
    """
    Clear the line that the cursor is currently on of characters
    """
    print("\033[1K", end="", flush=True)

  @staticmethod
  def carriage_return() -> None:
    """
    Return to the beginning of the same line to overwrite the previous input
    """
    print("\r", end="", flush=True)
