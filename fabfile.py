# TODO: You need to replace TESTAPP with the correct reponame 
from __future__ import with_statement
from fabric.api import run, settings, puts, cd, lcd, local, hosts
from fabric.colors import yellow, red
import os.path

#-- EDIT
HOST = 'seb@vm010944'  # production server
REMOTE_BASE_DIR = '/webapps/seb_django/sebio/'  # DJANGO BASE
REMOTE_ERR_FILE = '/webapps/seb_django/logs/00update_irndb2_git.err'
REMOTE_LOG_FILE = '/webapps/seb_django/logs/00update_irndb2_git.log'
REPO_NAME = 'irndb2'
REPO_URL = 'git@github.com:sschmeier/irndb2.git'


@hosts('%s' % HOST) # only for deploy to production
def logs():
    """ Reading remote log files and print to stdout. """
    puts(yellow("[Reading log-file]"))
    run("cat %s" % REMOTE_ERR_FILE)
    run("cat %s" % REMOTE_LOG_FILE)


@hosts('%s' % HOST) # only for deploy to production
def deploy():
    """ Deploy project to remote hosts. """
    remote_dir = os.path.abspath(os.path.join(REMOTE_BASE_DIR, REPO_NAME))
    
    with settings(warn_only=True):
        if run("test -d %s" % (remote_dir)).failed:
            puts(red("[Repo %s does not exist on remote at: %s]" % (REPO_NAME, remote_dir)))
            with cd(REMOTE_BASE_DIR):
                run("git clone %s %s" % (REPO_URL, REPO_NAME))

    puts(yellow("[Write logs]"))
    run("echo '-----------------------------' > %s" % REMOTE_ERR_FILE)
    run("echo `date` >> %s" % REMOTE_ERR_FILE)
    run("echo '-----------------------------' >> %s" % REMOTE_ERR_FILE)
    run("echo '-----------------------------' > %s" % REMOTE_LOG_FILE)
    run("echo `date` >> %s" % REMOTE_LOG_FILE)
    run("echo '-----------------------------' >> %s" % REMOTE_LOG_FILE)

    puts(yellow("[Update repo: %s]" % REPO_NAME))
    with cd(remote_dir):
        run("git pull origin master >> %s 2>> %s" %
            (REMOTE_LOG_FILE, REMOTE_ERR_FILE))

    # reminder new static files
    puts(yellow('Do not forget to run collect staticfiles on DJANGO server.'))


def github(branch, version=None):
    """Execute local git cheackout master, merge branch into master and push to github.

    Keyword arguments:
    branch -- the branch that should be merged into master.
    version -- new version/tag number requested this will create a repo tag.

    Usage:
    fab github:branch='new_feature',version='v1.2.5'
    """

    # co master and merge
    puts(yellow("[Checkout master]"))
    local("git checkout master")

    puts(yellow("[Merge branch '%s' into master]"%branch))
    local("git merge %s --no-ff" %branch)

    with settings(warn_only=True):
        if version:
            puts(yellow("[Bump version: %s]"%version))

            # bump version number: project specific
            local("sed -i -- 's/v.\..\../%s/g' templates/%s/base.html" %(version, REPO_NAME))
            local("git add templates/%s/base.html"%REPO_NAME)

            local('git commit -m "Bumped to %s"' %version)

            # add tag
            puts(yellow("[Tag new version: %s]"%version))
            local('git tag -a %s'%version)

    # deploy
    puts(yellow("[Deploy to origin]"))
    local("git push origin master")
    puts(yellow("[Do not forgot to deploy to production]"))
