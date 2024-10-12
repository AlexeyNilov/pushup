import shutil
import subprocess

from fastlite import create_mod

from data.fastlite_db import DB


name = "dataclasses"
create_mod(DB, name)
shutil.move(f"{name}.py", f"data/{name}.py")
subprocess.run(["black", f"data/{name}.py"])
