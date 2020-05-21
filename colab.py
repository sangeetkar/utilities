import subprocess
from pathlib import Path

class DirectoryCreationError (Exception):
  pass
class MountingError (Exception):
  pass

def create_wd (drive_folder, active_folder):
  import subprocess
  if (subprocess.run(["mkdir", active_folder]).returncode != 0):
    raise DirectoryCreationError
  if(subprocess.run(["mount", 
                     "--bind", 
                     f"/content/drive/My Drive/ml/{drive_folder}", 
                     f"/content/{active_folder}/"]).returncode != 0):
    raise MountingError
  return Path(".")/active_folder

