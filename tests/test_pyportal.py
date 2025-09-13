import subprocess
import textwrap
import pytest
import time

@pytest.fixture
def script_dir(tmp_path):
    """Create a tmp folder with a foo.py script (no git)."""
    repo_dir = tmp_path / "myscripts"
    repo_dir.mkdir()

    foo_py = repo_dir / "foo.py"
    foo_py.write_text(
        textwrap.dedent(
            """\
            def bar():
                return "version 1"
            """
        )
    )
    return repo_dir

def git_init(folder):
    subprocess.run(["git", "init"], cwd=folder, check=True)

def commit_changes(folder, msg="default commit message"):
    subprocess.run(["git", "add", "foo.py"], cwd=folder, check=True)
    subprocess.run(
        ["git", "commit", "-m", msg], cwd=folder, check=True
    )

@pytest.fixture
def git_script_dir(script_dir):
    """Turn the script_dir into a git repo and commit the file."""
    git_init(script_dir)
    commit_changes(script_dir, 'committing version 1')
    # must sleep because commits are distinguished by timestamps down to SECONDS
    time.sleep(2)
    # second commit
    foo_py = script_dir / "foo.py"
    foo_py.write_text(
        textwrap.dedent(
            """\
            def bar():
                return "version 2"
            """
        )
    )
    commit_changes(script_dir, 'committing version 2')
    # uncommitted changes
    foo_py.write_text(
        textwrap.dedent(
            """\
            def bar():
                return "version 3"
            """
        )
    )
    return script_dir


def test_imports_from_git_repo(git_script_dir, monkeypatch):
    import importlib

    import pyportal

    # point pyportal at tmp folder
    monkeypatch.setattr(pyportal, "path", [str(git_script_dir)])

    # import from file on disk
    foo_module = importlib.import_module("pyportal.foo.file")
    assert hasattr(foo_module, "bar")
    assert foo_module.bar() == "version 3"
    assert not hasattr(foo_module, "notdefined")

    from pyportal.scriptrepo import ScriptRepo

    repo = ScriptRepo(git_script_dir)
    commits = repo.logs()[::-1] # .logs() returns the most recent commits first, reverse so it's in ascending order
    print("all commits")
    print(commits)
    for i, cmt in enumerate(commits):
        date = cmt['date']
        print('read commit from date', date)
        foo_module = importlib.import_module(f"pyportal.foo.v{date}")
        assert hasattr(foo_module, "bar")
        assert foo_module.bar() == f"version {i+1}"
        assert not hasattr(foo_module, "notdefined")



def test_import_from_file_outside_a_repo(script_dir, monkeypatch):
    import importlib

    import pyportal

    # point pyportal at tmp folder
    monkeypatch.setattr(pyportal, "path", [str(script_dir)])

    # now dynamically import foo
    foo_module = importlib.import_module("pyportal.foo.file")
    assert hasattr(foo_module, "bar")
    assert foo_module.bar() == "version 1"




@pytest.fixture
def multi_script_dir(tmp_path):
    """
    Create two subfolders, each with foo.py, but different implementations.
    This tests whether pyportal can distinguish between them.
    """
    root = tmp_path / "myscripts"
    root.mkdir()

    sub1 = root / "sub1"
    sub1.mkdir()
    (sub1 / "foo.py").write_text(
        textwrap.dedent(
            """\
            def bar():
                return "hello from sub1"
            """
        )
    )

    sub2 = root / "sub2"
    sub2.mkdir()
    (sub2 / "foo.py").write_text(
        textwrap.dedent(
            """\
            def bar():
                return "hello from sub2"
            """
        )
    )

    sub3 = root / "sub3"
    sub3.mkdir()
    (sub3 / "__init__.py").write_text(
        textwrap.dedent(
            """\
            from .foo import bar as mybar
            """
        )
    )
    (sub3 / "foo.py").write_text(
        textwrap.dedent(
            """\
            def bar():
                return "hello from sub3"
            """
        )
    )

    return root, sub1, sub2, sub3

def test_same_name_from_different_folders(multi_script_dir, monkeypatch):
    import importlib
    script_dir, sub1, sub2, sub3 = multi_script_dir

    import pyportal

    # the first matching script will be used
    monkeypatch.setattr(pyportal, "path", [str(sub1), str(sub2)])
    foo_module = importlib.import_module("pyportal.foo.file")
    assert hasattr(foo_module, "bar")
    assert foo_module.bar() == "hello from sub1"

    # try sub2 first
    monkeypatch.setattr(pyportal, "path", [str(sub2), str(sub1)])
    foo_module = importlib.import_module("pyportal.foo.file")
    assert hasattr(foo_module, "bar")
    assert foo_module.bar() == "hello from sub2"

    # set to parent folder
    monkeypatch.setattr(pyportal, "DEBUG", True)
    monkeypatch.setattr(pyportal, "path", [str(script_dir)])
    foo_module = importlib.import_module("pyportal.sub1.foo.file")
    assert hasattr(foo_module, "bar")
    assert foo_module.bar() == "hello from sub1"
    foo_module = importlib.import_module("pyportal.sub2.foo.file")
    assert hasattr(foo_module, "bar")
    assert foo_module.bar() == "hello from sub2"

    # import sub3 as a package (it has __init__.py)
    monkeypatch.setattr(pyportal, "path", [str(script_dir)])
    foo_module = importlib.import_module("pyportal.sub3.file")
    assert hasattr(foo_module, "mybar")
    assert not hasattr(foo_module, "bar")
    assert foo_module.mybar() == "hello from sub3"

    # import a specifc module inside sub3
    foo_module = importlib.import_module("pyportal.sub3.foo.file")
    assert not hasattr(foo_module, "mybar")
    assert hasattr(foo_module, "bar")
    assert foo_module.bar() == "hello from sub3"
