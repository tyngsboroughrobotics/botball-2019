import sys; sys.path.append('/home/root/Documents/KISS/Default User/ths-botball-2019/')
try:
    from src import * # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    from wallaby import * # so it works on actual robot

