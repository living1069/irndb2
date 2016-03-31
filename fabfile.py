# TODO: You need to replace TESTAPP with the correct reponame 
from __future__ import with_statement
from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm

def git(branch="develop", ghpages=False, version=None):
    """
    branch: the branch that should be merged into master.
    ghpages: if set to true, merge master to gh-pages branch and push
    """
    local("git add -u && git commit")
    local("git co master")
    local("git merge %s --no-ff" %branch)
    # add tag?
    with settings(warn_only=True):
        if version:
            local('git tag -a %s'%version)
    # push to origin
    local("git push")

    if ghpages:
        local("git co gh-pages")
        local("git merge master")
        local("git push origin gh-pages")
        
    # checkout develop branch
    local("git co %s"%branch)
