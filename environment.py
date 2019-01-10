# import 
import re, random
import gamefunctions as gf

joker = ['joker', 0]
shapes = ['C', 'D', 'H', 'S']

class Environment(object):
    """
        나는
        모든 플레이어에게 보이는 상황이다.
         - 그래서 grave 처럼 Declarer와 Defender에게 보이는 것이 다른 정보는 저장하지 않는다.
        이 상황은 Player의 pickCard method에 불려가게 될 것이므로 상황을 card 이름과 bit로 둘 다 저장하고 있는다.

        모든 플레이어에게 같은 것
            - score
            - 어느 자리가 여당인지
            - roundRecord
            - roundNumber
            - roundLead (선)
            - 몇 번 플레이어가 어디인지
            - 어느 자리가 선인지
            - giruda
            - 

        플레이어마다 다른 것
            - hand
            - grave(king과 나머지가 다르다)
            - 

    """

    def __init__(self):
        """
		for the tf input, it is needed to fix input data form.

		self.role       [53bit]
		grave           [53bit]
		roundRecord     [ 53bit * 4 ]
		roundNumber     [ 10bit ]
		hand            [53bit]
		other's shape   [4bit * 4]                      (C,D,H,S)

		pledge          [4bit(shape) + int(num) ]
		location        [4bit]                          (내 기준 자리임. 내 다음에 여당 있으면 [1,0,0,0]. 여당 둘이면 [1,0,1,0])
		                                                (0끼리는 구분 안되어도 됨. 근데 의심을 하려면 뭔가 구분자가 필요할까? 모르겠다..)
		                + [4bit]                        (start of each round, 시작사람이 1, 내가 시작이면 [0,0,0,0])
		score           [4 ints]
		"""
        self.rule = "defalt"
        self.playerNumber = 5

        self.role = [0,0,0,0,0]         # 밝혀진 것만, 처음에 Declarer, 게임중에 Friend
        self.scores = [0,0,0,0,0]       #턴 넘버에 매칭
        self.locations = [0,1,2,3,4]    #players[?]에 넣을 숫자.
        self.field = []   #필드에 나와있는 숫자

        self.roundShape = 'all'
        self.roundTrun = []

        self.giruda = ""
        self.bidding = 0

        self.mighty = ['S', 14]
        self.jokerCall = ['C',3]

        self.roundCards = list(range(0,self.playerNumber))

        self.bits = list(range(0,478))                  # 비트화된 정보 for tf
        """
            bits    0~4     role
                    5~9     giruda      [c,d,h,s,nogiru]
                    10~14   scores
                    15~19   locations # 이건 아닌가... 각자가 다른 입장일텐데 위치에 대해선.
                    20~24   roundStart
                    ...
        """

#         self.             #의심도(?) 누가누가 프랜드같은지... 추론은 어케 해야 하냐
# 피하고 싶은 상황: 눈앞에서 뻔히 프랜드같은놈이 주공한테 점수 퍼주는데 프랜드인지 모르고 걔한테 점수 주는 짓.
#                  혹은 야당끼리 협력 못하고 모두 서로를 프랜드로 보고 자기 점수만 늘리려고 하는 전략.
# 피하기 위한 정보: 누가 무슨 카드를 냈나. 그 때 상황이 (필드가) 어땠나.    
    
    def setGiruda(self,giruda):
        self.giruda = giruda
        if giruda == 'S':
            self.mighty = ['D', 14]
        elif giruda == 'C':
            self.jokerCall = ['H',3]
        if giruda in shapes:
            giruIndex = shapes.index(giruda)
            bits[5+giruIndex] = 1 # 5~9: giruda
        else:
            bits[9] = 1

    def setDeclarer(self,kingNo):
        self.role[kingNo] = 1

    def setFriend(self,friendNo):
        self.role[friendNo] = 1

    def initialize(self): #단순히 모든 변수 다 초기처럼 똑같이 맞추면 되겠군.
        self.rule = "defalt"
        self.playerNumber = 5

        self.role = [0,0,0,0,0]         # 밝혀진 것만, 처음에 Declarer, 게임중에 Friend
        self.scores = [0,0,0,0,0]       #턴 넘버에 매칭
        self.locations = [0,1,2,3,4]    #players[?]에 넣을 숫자.
        self.field = []   #필드에 나와있는 숫자

        self.roundShape = 'all'
        self.roundTrun = []

        self.giruda = ""
        self.bidding = 0

        self.mighty = ['S', 14]
        self.jokerCall = ['C',3]

        self.roundCards = list(range(0,self.playerNumber))

        self.bits = list(range(0,478))