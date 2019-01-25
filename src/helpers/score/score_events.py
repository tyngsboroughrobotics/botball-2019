try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

# Score events
#
# Fill this in as we develop our strategy. Example:
#
#     POM_PICKED_UP = 3
#     score_add(POM_PICKED_UP)
#