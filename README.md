# pyportal

When you have scripts like below

```
# /myscripts/utils.py
def my_func():
    print("hello!")

# /myscripts/data_analysis.py
def show_df(df):
    print(df)
```


```python
import pyportal
pyportal.path = ['/myscripts'] # OR, configure global path in environemnt variable (see below)
import pyportal.utils.file as U
U.my_func()

from pyportal.data_analysis.file import show_df
show_df()
```

## Installation

```
pip install pyportal
```

## Import from a commit


```
# Commit 1
# /myscripts/utils.py
def my_func():
    print("version 1")

# Commit 2, timestamp 20251231235959
# /myscripts/utils.py
def my_func():
    print("version 2")

# ...

# Commit 10, timestamp 20261231235959
# /myscripts/utils.py
def my_func():
    print("version 10")

```

```python
import pyportal
import pyportal.utils.v20251231235959 as U
U.my_func()
# prints "version 2"

import pyportal.utils.v20261231235959 as U2
U2.my_func()
# prints "version 10"
```


## pyportal path

Set it up globally on your computer or locally in a script.

Configure globally in environment variable `PYPORTAL_PATH`, separated by a semicolon:
```
PYPORTAL_PATH = "/myscript1;/home/var/mylibrary"
```

Temporarily set/update portal path in code:

```python
import pyportal
pyportal.path.insert(0, "/search/this/folder/first")
```


## Doc

```
import pyportal.[path_to_file].[version] 
```

`[path_to_file]`: can be the script name or path.`import pyportal.utils.file` : import the FIRST script or package found under the `path`. Modules are folders that contain `__init__.py`. `utils` can be a path pointing to a script or package, like `pyportal.utils.network.file`, if relative path `utils/network` exists under one of the paths.


`[version]`: `file` or `vyyyymmddHHMMSS`. The latter is v + the timestamp of the commit.

Import from commit only works if the folder is a git repo. The timestamp of the commit will be shown when you use `.file` to import a file form a repo, you just need to copy and paste the version, replacing the `.file` with `vYOURVERSION` to lock it.

