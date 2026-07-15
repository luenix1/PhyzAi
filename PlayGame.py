import Variables

def haveCard(goal, cards):
    for i in cards:
        if goal == i:
            return "has card"
    return "go fish!"

def askForCard():

    #"score" for each card, highest score is gonna be asked for
    scores = [0] * 13
    highestScore = 0
    highestCard = "none"
    n = 0
    
    # create number in play variable for each card
    # 1. ask for the card that has atleast 3 in play and prioritize 4
    # 2. ask for the card you know your opponent has atleast one of
    # 3. ask for the card you have atleast 2 of and prioritize 3
    # 4. ask for the card you have atleast one of
    # 5. ask for random card?
    for i in Variables.Templates.name:
        for cards in Variables.currentCards:
            if i == cards:
                scores[n] += 10
        for cards in Variables.knownCards:
           if i == cards:
                scores[n] += 20
        if scores[n] >= highestScore:
            highestScore = scores[n]
            highestCard = i
        n+=1

    return highestCard