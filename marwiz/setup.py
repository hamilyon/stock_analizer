#!/usr/bin/env python

from setuptools import setup, find_packages
from market import __version__


setup(name="marketwizard",
    version=__version__,
    author="AlgoMarkets LLC",
    author_email="marketwizard@algomarkets.ru",
    url='http://marketwizard.algomarkets.ru/',
    description = "MarketWizard is a framework for rapid development trading robots and backtesting trading strategies.",
    download_url = "http://marketwizard.algomarkets.ru/downloads/marketwizard-%s.tar.gz".format(__version__),
    packages = find_packages(exclude=["tests"]),
    classifiers = ["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Financial and Insurance Industry",
                   "License :: OSI Approved :: BSD License",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Office/Business :: Financial :: Accounting",
                   "Topic :: Office/Business :: Financial :: Investment",
                   "Topic :: Software Development :: Libraries :: Application Frameworks",
                   "Topic :: Software Development :: Code Generators",
                   "Topic :: Software Development :: Embedded Systems",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
    )

