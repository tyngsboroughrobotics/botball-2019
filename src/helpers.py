try:
    from __wallaby_local import * # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    from wallaby import * # so it works on actual robot

def print_botball_logo():
  """Prints a cool-looking Botball ASCII-art logo to the console!
  """

  print "    ____  ____  __________  ___    __    __  "
  print "   / __ )/ __ \\/_  __/ __ )/   |  / /   / / "
  print "  / __  / / / / / / / __  / /| | / /   / /   "
  print " / /_/ / /_/ / / / / /_/ / ___ |/ /___/ /___ "
  print "/_____/\\____/ /_/ /_____/_/  |_/_____/_____/"
  print "============================================\n"

def map(x, in_min, in_max, out_min, out_max):
  """Maps a number from one range to another.
  
  Arguments:
    x {number} -- The number to map.
    in_min {number} -- The min of the first range.
    in_max {number} -- The max of the first range.
    out_min {number} -- The min of the new range.
    out_max {number} -- The max of the new range.
  
  Returns:
    number -- The mapped number.
  """

  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def msleep(ms):
  """Blocks for the desired amount of milliseconds.
  
  Arguments:
    ms {int} -- The number of milliseconds to sleep.
  """

  from time import sleep
  sleep(ms / 1000)
