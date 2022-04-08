"""
A collection of tools relating to text formatting and manipulation
"""


import re


class Text:
  """
  A static class containing different functionality relating totext formatting
  """

  # Class-Level constant octal escape characer codes
  END = "\033[0m"
  BLACK = "\033[30m"
  RED = "\033[31m"
  GREEN = "\033[32m"
  YELLOW = "\033[33m"
  BLUE = "\033[34m"
  MAGENTA = "\033[35m"
  CYAN = "\033[36m"
  WHITE = "\033[37m"
  SUCCESS = "\033[92m"
  WARNING = "\033[93m"
  FAIL = "\033[91m"
  BOLD = "\033[1m"
  DIM = "\033[2m"
  UNDERLINE = "\033[4m"

  @classmethod
  def black(cls, string: str) -> str:
    """
    Convert the argument string only to black text
    """
    return f"{cls.BLACK}{string}{cls.END}"

  @classmethod
  def yellow(cls, string: str) -> str:
    """
    Convert the argument string only to yellow text
    """
    return f"{cls.YELLOW}{string}{cls.END}"

  @classmethod
  def blue(cls, string: str) -> str:
    """
    Convert the argument string only to blue text
    """
    return f"{cls.BLUE}{string}{cls.END}"

  @classmethod
  def white(cls, string: str) -> str:
    """
    Convert the argument string only to white text
    """
    return f"{cls.WHITE}{string}{cls.END}"

  @classmethod
  def green(cls, string: str) -> str:
    """
    Convert the argument string only to green text
    """
    return f"{cls.GREEN}{string}{cls.END}"

  @classmethod
  def red(cls, string: str) -> str:
    """
    Convert the argument string only to red text
    """
    return f"{cls.RED}{string}{cls.END}"

  @classmethod
  def magenta(cls, string: str) -> str:
    """
    Convert the argument string only to magenta (shade of pink) text
    """
    return f"{cls.MAGENTA}{string}{cls.END}"

  @classmethod
  def cyan(cls, string: str) -> str:
    """
    Convert the argument string only to cyan (shade of blue) text
    """
    return f"{cls.CYAN}{string}{cls.END}"

  @classmethod
  def success(cls, string: str) -> str:
    """
    Convert the argument string only to 'success' (shade of green) text
    """
    return f"{cls.SUCCESS}{string}{cls.END}"

  @classmethod
  def warning(cls, string: str) -> str:
    """
    Convert the argument string only to 'warning' (shade of yellow) text
    """
    return f"{cls.WARNING}{string}{cls.END}"

  @classmethod
  def fail(cls, string: str) -> str:
    """
    Convert the argument string only to 'fail' (shade of red) text
    """
    return f"{cls.FAIL}{string}{cls.END}"

  @classmethod
  def bold(cls, string: str) -> str:
    """
    Convert the argument string only to emboldened text
    """
    return f"{cls.BOLD}{string}{cls.END}"

  @classmethod
  def dim(cls, string: str) -> str:
    """
    Convert the argument string only to dimmed text
    """
    return f"{cls.DIM}{string}{cls.END}"

  @classmethod
  def underline(cls, string: str) -> str:
    """
    Convert the argument string only to underlined text
    """
    return f"{cls.UNDERLINE}{string}{cls.END}"

  @staticmethod
  def string_insert(index: int, insertion: str, initial_string: str) -> str:
    """
    Return a new string with the inserted substring at a specified index
    """
    return initial_string[:index] + insertion + initial_string[index:]

  @staticmethod
  def heading(string: str) -> str:
    """
    Converts the argument string into a heading format, accounting for most notable rule-exceptions (articles & formatting codes)
    """
    formatting_data = {match.start(0): match.group() for match in re.finditer("\\x1b\[[\s\S]*?m", string)}  # Locate all the formatting escape codes in the string, and save the data
    for formatting_string in list(formatting_data.values()):  # Strip the formatting from the string
      string = string.replace(formatting_string, "")
    articles = ["the", "a", "an"]
    string = string.split(" ")
    for idx, word in enumerate(string):
      if word.lower() in articles and idx != 0 and idx != len(string) - 1:
        string[idx] = word.lower()
        continue
      string[idx] = word[0].upper() + word[1:].lower()
    string = " ".join(string)
    for formatting_idx in formatting_data:  # Convert the correctly capitalized string back to have its old formatting
      string = Text.string_insert(formatting_idx, formatting_data.get(formatting_idx), string)
    return string
