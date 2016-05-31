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
        run("git pull >> %s 2>> %s" %
            (REMOTE_LOG_FILE, REMOTE_ERR_FILE))

    # reminder new static files
    puts(yellow('Do not forget to run collect staticfiles on DJANGO server.'))

