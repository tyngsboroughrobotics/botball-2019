#!/usr/bin/env python2

try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from helpers.functions import print_botball_logo
from game import test as game_test

print_botball_logo()
