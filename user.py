# import
import gamefunctions as gf

mighty = ['S', 14]
joker = ['joker', 0]
shapes = ['C', 'D', 'H', 'S']

class User(object):
    
    def __init__(self):
        """
            이건 프로그램을 사용하는 게이머(닝겐)입니답.
        """
        self.name = "ningen"
        self.hand = []
        self.field = []
        self.score = 0  
        self.role = [0,0]    #00:야당, 01:프랜드, 10: 주공
        self.grave = []
#         함수명은 동일하게 가자, 내부 구현만 다르면 될것 같아

###    이하 복붙 영역    ###
    def setMighty(self,giruda):
        if giruda == 'S':
            mighty = ['D', 14]
        else: mighty = ['S', 14]
        return mighty
    
    def pledge(self, others): #공약... 쉽지 않겠는걸
        biddingYesNo = ""
        myBidding = ["",0]
        biddingYesNo = input(self.name + ', will you pledge? (y/n) ')
        while not(biddingYesNo in ['y', 'n']):
            biddingYesNo = input('try again, will you pledge? (y/n) ')
        if biddingYesNo == "n":
            return myBidding
        else:
            if others[0] != 'noGiru':
                minBidding = others[1] + 1
            else:
                minBidding = others[1] + 2
            myBidding[0] = input('choose shape, one of ' + str(shapes) + " or 'noGiru' :")
            while not(myBidding[0] in shapes) and not(myBidding[0] == 'noGiru'):
                myBidding[0] = input('try again, one of ' + str(shapes) + " or 'noGiru' :")


            if myBidding[0] != 'noGiru':
                myBidding[1] = int(input('Choose number 비트윈 ' + str(minBidding) + '~20 : '))
                while myBidding[1] < minBidding or myBidding[1] > 20:
                    myBidding[1] = int(input('try again, Choose number 비트윈 ' + str(minBidding) + '~20 : '))
            else:
                myBidding[1] = int(input('Choose number 비트윈 ' + str(minBidding - 1) + '~20 : '))
                while myBidding[1] < minBidding-1 or myBidding[1] > 20:
                    myBidding[1] = int(input('try again, Choose number 비트윈 ' + str(minBidding - 1) + '~20 : '))
            print(self.name + ', your bidding is ')
            return myBidding

        #핸드에서 한 카드 종류가 몇개인지
        #핸드에 점카는 몇개인지
        #핸드에 특수카드(마이티(빨마), 조커, 조커콜)는 몇갠지, 어떤 조합인지...
        # print('this is your hand: ' + str(self.hand))
        # while not(oath[0] in ["H","S","C","D","noKiru"]):
        #     oath[0] = input(self.name + ', Pick one of those "H","S","C","D","noKiru" : ')
        #     if not(oath[0] in ["H","S","C","D","noKiru"]): print('Plz choice again')
        # while not(oath[1] in [1,13,14,15,16,17,18,19,20]): #21은 패스
        #     oath[1] = int(input('How many do you pledge? (1 for pass, 13~20 to pledge)'))
        #     if not(oath[1] in [1,13,14,15,16,17,18,19,20]): print('Plz say again')
        # #random.randrange(13,21)
    
    def friendCall(self):
        print(" << 친구고르기 >> ")
        print(self.name + ', This is your hand: ' +str(self.hand))
        userFriend = [" ", 0]
        userPick[0] = input('Choose your friend! say one of ' + str(shapes) + ', or "joker"')
        while not(userFriend[0] in shapes) and not(userFriend[0] == 'joker'):
            userPick[0] = input('try gain. Choose one of ' + str(shapes) + ', or "joker"')
        if userPick[0] == "joker":
            return joker
        else:
            userPick[1] = int(input('Choose number of 2 ~ 14 (14 for A, 13 for K, ...)'))
            while not(userFriend[1] in [2,3,4,5,6,7,8,9,10,11,12,13,14]):
                userPick[1] = int(input('try again. one of 2 ~ 14 (14 for A, 13 for K, ...)'))
            return userPick

    def possibleOptions(self, turnShape, mighty): 
        if turnShape == 'all':
            count = 0
        else:
            count = gf.shapeCounter(self.hand, turnShape)
        if count > 0:
            options = gf.shapeCollector(self.hand, turnShape)
            if mighty in self.hand:
                options += mighty
            if joker in self.hand:
                options += joker
        else:
            options = self.hand.copy()
        return options

    def sayShape(self):
        # when startCard is 'joker', then first player needs to say shape.
        return 'S'

    def pickCard(self, bits, turnShape, mighty):        #젤어렵겠다... AI 구현 with TF
#         print('카드 고르기')
#     self.hand[random.randrange(0,len(self.hand))]
#상황에 따라 보기를 주고 그 중에 고르라고 하는게 맞을것 같다. pickable card.
        if len(self.hand) <= 0:
            print('noCardError')
            return False
        
        #선 이 뭔지 파악(선이 뭔지 인자로 받아야) (혹은 내가 선인지)
        #선 과 같은 카드 있는지 확인 (내 핸드는 내가 알지 self.hand 임)
        #선 과 같은 카드 있으면 그 중에 선택(선, 마이티, 조커)
        #선 과 같은 카드 없으면 모든 핸드중에 선택
        
        print(self.name + ', This is your hand: ' +str(self.hand))
        userPick = " "
        while not(userPick in self.hand):
            print("your hand is 0 ~ " + str(len(self.hand) - 1))
            userPick = int(input('Witch card will you choose? Tell me index  '))
            # if not(userPick in self.hand): print('Plz choice again')
            if userPick > len(self.hand) - 1: print('Plz choice again')
            else: userPick = self.hand[userPick]
        self.hand.remove(userPick)
        return userPick
        
    def jokerCallPick(self, bits, turnShape, mighty):
        if joker in self.hand:
            self.hand.remove(joker)
            return joker
        else:
            return self.pickCard(bits, turnShape, mighty)



