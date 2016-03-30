#!/usr/bin/env python
"""
NAME: xxx
=========

DESCRIPTION
===========

INSTALLATION
============

USAGE
=====

VERSION HISTORY
===============

0.1.0   xxxx/xx/xx    Initial version.

LICENCE
=======
2015, copyright Sebastian Schmeier (s.schmeier@gmail.com), http://sschmeier.com

template version: 1.1 (2015/12/10)
"""
__version__='0.1.0'
__date__='xxxx/xx/xx'
__email__='s.schmeier@gmail.com'
__author__='Sebastian Schmeier'
import sys, os, os.path, argparse, csv, collections, gzip, bz2, zipfile, time
import glob, re

# When piping stdout into head python raises an exception
# Ignore SIG_PIPE and don't throw exceptions on it...
# (http://docs.python.org/library/signal.html)
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def parse_cmdline():
    
    ## parse cmd-line -----------------------------------------------------------
    sDescription = 'Get app ready. Replace "testapp" in all files with "APPNAME".' 
    sVersion='version %s, date %s' %(__version__,__date__)
    sEpilog = 'Copyright %s (%s)' %(__author__, __email__)

    oParser = argparse.ArgumentParser(description=sDescription,
                                      version=sVersion,
                                      epilog=sEpilog)
    oParser.add_argument('sAppName',
                         metavar='APPNAME',
                         help='Your app name that replaces "testapp"')
    
    oArgs = oParser.parse_args()
    return oArgs, oParser

def load_file(s):
    """ LOADING FILES """
    if s in ['-', 'stdin']:
        oF = sys.stdin
    elif s.split('.')[-1] == 'gz':
        oF = gzip.open(s)
    elif s.split('.')[-1] == 'bz2':
        oF = bz2.BZFile(s)
    elif s.split('.')[-1] == 'zip':
        oF = zipfile.Zipfile(s)
    else:
        oF = open(s)
    return oF

def repl(sApp, sFile):
    oF = load_file(sFile)
    sNew = re.sub('testapp', sApp, oF.read())
    oF.close()
    oF = open(sFile,'w')
    oF.write('%s\n'%sNew)
    oF.close()

def main():
    oArgs, oParser = parse_cmdline()

    sApp = oArgs.sAppName

    # renmame dirs
    try:
        os.rename('static/testapp', 'static/%s'%sApp)
    except:
        pass

    try:
        os.rename('templates/testapp', 'templates/%s'%sApp)
    except:
        pass

    # replace testapp in files
    repl(sApp, 'urls.py')
    repl(sApp, 'views.py')
    repl(sApp, 'apps.py')
    aF = glob.glob('templates/%s/*.html'%sApp)
    for sF in aF:
        repl(sApp,sF)
   
    return
        
if __name__ == '__main__':
    sys.exit(main())


