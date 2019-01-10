# 다양한 functions for handling cards and game.

"""

"""

import re, random

shapes = ['C', 'D', 'H', 'S']


def setMightyJokercall(giruda = 'H'):
	mighty = ['S', 14]
	jokerCall = ['C', 3]
	if giruda == 'S':
		mighty = ['D', 14]
	elif giruda == 'C':
		jokerCall = ['H', 3]
	else:
		pass
	return mighty, jokerCall
mighty, jokerCall = setMightyJokercall()
joker = ['joker', 0]

#test function run
def printA():
	print('print A, to test')

def ruleSetting(playerNum = 5, ruleName = 'defalt'):
    """
    플레이어 수와 룰을 묻는다.
    AI끼리 대전하는 룰인지, 사람이 같이 하는 룰인지 확인.
    """
    playerNumber = playerNum
    if ruleName == 'defalt':
        sets = [playerNumber, ruleName]
        return sets
    elif ruleName == "AIs":
        sets = [playerNumber, ruleName]
        return sets
    else:
        print(str(ruleName) + ', this rule is not ready')

def deckGenerator(ruleName = 'defalt'):
	if ruleName == 'defalt':
		deck = []
		for i in 'C', 'D', 'H', 'S':
		    for k in list(range(2, 15)):
		        deck.append([i,k])
		deck.append(['joker', 0])
		return deck
		# random.shuffle(deck)
	else:
		print(str(ruleName) + ', this rule is not ready')	

def shapeCounter(hand, shape = "all"):
    """
    'hand' is a list of cards, card is something like ["S", 2].
    when 'shape' is "all", return is ['C', 'D', 'H', 'S', mighty, joker]
    if 'shape' is one of ['C', 'D', 'H', 'S'], it return number of that shape.
    """
    # 딸마가 있다는건 마이티랑 같은 모양이 시작카드일 때 그모양이 마이티뿐이면 그거 낸다는거지?
    # 근데 선카가 다른 카드여도 마이티는 낼 수 있는건가? 그치?
    # 낼 수 있는 카드는 [0:3] 중에 1 이상인것, 그리고 마이티, 그리고 조커.
    shapes = [0,0,0,0,0,0]
    for i in range(len(hand)):
        if hand[i][0] == 'C':
            shapes[0] += 1
        elif hand[i][0] == 'D':
            shapes[1] += 1
        elif hand[i][0] == 'H':
            shapes[2] += 1
        elif hand[i][0] == 'S':
            shapes[3] += 1
        if hand[i] == mighty: 
            shapes[4] += 1
        if hand[i] == joker:
            shapes[5] += 1
    if shape == 'all':
        return shapes
    elif shape == 'C':
        return shapes[0]
    elif shape == 'D':
        return shapes[1]
    elif shape == 'H':
        return shapes[2]
    elif shape == 'S':
        return shapes[3]
    else: print('input error!!!')

def shapeCollector(hand, shape):
    result = []
    for i in hand:
        if i[0] == shape: result += [i]
#     print(result)
    return result

def numCounter(hand, num):
    result = 0
    for i in hand:
        if i[1] == num: result += 1
    return result


#set mighty and jokercall from giruda


def handout(players, deck, grave): #hand out cards to AI player
    random.shuffle(deck)
    for i in range(len(players)):
    	# global players[i].hand
        players[i].hand = deck[i*10 + 0:i*10 + 10]
#         print(players[i].hand)
    grave = deck[len(players)*10:]
    return grave
    
def dealCount(playersHand):
    count = 0
    for j in range(10):
        if int(playersHand[j][1]) >=10: 
            count += 1
            if playersHand[j] == ['S', 14]: count -= 2 # mighty 면 점수 -1
        if playersHand[j] == ['joker', 0]: count -= 1 # joker는 -1
#     print(count)
    return count

def roundTrun(turn, startPosition): #이 함수는 아래 함수로 대체될것 같다... 
    a = list(range(len(turn)))
    for i in range(len(turn)):
        a[i] = turn[startPosition]
        startPosition += 1
        if startPosition == len(turn):
            startPosition = 0
    return a

def turnSetting(position, turnStart): #턴스타트는 int, turn은 list
    roundTurn = position.copy()
    while turnStart != roundTurn[0]:
        roundTurn.append(roundTurn[0])
        roundTurn.pop(0)
    return roundTurn

def card2bits(cardList):
    bits = ['0'] *53
    bitIndex = 0
    for i in cardList:
        if i[0] == shapes[0]:
            bitIndex += 0
            bitIndex += i[1]-2
        elif i[0] == shapes[1]:
            bitIndex += 13
            bitIndex += i[1]-2
        elif i[0] == shapes[2]:
            bitIndex += 26
            bitIndex += i[1]-2
        elif i[0] == shapes[3]:
            bitIndex += 39
            bitIndex += i[1]-2
        elif i[0] == 'joker':
            bitIndex = 52
        else: 
            print('!! Error card is in this list !!')
            break
        bits[bitIndex] += 1
    return bits


def roundWin(roundCards, mighty, giruda, jokerCall, validJoker): # validJoker: 첫턴0, 중간턴1, 끝턴0
    calculateScore = 0
    for i in range(len(roundCards)):
        if roundCards[i][1] >= 10:
            calculateScore += 1 #해당라운드의 점수지롱.
    if mighty in roundCards:
        return roundCards.index(mighty), calculateScore
    elif (joker in roundCards) and (roundCards[0] != jokerCall) and (validJoker == 1) :
        return roundCards.index(joker), calculateScore
    elif giruda != 'noGiru' : 
        #이제부턴 마이티도 조커도 없으니 기루다 싸움이다. 근데 기루다가 있는지 먼저 물어보는게 예의지.
        if shapeCounter(roundCards, giruda) > 0: # 기루다가 라운드 카드중에 나왔을 때
            giruSet = shapeCollector(roundCards, giruda)
            maxCount = 0
            winCard = []
            for i in giruSet:
                if i[1] > maxCount:
                    maxCount = i[1]
                    winCard = i
            return roundCards.index(winCard), calculateScore
        else: #기루다 없어
            sunSet = shapeCollector(roundCards, roundCards[0][0]) #선 카드 모음
            maxCount = 0
            winCard = []
            for i in sunSet:
                if i[1] > maxCount:
                    maxCount = i[1]
                    winCard = i
            return roundCards.index(winCard), calculateScore
    else: # 노기루여?
        sunSet = shapeCollector(roundCards, roundCards[0][0]) #선 카드 모음
        maxCount = 0
        winCard = []
        for i in sunSet:
            if i[1] > maxCount:
                maxCount = i[1]
                winCard = i
        return roundCards.index(winCard), calculateScore

def finalWin(scores, roles):
    """
    input:  scores(list), roles(list)
    output: declarerScore(int), defenderScore(int)
    """
    declarerScore = 0 #여당점수
    defenderScore = 0 #야당점수
    if len(scores) != len(roles):
        print('error Input in finalWin')
    for i in range(len(roles)):
        if roles[i] == 0:
            defenderScore += scores[i]
    declarerScore = 20 - defenderScore # 처음에 무덤에 들어간 점카도 여당이 먹은거니까
    return declarerScore, defenderScore