#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Testing with Nose
=================

This test runner uses Nose for test discovery and running. It uses the argument
spec of Nose, but with some options pre-set. To begin with, make sure you have
Nose installed, e.g.:

    $ sudo easy_install nose

For daily test runs, use:

    $ ./run_tests.py

If you supply attributes, the default ones defined in ``DEFAULT_ATTRS`` will be
ignored. So to run e.g. all tests marked ``slowtest`` or ``non_standard_dep``,
do:

    $ ./run_tests.py -a slowtest,non_standard_dep

See <http://code.google.com/p/python-nose/> for furher details. An excellent
article is also available at <http://ivory.idyll.org/articles/nose-intro.html>.

Note that this is just a convenience script. You can use ``nosetests`` directly
if it's on $PATH, with the difference that you have to supply the options
pre-set here manually.

Coverage
========

If ``coverage.py`` is placed in $PYTHONPATH, it can be used to create coverage
information (using the built-in coverage plugin of Nose) if the default
option "--with-coverage" is supplied (which also enables some additional
coverage options).

See <http://nedbatchelder.com/code/modules/coverage.html> for details.

"""


NOSE_ARGS = [
        '--where=./',
        '--with-doctest',
        #'--doctest-extension=.doctest',
        #'--doctest-tests',
        #'--with-coverage',
        #'--enable-cover',
        #'--enable-audit',
        #'--extra-include=rdfextras',
        #'--source-folder=rdfextras',
        #'--trim-errors',
        #'--with-EARL',
        #'--with-xunit',
    ]

COVERAGE_EXTRA_ARGS = [
        '--cover-package=rdfextras',
        '--cover-inclusive',
        '--cover-html',
        '--cover-html-dir=coverage',
    ]

DEFAULT_ATTRS = ['!known_issue', '!performancetest', '!storetest'] # ['!known_issue', '!sparql']

DEFAULT_DIRS = ['test', 'rdfextras']


if __name__ == '__main__':

    from sys import argv, exit, stderr
    try: import nose
    except ImportError:
        print("""\
    Requires Nose. Try:

        $ sudo easy_install nose

    Exiting. """, file=stderr); exit(1)


    if '--with-coverage' in argv + NOSE_ARGS:
        try: import coverage
        except ImportError:
            print("No coverage module found, skipping code coverage.", file=stderr)
            argv.remove('--with-coverage')
        else:
            NOSE_ARGS += COVERAGE_EXTRA_ARGS


    if True not in [a.startswith('-a') or a.startswith('--attr=') for a in argv]:
        argv.append('--attr=' + ','.join(DEFAULT_ATTRS))

    if not [a for a in argv[1:] if not a.startswith('-')]:
        argv += DEFAULT_DIRS # since nose doesn't look here by default..


    finalArgs = NOSE_ARGS + argv
    print("Running nose with:", " ".join(finalArgs[1:]))
    nose.run_exit(argv=finalArgs)
