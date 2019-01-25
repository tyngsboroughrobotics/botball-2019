try:
    from src import __wallaby_local as w # for VSCode support
except ImportError: 
    import imp; wallaby = imp.load_source('wallaby', '/usr/lib/wallaby.py')
    import wallaby as w # so it works on actual robot

__CURRENT_SCORE = 0

def score_add(amount):
    """Adds the `amount` to the current score and returns
    the score.
    """

    global __CURRENT_SCORE
    __CURRENT_SCORE += amount 
    return __CURRENT_SCORE

def score_subtract(amount):
    """Subtracts the `amount` from the current score and
    returns the score.
    """

    global __CURRENT_SCORE
    __CURRENT_SCORE -= amount 
    return __CURRENT_SCORE

def score():
    """Returns the current score.
    """


    return __CURRENT_SCORE

def print_score():
    """Prints the current score to the console.
    """
    
    print '**** Current score: ' + str(__CURRENT_SCORE) + ' ****'
