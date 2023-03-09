# script importer

> Import from any version of python scripts.


You have a script of frequently used functions, but you don't feel comfortable importing the script because you modify it frequently and that breaks dependencies. If this is you, worry no more. In new projects, just use `script_importer` to lock dependency on a specific version of your script, and no future changes will break it!

# Use script_importer

The following short example demonstrates how to import functions from any version of a python script.

Say you have a script file `myutils.py` that contains a `say_hello` function defined as below

__myutils.py__

```
def say_hello():
    print('hello')
```

You happily used it in another place:

```
# line 1
import script_importer
# line 2
from script_importer.myutils.latest import my_func
# line 3
my_func()
# prints: hello
```

Now you have dependency in this code. Future changes to `say_hello` will break it. With `script_importer`, you lock the import on the specific version (identified by the yyyymmddHHMMSS of the commit). You can make whatever changes to your script and dependency will never be an issue again:

```
import script_importer
# specify a version to import from
from script_importer.myutils.v20230103192241 import my_func
my_func()
# prints: hello
```

# install

This is not yet published to pypi.

You can install it by git cloning the repo and run the following command in the cloned folder to install the package locally:

`pip install -e .`

# Behind the wheels - how set script folders
You need to tell script_importer which folders to look up for scripts. You can set the folders globally in the SCRIPT_IMPORTER_PATH=C:\myscripts;C:\Document\PythonScripts variable, (separate multiple folders by a semicolon), or just the current context by setting `script_importer.path=[path1, path2, ...]`.
