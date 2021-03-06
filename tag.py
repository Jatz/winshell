import os, sys
import subprocess

PROJECT = "winshell"
VERSION_FILE = "__%s_version__.py" % PROJECT

VERSION_BLOCK = """
# -*- coding: UTF8 -*-
__VERSION__ = "%(tag)s"
__RELEASE__ = ""
"""


def git(command):
    if isinstance(command, basestring):
        command = [command]
    return subprocess.check_output(["git.cmd"] + command)

def main(tag):
    #
    # Add stuff to changelog
    #
    git("checkout master")
    git("pull")
    with open(VERSION_FILE, "w") as f:
        f.write(VERSION_BLOCK % tag)
    git(["add", VERSION_FILE])
    git(["commit", "-m", "Tagged master for v%s" % tag])

    git("checkout stable")
    git("pull")
    git("merge master")
    git(["tag", tag])

    git("checkout master")
    git("push --all")
    git("push --tags")

    subprocess.call("python setup.py sdist")

    #
    # Reset version.py to next version-dev
    #

if __name__ == '__main__':
    main(*sys.argv[1:])
