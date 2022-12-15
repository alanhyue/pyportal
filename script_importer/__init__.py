import sys
import os.path

import sys, importlib.util

DEBUG = False
PACKAGE_NAME = "script_importer"
import os

path = os.environ.get("SCRIPT_IMPORTER_PATH", "").split(";")
# remove empty strings
path = [s for s in path if s.strip() != ""]
# SCRIPT_PATH = [r"D:\yueheng6\Documents", r"D:\yueheng6\Desktop\Project - 商分\18 modular"]
from pathlib import Path


def get_script(fname):
    if len(path) == 0:
        raise ValueError(
            f"No script path configured"
            ". You can set path globally in the environment variable SCRIPT_IMPORTER_PATH"
            ", or locally in the variable with script_importer.path.append('script_folder_path')"
        )
    for fo in path:
        p = Path(fo) / (fname + ".py")
        if p.exists():
            return p
    # no script found
    raise ValueError(
        f"No script named {fname}.py found. Please make sure the script exists under {path=}"
    )


def get_script_content(fname):
    fin = get_script(fname)
    if fin is not None:
        return fin.read_text(encoding="utf8")


def get_version(fname, ver):
    fin = get_script(fname)
    if fin is not None:
        from .scriptrepo import ScriptRepo
        from pathlib import Path

        sr = ScriptRepo(Path(fin).parent)
        if ver == "latest":
            date = None
        else:
            # ver is like "v123", get the "123" part after "v"
            date = ver[1:]
        code = sr.read_script("./" + fin.stem + ".py", date=date)
        return code


class ScriptImporter:
    def __init__(self, code):
        self.code = code

    @classmethod
    def find_spec(cls, name, path, target=None):
        if DEBUG and name.startswith(PACKAGE_NAME):
            print(f"{name=} {path=} {target=}")
        if name == PACKAGE_NAME:
            # handle top level import with an empty module so no exception is raised
            return importlib.util.spec_from_loader(name, loader=cls(""))
        if not name.startswith(PACKAGE_NAME + "."):
            # not our thing, delegate to other importers
            return None
        else:
            parts = name.split(".")
            if len(parts) == 1:
                raise ImportError(
                    f"You must specify a script name, such as 'import {PACKAGE_NAME}.utils'"
                )
            elif len(parts) == 2:
                # no version specified, use the latest version
                return importlib.util.spec_from_loader(name, loader=cls(""))
                raise ValueError(
                    "No version specified."
                    " To use the latest (current on disk) version, use 'import script_importer.[fname].latest'"
                    " If you want to import the version from a specific commit, use 'import script_importer.[fname].v[date]'."
                )

            elif len(parts) == 3:
                # the version part either starts with v or is latest, otherwise the third part is not a version
                if parts[2].startswith("v") or parts[2] == "latest":
                    fname, ver = parts[1], parts[2]
                    src = get_version(fname, ver)
                else:
                    raise ValueError(
                        "No version specified."
                        " To use the latest (i.e., the currently on disk) version, use 'import script_importer.[fname].latest'"
                        " If you want to import the version from a specific commit, use 'import script_importer.[fname].v[date]'."
                    )
            else:
                objname = parts[-1]
                raise ValueError(
                    f"the object named '{objname}' is not found in {name}. Does it exist in the specified version of the script?"
                )
            return importlib.util.spec_from_loader(name, loader=cls(src))

    def create_module(self, spec):
        return None  # use default module creation semantics

    def exec_module(self, module):
        exec(self.code, module.__dict__)
        # set the __path__ attribute so the module is regarded as a package
        module.__path__ = "."


sys.meta_path.append(ScriptImporter)
