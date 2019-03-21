#!/usr/bin/env python2

import sys; sys.path.append('/home/root/Documents/KISS/Default User/ths-botball-2019/')
try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from helpers.functions import print_botball_logo
from game import game
# from game import game_create

print_botball_logo()
game.run() # choose `game` or `game_create` to run
