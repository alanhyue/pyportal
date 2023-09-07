import subprocess


class ScriptRepo:
    def __init__(self, path):
        self.repo = path
        if not self.is_a_git_repo():
            raise ValueError('Path specified is not a git repo. "%s"' % path)

    def is_a_git_repo(self):
        cp = subprocess.run(
            ["git", "-C", str(self.repo), "status"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if "not a git repository" in cp.stderr.decode("utf8"):
            return False
        return True

    def logs(self):
        import re
        cp = subprocess.run(
            ["git", "-C", str(self.repo), "log", "--date=format:%Y%m%d%H%M%S"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        text = cp.stdout.decode("utf8")
        text = re.split('^commit ', text, flags=re.MULTILINE)
        text = [l.strip() for l in text if l.strip() != ""]
        logs = [
            re.search("(.*?)\nAuthor: (.*?)\nDate:(.*?)\n\n(.*)", log).groups()
            for log in text
        ]
        logs = [[x.strip() for x in l] for l in logs]
        names = ["commit", "author", "date", "comment"]
        logs = [dict(zip(names, l)) for l in logs]
        return logs

    def get_commit_by_comment_keyword(self, kwd, exact=False):
        for l in self.logs():
            if not exact and kwd in l["comment"]:
                return l["commit"]
            if exact and kwd == l["comment"]:
                return l["commit"]
        raise ValueError(
            "No commit found with comment like '%s'\nRepo commits:\n%s "
            % (kwd, "\n".join([str(d) for d in self.logs()]))
        )

    def get_commit_by_date(self, date):
        for l in self.logs():
            if l["date"] == date:
                return l["commit"]
        raise ValueError(
            "No commit found with date = '%s'\nRepo commits:\n%s "
            % (date, "\n".join([str(d) for d in self.logs()]))
        )

    def exec_script(self, code):
        import inspect

        caller_globals = inspect.stack()[1][0].f_globals
        exec(code, caller_globals)

    def run_script_in_commit(self, commit, fpath):
        self.exec_script(self.read_script_in_commit(commit, fpath))

    def read_script_in_commit(self, commit, fpath):
        # given a commit hash
        cp = subprocess.run(
            ["git", "-C", str(self.repo), "show", commit + ":" + fpath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if len(cp.stderr) > 0:
            raise ValueError("git show file failed: %s" % cp.stderr)
        return cp.stdout.decode("utf8")

    def pull(self):
        cp = subprocess.run(
            ["git", "-C", str(self.repo), "pull", "origin", "master"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print(cp.stderr.decode("utf8"))
        print(cp.stdout.decode("utf8"))

    def run_script_by_comment(self, kwd, fpath, comment_exact_match=False):
        return self.run_script_in_commit(
            self.get_commit_by_comment_keyword(kwd, comment_exact_match), fpath,
        )

    def run_script(self, fpath, comment_kwd=None, comment_exact_match=False, date=None):
        self.exec_script(
            self.read_script(fpath, comment_kwd, comment_exact_match, date)
        )

    def read_script(
        self, fpath, comment_kwd=None, comment_exact_match=False, date=None
    ):
        if comment_kwd is not None:
            commit = self.get_commit_by_comment_keyword(
                comment_kwd, comment_exact_match
            )
        elif date is not None:
            commit = self.get_commit_by_date(date)
        else:
            # no version specified, default to the latest version
            commit = "master"
            print("Reading the bleeding edge version of", fpath)
            info = self.logs()[0]
            print(
                "date:%s, comment:%s, commit:%s"
                % (info["date"], info["comment"], info["commit"])
            )
        return self.read_script_in_commit(commit, fpath)
