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

# Score types
#
# Fill this in as we develop our strategy. Example:
#
#     POM_PICKED_UP = 3
#     score_add(POM_PICKED_UP)
#