#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re


# Find version. We have to do this because we can't import it in Python 3 until
# its been automatically converted in the setup process.
def find_version(filename):
    _version_re = re.compile(r'__version__ = "(.*)"')
    for line in open(filename):
        version_match = _version_re.match(line)
        if version_match:
            return version_match.group(1)

__version__ = find_version('rdfextras/__init__.py')

config = dict(
    name = 'rdfextras',
    version = __version__,
    description = "RDFExtras provide tools, extra stores and such for RDFLib.",
    author = "Niklas Lindström",
    author_email = "lindstream@gmail.com",
    url = "http://github.com/RDFLib/rdfextras",
    license = "BSD",
    platforms = ["any"],
    classifiers = ["Programming Language :: Python",
                   "License :: OSI Approved :: BSD License",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   "Operating System :: OS Independent",
                   ],
    packages = ['rdfextras',
                'rdfextras.sparql',
                'rdfextras.sparql.results',
                'rdfextras.store',
                'rdfextras.store.FOPLRelationalModel',
                'rdfextras.tools',
                'rdfextras.utils']
)

from setuptools import setup
install_requires = ['rdflib >= 3.2.1', 'pyparsing']


tests_require = install_requires + \
                []

extras_require = { 
    }


config.update(
    entry_points = {
        'console_scripts': [
            'rdfpipe = rdfextras.tools.rdfpipe:main',
            'csv2rdf = rdfextras.tools.csv2rdf:main',
            'rdf2dot = rdfextras.tools.rdf2dot:main',
            'rdfs2dot = rdfextras.tools.rdfs2dot:main',
        ],
        'rdf.plugins.queryprocessor': [
            'sparql = rdfextras.sparql.processor:Processor',
        ],
        'rdf.plugins.queryresult': [
            'sparql = rdfextras.sparql.query:SPARQLQueryResult',
        ],
        'rdf.plugins.resultserializer': [
            'xml = rdfextras.sparql.results.xmlresults:XMLResultSerializer',
            'json = rdfextras.sparql.results.jsonresults:JSONResultSerializer',
        ],
        'rdf.plugins.resultparser': [
            'xml = rdfextras.sparql.results.xmlresults:XMLResultParser',
            'json = rdfextras.sparql.results.jsonresults:JSONResultParser',
        ],
    },
    #namespace_packages = ['rdfextras'], # TODO: really needed?
    install_requires = install_requires,
    tests_require = tests_require,
    extras_require = extras_require 
)
    
setup(**config)

