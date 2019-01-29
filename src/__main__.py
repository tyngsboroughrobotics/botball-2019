#!/usr/bin/env python2

import sys; sys.path.append('/home/root/Documents/KISS/Default User/ths-botball-2019/')
try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

from helpers.functions import print_botball_logo
from game.follow_object import follow_object

print_botball_logo()
follow_object()
