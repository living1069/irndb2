# TODO: You need to replace TESTAPP with the correct reponame 
from __future__ import with_statement
from fabric.api import *
from fabric.colors import *
from fabric.contrib.console import confirm

@hosts('seb@vm010865.massey.ac.nz', 'seb@vm010944.massey.ac.nz') # only for deploy
def logs():
    err_file = '/webapps/seb_django/logs/00update_TESTAPP_git.err'
    log_file = '/webapps/seb_django/logs/00update_TESTAPP_git.log'
    puts(yellow("[Reading log-file]"))
    errout = run("cat %s"%err_file)
    logout = run("cat %s"%log_file)

@hosts('seb@vm010865.massey.ac.nz', 'seb@vm010944.massey.ac.nz') # only for deploy
def deploy():
    # TODO: Needs adjustment: acctual reponame
    app_dir = '/webapps/seb_django/TESTAPP'
    err_file = '/webapps/seb_django/logs/00update_TESTAPP_git.err'
    log_file = '/webapps/seb_django/logs/00update_TESTAPP_git.log'
        
    with settings(warn_only=True):
        if run("test -d %s" % www_dir).failed:
            # TODO: Needs adjustment, change repo link to acctual repo, not the template
            run("git clone git@gitlab.com:s-schmeier/TESTAPP.git %s" % app_dir)
            run("git submodule init")

    puts(yellow("[Activate env]"))
    run('source ~/bin/activate')
    puts(yellow("[Write logs]"))
    run("echo '-----------------------------' > %s"%err_file)    
    run("echo `date` >> %s"%err_file)
    run("echo '-----------------------------' >> %s"%err_file)
    run("echo '-----------------------------' > %s"%log_file)    
    run("echo `date` >> %s"%log_file)
    run("echo '-----------------------------' >> %s"%log_file)

    puts(yellow("[Update TESTAPP]"))
    with cd(app_dir):
        run("git pull >> %s 2>> %s"%(log_file, err_file))
        run("git submodule update --remote --merge >> %s 2>> %s"%(log_file, err_file))

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
