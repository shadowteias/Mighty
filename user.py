# import

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
#         함수명은 동일하게 가자, 내부 구현만 다르면 될것 같아

###    이하 복붙 영역    ###
    def friendCall(self):
        print("친구고르기")
    
    def pledge(self, others): #공약... 쉽지 않겠는걸
        oath = ["",0]
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
        return oath
    
    def pickCard(self):        #젤어렵겠다... AI 구현 with TF
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
        
        print('This is your hand: ' +self.hand)
        userPick = " "
        while not(userPick in self.hand):
            userPick = input('Your choice: ')
            if not(userPick in self.hand): print('Plz choice again')
        return userPick
        