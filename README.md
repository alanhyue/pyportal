# pyportal

**Dependable Imports for Your Ever-Changing Scripts.**


Working with constantly changing Python scripts poses a unique challenge: how do you maintain reliable imports? The answer is `pyportal`. This innovative tool enables you to **lock in** on a specific version of your script, ensuring that future changes won't disrupt your dependencies. With `pyportal`, you're free to innovate and iterate your scripts while keeping other projects stable and dependable.


## Examples

**Example 1: Simple Import**  You can use `pyportal` to import the latest version of the `say_hello` function from `myutils.py`. This will always import `say_hello` from the most recent commit (as the suffix `.latest` suggests).

```python
# This is your original script file `myutils.py`
def say_hello():
    print('hello')

# Now you want to use it in another place:
import pyportal
from pyportal.myutils.latest import say_hello

# Using the function
say_hello()  # prints: hello
```

**Example 2: Version-specific Import** With the `.v` suffix, `pyportal` can import a specific version of a function. Even though `myutils.py` has been modified, you can still access the old version of `say_hello` thanks to `pyportal`.

```python
# Assume that you have modified `myutils.py` and it now looks like this:
def say_hello():
    print('hello, world!')

# But you still want the old version in another place:
import pyportal

# v20230103192241 is a version identifier, 'v' followed by the datetime of the specific git commit
from pyportal.myutils.v20230103192241 import say_hello

# Using the function
say_hello()  # prints: hello
```

**Example 3: Managing Multiple Script Versions** `pyportal` allows you to manage and use multiple versions of a script within the same project. By importing different versions of the `say_hello` function under different names, you can use the version that suits your needs in each part of your project.

```python
# Assume that you have multiple versions of `myutils.py` and you want to use different versions in different places:
import pyportal

# Importing a specific version, again using the datetime of the commit as the version identifier
from pyportal.myutils.v20230103192241 import say_hello as old_hello
old_hello()  # prints: hello
```


**Example 4: Importing Like Standard Python Imports** With the `.file` suffix, you can import whatever is currently in the script file with `pyportal`. It works just like the standard Python import. This is particularly useful for testing out your scripts. But be aware, you must commit your changes to be able to lock in on them, as shown in Example 2.

```python
# Assume that you have multiple versions of `myutils.py` and you want to use different versions in different places:
import pyportal

# Importing a specific version, again using the datetime of the commit as the version identifier
from pyportal.myutils.v20230103192241 import say_hello as old_hello
old_hello()  # prints: hello
```

## How to use

**Install the package**

```
pip install pyportal
```

**Import syntax**

You must import the `pyportal` package first. Then you can import a specific version of a script.

For example, you have a folder with the following structure

```python
# /utility_scripts/myutil.py
def foo():
    pass

###

# In any python script on your computer
import pyportal
# add script folder
pyportal.path.insert(0, "/utility_scripts")

# Import from script myutil.py
from pyportal.myutil.file import foo
# OR import the whole script
import pyportal.myutil.file as Util
# OR import everything
from pyportal.myutil.file import *
```

Package statement follows the syntax `pyportal.<name_of_scriptfile>.<version>` (e.g., `pyportal.myutil.latest`). It always has three components, separated by dots.

1. `pyportal`. The name of the package.
2. `<name_of_scriptfile>`. The file name of your script, *no space allowed*. `pyportal` searches in order of specified folders (see the setup guide below), and returns the first result. Try not to have scripts under the same name.
3. `<version>`. Specify the version of the script to import from. Can be one of
   1. `file`. Import the file on disk just like the standard Python import.
   2. `vyyyymmddHHMMSS`. Import a specific version to lock in. It is a `v` followed by the datetime of the git commit in yyyymmddHHMMSS (year month day hour minutes seconds) format.


**Setup script folders**

Working like Python imports, `pyportal` searches for the requested script by its file name in the given folders. You can set the folders globally in the environment variable `pyportal_PATH`. For example, we add a folder under C drive named `my scripts`, and another folder named `PythonScripts` under our Documents folder. In all OS systems, you need to separate multiple folders by a `semicolon`. Note that the order of folders matters. If you have two script files with the same name, the one that appeared first in the folders will be used.

```cmd
pyportal_PATH=C:\my scripts;C:\Document\PythonScripts
```

You can also modify the path `pyportal` searches by manipulating its `path` attribute:

```python
import pyportal
# modify the path list and add a new folder to search for scripts
pyportal.path.append('D:/new script')
# import a constant from a script located at D:/new script/foo.py
from pyportal.foo.file import pi
print(pi) 
# prints 3.14
```
