import sys
import os.path
import pathlib
import sys, importlib.util

DEBUG = False
PACKAGE_NAME = "pyportal"
import os

path = os.environ.get("PYPORTAL_PATH", "").split(";")
# remove empty strings
path = [s for s in path if s.strip() != ""]
from pathlib import Path


def read_file_text(sr, fname):
    # file from last commit
    lc = sr.logs()[0]
    lc_text = sr.read_script_in_commit(lc["commit"], fname)
    # text on disk
    text = (Path(sr.repo) / fname).read_text(encoding="utf8")
    if text == lc_text:
        print('Reading file "%s" from the last commit (%s)' % (fname, lc["date"]))
    else:
        print(
            'Reading file on disk. Note, file "%s" has uncommitted changes. Last commit is %s'
            % (fname, lc["date"])
        )
    return text


def get_script_content(fin):
    return fin.read_text(encoding="utf8")


def get_version(script_path, ver):
    from .scriptrepo import ScriptRepo
    from pathlib import Path

    try:
        sr = ScriptRepo(Path(script_path).parent)
    except ValueError:
        sr = None
    if sr is None:
        # script not in a git repo
        if ver != "file":
            raise ValueError(
                f"The requested script is not in a git repo,"
                " you can ONLY read the file currently on disk. E.g., 'import script_repo.<not_in_a_repo_script>.file'."
                f" More information: located script path = '{script_path}', requested version: '{ver}'"
            )
        return script_path.read_text(encoding="utf8")
    else:
        # script is in a git repo
        fpath_relative = "./" + script_path.stem + ".py"
        if ver == "file":
            return read_file_text(sr, fpath_relative)
        elif ver == "latest":
            date = None
        else:
            # ver is like "v123", get the "123" part after "v"
            date = ver[1:]
        code = sr.read_script(fpath_relative, date=date)
        return code


def ts(fmt="%Y-%m-%d %H%M%S"):
    from datetime import datetime

    return datetime.now().strftime(fmt)


class ScriptImporter:
    def __init__(self, code, cache_module=True):
        self.code = code
        self.cache_module = cache_module

    @classmethod
    def find_spec(cls, name, module_path, target=None):
        global path
        cache_module = True
        if DEBUG and name.startswith(PACKAGE_NAME):
            print(f"name={name} module_path={module_path} target={target}")
        if name == PACKAGE_NAME:
            # handle top level import with an empty module so no exception is raised
            return importlib.util.spec_from_loader(name, loader=cls(""))
        if not name.startswith(PACKAGE_NAME + "."):
            # not our thing, hand over to other importers
            return None
        parts = name.split(".")
        if len(parts) == 1:
            raise ImportError(
                f"You must specify a script name, such as 'import {PACKAGE_NAME}.utils'"
            )
        elif len(parts) == 2:
            # no version specified, use the latest version
            return importlib.util.spec_from_loader(name, loader=cls(""))

        sub_parts = parts[1:]  # skip PACKAGE_NAME
        # if last part is 'file or version', treat as the target script file
        if sub_parts[-1] == "file" or sub_parts[-1].startswith('v'):
            version = sub_parts[-1]
            script_parts = sub_parts[:-1]  # all parts before 'file'
            # try to find the file on disk in any root path
            script_file = None
            for root in path:
                candidate_folder = pathlib.Path(root).joinpath(*script_parts)
                init_file = candidate_folder / '__init__.py'
                if candidate_folder.is_dir() and init_file.is_file():
                    # import the package
                    code = get_version(init_file, version)
                    return importlib.util.spec_from_file_location(
                                name,
                                str(init_file),
                                loader=cls(code, cache_module),
                                submodule_search_locations=[str(candidate_folder)],  # ← marks as package
                            )
                candidate_file = pathlib.Path(root).joinpath(*script_parts).with_suffix(".py")
                if candidate_file.is_file():
                    script_file = candidate_file
                    break
            if script_file is None:
                raise ImportError(f"Script {'.'.join(script_parts)} not found under {path}")

            code = get_version(script_file, version)
            # return importlib.machinery.ModuleSpec(name, loader=cls(code, cache_module))
            return importlib.util.spec_from_loader(name, 
                                                   loader=cls(code, cache_module),
                                                   )
        return importlib.util.spec_from_loader(name, loader=cls("", cache_module))

    def create_module(self, spec):
        """
        .file will always reload the module

        To avoid reloading and use the cached module as the first import, use .file_cache

        from pyportal.test_import.file_cache import x
        """
        if spec.name.endswith(".file"):
            tmp_name = spec.name + "_cache"
            if tmp_name in sys.modules:
                del sys.modules[tmp_name]

            import types

            spec.name = tmp_name
            # Create a new module with this random name
            module = types.ModuleType(spec.name)
            # Optionally set any other attributes on the module here
            return module

        return None  # use default module creation semantics

    def exec_module(self, module):
        # Execute the module in its namespace
        exec(self.code, module.__dict__)
        module.__path__ = "."


sys.meta_path.append(ScriptImporter)
