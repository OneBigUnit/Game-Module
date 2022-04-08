from ..ConsoleControl.text import Text


class Output:
  """
  A collection of utilities that account for facilitated output
  """
  @staticmethod
  def speech(speaker: str, *speech: str, sep: str="\n", blank_canvas: bool=False) -> str:
    """
    Takes parameters and formats an output that represents in-game speech
    """
    nl = "\n"
    formatted_speaker = Text.magenta(Text.bold(f"[{speaker}]"))
    text = f"{nl if not blank_canvas else ''}{formatted_speaker}\t"
    for words in speech:
      text += f"{words}{sep}"
    return text[:-1]
    
  @staticmethod
  def hint(*speech: str, sep: str="\n", blank_canvas: bool=False) -> str:
    """
    Takes parameters and formats an output that represents tutorial-like hints
    """
    nl = "\n"
    formatted_speaker = Text.yellow(Text.bold("[HINT]"))
    text = f"{nl if not blank_canvas else ''}{formatted_speaker}\t"
    for words in speech:
      text += f"{words}{sep}"
    return text[:-1]
