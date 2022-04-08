"""
A collection of tools allowing for saved data integration
"""


from __future__ import annotations
from typing import Optional, Set, Any, Callable, List

from hashlib import sha256
import _pickle as pickle
import os
import time
import shutil
import inspect

from .errors import AccessError, VerificationError, SaveError

from ..ConsoleControl.console import Console


class Preservable:
  """
  A class containing all data preservation and saving/loading functionality using cpickle serialization
  """
  def __init__(self, save_name: str, save_path: str, save_password: Optional[str]=None, auto_save: bool=True) -> None:
    self.save_name = save_name
    if save_password is None:
      self.protected_save_password = None
    else:
      self.protected_save_password = self.__salt(self.__hash(save_password))
    self.save_path = "/".join(save_path.split("/"))
    self.auto_save = auto_save

    if not hasattr(self, "refreshable_signature"):
      self.refreshable_signature = None
    self.preserved_init_vars = self.__get_init_vars()

    self.__id = self.__salt(self.__hash(f"{self.save_name}{time.time_ns()}"))

    if self.auto_save:
      self.__create()

  def save(self) -> None:
    """
    Save the object to a file
    """
    if not os.path.exists(self.save_path + f"/Save - {self.save_name}"):
      os.makedirs(self.save_path + f"/Save - {self.save_name}")
    
    with open(f"{self.save_path}/Save - {self.save_name}/Save Data - {self.save_name}", 'wb') as f:
      pickle.dump(self, f)
  
  @classmethod
  def load(cls, save_name: str, save_path: str, prompt: str="\nPlease verify your password:\t", already_verified: bool=False, additional_tests: Optional[List[Callable]]=None) -> Preservable:
    """
    Load a previously saved object from a file
    """
    preservable = cls.__load(save_name, save_path, prompt, already_verified, additional_tests)
    try:
      if cls.refreshable_signature is not None:
        preservable.__refresh()
    except AttributeError:
      pass

    if preservable.auto_save:
      preservable.save()
    return preservable

  @classmethod
  def __load(cls, save_name: str, save_path: str, prompt: str, already_verified: bool, additional_tests: Optional[List[Callable]]) -> Preservable:
    """
    A mangled helper method to load pickled data from a file
    """
    if additional_tests is None:
      additional_tests = []
    if os.path.exists(f"{save_path}/Save - {save_name}/Save Data - {save_name}"):
      with open(f"{save_path}/Save - {save_name}/Save Data - {save_name}", 'rb') as f:
        preservable = pickle.load(f)
    else:
      raise AccessError("That Save Does Not Exist") from None
    
    for assertion, fail_message in additional_tests:
      try:
        if not assertion(preservable):
          raise AssertionError("Could not load, as an access check was failed")
      except AssertionError:
        if fail_message is None:
          fail_message = "Could not load, as an access check was failed"
        raise AccessError(fail_message)

    if already_verified or preservable.protected_save_password is None:
      return preservable
    if preservable.verify_password(Console.get_input(prompt, cover_character="*", input_zone=True)):
      return preservable
    raise VerificationError() from None
  
  def __get_init_vars(self) -> Set[str]:
    """
    A mangled helper method to scan and retrieve some changed __init__ source code since the last save
    """
    init_vars = []
    for line in inspect.getsource(self.__init__).splitlines()[1:]:
      try:
        if ((split_line := [part for part in line.split(" ") if part])[0].startswith("self.") and split_line[1] == "="):
          init_vars.append(line)
      except IndexError:
        continue
    return set(init_vars)

  def __refresh(self) -> None:
    """
    A mangled helper method to carry out the execution of refeshing an old class with newly added variables in the __init__ method
    """
    current_init_vars = self.__get_init_vars()
    new_init_vars = [line.lstrip() for line in current_init_vars - self.preserved_init_vars]
    for line in new_init_vars:
      try:
        exec(line)  # Safe unless code infiltrated, in which case there is no hope anyway...
      except Exception:
        raise SaveError("This save is out of date, and a new version of the save template has been created, which is nt backwards-compatible") from None
    self.preserved_init_vars = current_init_vars

  def edit_save_name(self, new_name: str, already_verified: bool=False, prompt: str="\nPlease verify your current save name:\t") -> None:
    """
    Changes and updates the save name in the file and class with verification
    """
    old_name = self.save_name
    if already_verified or self.protected_save_password is None:
      self.save_name = new_name
    else:
      if self.verify_password(Console.get_input(prompt, cover_character="*", input_zone=True)):
        self.save_name = new_name
      else:
        raise VerificationError() from None
    
    self.__create()
    self.delete(name_override=old_name, already_verified=already_verified)

    if self.auto_save:
      self.save()
  
  def edit_save_password(self, new_password: str, already_verified: bool=False, prompt: str="\nPlease verify your current save password:\t") -> None:
    """
    Changes and updates the save password in the file and class with verification
    """
    if already_verified or self.protected_save_password is None:
      self.protected_save_password = self.__salt(self.__hash(new_password))
    else:
      if self.verify_password(Console.get_input(prompt, cover_character="*", input_zone=True)):
        self.protected_save_password = self.__salt(self.__hash(new_password))
      else:
        raise VerificationError() from None
    
    if self.auto_save:
      self.save()
  
  def edit_saved_attribute(self, attribute_name: str, attribute_value: Any, set_sequence: Optional[Callable]=None, already_verified: bool=False, prompt: str="\nPlease verify your current save password:\t") -> None:
    """
    Changes and updates another specified saved attrivute in the file and class with verification
    """
    if already_verified or self.protected_save_password is None or set_sequence is not None:
      try:
        if set_sequence is None:
          setattr(self, attribute_name, attribute_value)
        else:
          set_sequence(getattr(self, attribute_name), attribute_value)
      except AttributeError:
        raise AccessError("The requested saved attribute to edit does not exist")
    else:
      if self.verify_password(Console.get_input(prompt, cover_character="*", input_zone=True)):
        try:
          setattr(self, attribute_name, attribute_value)
        except AttributeError:
          raise AccessError("The requested saved attribute to edit does not exist")
      else:
        raise VerificationError() from None
    
    if self.auto_save:
      self.save()

  def verify(caller_attribute: str, prompt: str="\nPlease verify your password:\t") -> Callable:
    """
    A decorator used to verify the user before calling a user-defined method
    """
    def _verify(f):
      def wrapper(caller, *args, **kwargs):
        try:
          self = getattr(caller, caller_attribute)
          assert isinstance(self, Preservable)
        except AttributeError:
          raise AccessError("The provided preservable attribute did not exist")
        except AssertionError:
          raise AccessError("The provided attribute was not a preservable object")
        if self.protected_save_password is not None:
          if not self.verify_password(Console.get_input(prompt, cover_character="*", input_zone=True)):
            raise VerificationError() from None
        return f(caller, *args, **kwargs)
      return wrapper
    return _verify

  def verify_password(self, password_verification: str) -> bool:
    """
    Cross-checks a password with the securely stored password for verification
    """
    if self.protected_save_password is None:
      return True
    return self.protected_save_password == self.__salt(self.__hash(password_verification))
  
  def __create(self) -> None:
    """
    A mangled helper method to create (or re-create) the saved files
    """
    if os.path.exists(self.save_path + f"/Save - {self.save_name}/Save Data - {self.save_name}"):
      raise SaveError("Save Already Exists") from None
    os.makedirs(self.save_path + f"/Save - {self.save_name}")
    
    with open(f"{self.save_path}/Save - {self.save_name}/Save Data - {self.save_name}", 'wb') as f:
      pickle.dump(self, f)
  
  def delete(self, name_override: Optional[str]=None, already_verified: bool=False, prompt: str="\nPlease verify your password:\t") -> None:
    """
    Deletes the saved files for the preservable object
    """
    if name_override is None:
      name_override = self.save_name
    if already_verified or self.protected_save_password is None:
      shutil.rmtree(self.save_path + f"/Save - {name_override}")
    else:
      if self.verify_password(Console.get_input(prompt, cover_character="*", input_zone=True)):
        shutil.rmtree(self.save_path + f"/Save - {name_override}")
      else:
        raise VerificationError() from None

  def __hash(self, _input: str) -> str:
    """
    A mangled helper method to generate a SHA256 digest/hash
    """
    return sha256((str(type(_input)) + str(_input)).encode()).digest()
  
  def __salt(self, _input):
    """
    A mangled helper method to salt an input with the SHA256 hashing algorithm
    """
    return _input + sha256(_input).digest()

  def __eq__(self, other: Any) -> bool:
    """
    Override the builtin __eq__ to check for preservable object equality
    """
    return (self.__id == other.__id) and (type(self) is type(other))

  def in_development() -> Callable:
    """
    A decorator to mark preservable classes as 'in development', so the program can attempt to update old saves with new additions to the class automatically
    """
    def _class(unrefreshable_class):
      setattr(unrefreshable_class, "refreshable_signature", unrefreshable_class)
      return unrefreshable_class
    return _class
