# Red, Blue, Orange, White
# 3 positions
import re
import random

def filterStates(states, filter, exclude):
    print(filter, exclude)
    pattern = re.compile(filter)

    newStates = set()
    for state in states:
        match = pattern.match(state)
        #print(match)
        if exclude:
            if not match:
                newStates.add(state)
        else:
            if match:
                newStates.add(state)

    print(newStates)
    return newStates

def processAnswer(states, guess, answer):
    numX = answer.count('X')
    numO = answer.count('O')
    print('')

    if numX == 1:
        #eliminate all states that don't contain only one color in the guess position
        filter =  guess[0]+'[^'+guess[1]+'][^'+guess[2]+']'
        filter += '|[^'+guess[0]+']'+guess[1]+'[^'+guess[2]+']'
        filter += '|[^'+guess[0]+'][^'+guess[1]+']'+guess[2]
        states = filterStates(states, filter, False)
    elif numX == 2:
        #eliminate all states that don't contain only two colors in the guess position
        filter =  guess[0]+guess[1]+'[^'+guess[2]+']'
        filter += '|'+guess[0]+'[^'+guess[1]+']'+guess[2]
        filter += '|[^'+guess[0]+']'+guess[1]+guess[2]
        states = filterStates(states, filter, False)
    elif numX == 3:
        #solution found!
        states = filterStates(states, guess, False)

    if numO+numX == 0:
        #eliminate all colors in the guess
        filter =  '.*'+guess[0]+'+.*'
        filter += '|.*'+guess[1]+'+.*'
        filter += '|.*'+guess[2]+'+.*'
        states = filterStates(states, filter, True)
    elif numO+numX == 1:
        # eliminate all states with more than one color in common with the guess
        None
    elif numO+numX == 2:
        # eliminate all states with more than two colors in common with the guess
        None
    elif numO+numX == 3:
        if numX == 0:
            # eliminate all states with colors in the guess positions
            filter =  guess[0]+'..'
            filter += '|.'+guess[1]+'.'
            filter += '|..'+guess[2]
            states = filterStates(states, filter, True)
        # eliminate all states with colors not in the guess
        filter =  '['+guess[0]+guess[1]+guess[2]+']'
        filter += '['+guess[0]+guess[1]+guess[2]+']'
        filter += '['+guess[0]+guess[1]+guess[2]+']'
        states = filterStates(states, filter, False)

    print('')
    return states;

colors = ['R', 'B', 'O', 'W']
states = set()
for c1 in colors:
    for c2 in colors:
        for c3 in colors:
            states.add(c1+c2+c3)

while (len(states) != 1):
    if len(states) == 0:
        print('No possible codes left! Answer carefully!')
        exit()
    # select a possible state as a guess
    guess = random.choice(tuple(states))
    print('Guess:',guess)
    answer = input('Answer: ')
    states = processAnswer(states, guess, answer)

print('Code is',next(iter(states), None))
