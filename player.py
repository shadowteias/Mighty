# import 
import re, random
import gamefunctions as gf

# 변수 정의
mighty = ['S', 14]
joker = ['joker', 0]
# giruda
# grave
shapes = ['C', 'D', 'H', 'S']

#게임 플레이 과정에서 정해진 기루다, 마이티 같은거 어케 자동으로 못 가져오나... 인풋으로 안넣고도.

class Player(object):
    """
        나는
        핸드가 있어야 하고
        내 점수카드를 인식해야 하고
        남의 카드 낸걸 카운팅 해야 하고
        누가 점수카드를 몇 장 가졌는지 알아야 하고
        지금이 몇 라운드인지 알아야 하고
        기루나 조커콜이나 마이티 카드를 알아야 하고
        조커나 마이티가 나왔는지 알아야 하고
        카드를 선택해서 낼 줄 알아야 하고
        남이 어떤 카드가 소진됬는지 알아야 하고
        자기 자리를 기준으로 주공이 어딨는지, 프랜드가 어딨는지 포지션(자리)를 알아야 하고
        
        공약을 할 줄 알아야 하고
        프랜드를 선택할줄 알아야 하고
        
        야당/주공/프랜드일때 플레이하는법을 알아야 하고
        이에 따라 카드를 선택해서 낼 줄 알아야 하고
        내 정체가 드러났는지 알아야 하고
        
        어쩌면
        내 누적 점수를 기억해야 할 수도 있고
        세이브/로드로 불러오기가 가능해야 할지도
        
        나는 아래 정보로 공약을 하고,
            내 핸드, 남의 공약
        
        나는 아래 정보로 카드를 내요.
            역할(주공,프랜드,야당), 핸드, 자리(누가누가옆에앉았나)/차례, 라운드카드, 
            몇번째턴인지, 프랜드가 밝혀졌는지, 내가 프랜드인데 그게 드러났는지(혹은 의심받는지...이건 어케 구현하냐;;),
            그동안 나온 히스토리(grave를 기억하면 되겠군), 누가 무슨 카드가 떨어졌는지(남의 카드를 의심할 줄 알아야 하나?)
            
    """
    
    def __init__(self):
        """
            이건 AI플레이어잆니다
        """
        self.name = ""    #이름. 예를 들어 윤희
        self.hand = []    #내가 가진 카드
        self.field = []   #내 현재 점수카드
        self.score = 0    #내 현재 점수
        self.role = [0,0]     #00:야당, 01:프랜드, 10: 주공
        self.grave = []
#         self.             #의심도(?) 누가누가 프랜드같은지... 추론은 어케 해야 하냐
# 피하고 싶은 상황: 눈앞에서 뻔히 프랜드같은놈이 주공한테 점수 퍼주는데 프랜드인지 모르고 걔한테 점수 주는 짓.
#                  혹은 야당끼리 협력 못하고 모두 서로를 프랜드로 보고 자기 점수만 늘리려고 하는 전략.
# 피하기 위한 정보: 누가 무슨 카드를 냈나. 그 때 상황이 (필드가) 어땠나.    
    
    def setMighty(self,giruda):
        if giruda == 'S':
            mighty = ['D', 14]
        else: mighty = ['S', 14]
        return mighty

    
    def pledge(self, others): #공약... 쉽지 않겠는걸
        oath = ["",1]
        #핸드에서 한 카드 종류가 몇개인지
        #핸드에 점카는 몇개인지
        #핸드에 특수카드(마이티(빨마), 조커, 조커콜)는 몇갠지, 어떤 조합인지...
        a = gf.shapeCounter(self.hand)
        b = max(a)
        maxIndex1 = a.index(b)
        if a.count(b) == 3 and gf.dealCount(self.hand) >5 and others[1] <17:
            oath[0] = "noGiru"
            if others[1] < 5: oath[1] = 12
            elif others[0] != 'noGiru':
                oath[1] = others[1]
            else:
                oath[1] = others[1]+1
        elif a.count(b) == 2: # 33 또는 44 또는 55다, 
            maxIndex2 = a[maxIndex1+1:].index(b) + maxIndex1 + 1
            shapeCards1 = gf.shapeCollector(self.hand, shapes[maxIndex1])
            shapeCards2 = gf.shapeCollector(self.hand, shapes[maxIndex2])
            # print(shapeCards1)
            # print(shapeCards2)
            # print(b)
            if b in [3,4] and gf.dealCount(self.hand) > 6:
                oath[0] = "noGiru"
                if others[1] < 5: oath[1] = 12
                elif others[0] != 'noGiru':
                    oath[1] = others[1]
                else:
                    oath[1] = others[1]+1
            else: #b = 5임, 두 모양으로 5개씩 <Error!!!!> b==4인 경우도 있구나! 
                sum1 = 0
                sum2 = 0
                for i in range(b):
                    sum1 += shapeCards1[i][1]
                    sum2 += shapeCards2[i][1]
                if sum1 >= sum2 and int((sum1+6)/4) > others[1]:
                    oath[0] = shapes[maxIndex1]
                    if others[0] != 'noGiru': oath[1] = others[1] + 1
                    else: oath[1] = others[1] + 2
                elif int((sum2+6)/4) > others[1]:
                    oath[0] = shapes[maxIndex2]
                    if others[0] != 'noGiru': oath[1] = others[1] + 1
                    else: oath[1] = others[1] + 2
                else: pass
        elif b >= 5: # 최고 많은 카드가 한 모양일때. 아마 대다수의 경우. 6,7,8,9,10이 가능하다. 졸라많네.
            sum1 = 0
            shapeCards1 = gf.shapeCollector(self.hand, shapes[maxIndex1])
            for i in range(b):
                sum1 += shapeCards1[i][1]
            if int((sum1+6)/4) > others[1]:
                oath[0] = shapes[maxIndex1]
                if others[0] != 'noGiru': oath[1] = others[1] + 1
                else: oath[1] = others[1] + 2
            else: pass
        else: pass
        return oath
        
#         if max(shapeCounter(self.hand)) >=4:
#             if shapeCounter(self.hand).index(max(shapeCounter(self.hand)))
#         oath[0] = random.choice(["H","S","C","D","noGiru"])
#         oath[1] = int(8*random.random()*random.random()) + 13
        #random.randrange(13,21)

    def kingGrave(self,grave, giruda):
        """ 여기 tf 로 대체해야 할 부분임. 룰 베이스로 할까... """
        graveCandidate = self.hand + grave
        mighty = self.setMighty(giruda)
        if mighty in graveCandidate:
            graveCandidate.remove(mighty)
        if joker in graveCandidate:
            graveCandidate.remove(joker)
        
        #아래에 노기루가 고려 안되어있다 젠장..... shapeCounter에도 그렇고 아래 로직에도 그렇고....
        if giruda == 'noGiru':
            while len(graveCandidate) > len(grave):
                giruMax = 0
                findMaxIndex = 0
                for i in graveCandidate:
                    if i[1] > giruMax:
                        giruMax = i[1]
                        findMaxIndex = graveCandidate.index(i)
                graveCandidate.pop(findMaxIndex)
        elif (len(graveCandidate) - gf.shapeCounter(graveCandidate, giruda)) > len(grave): #기루 아닌게 버리기 충분할때
            tempList = []
            print('giru delete: '+ str(giruda))
            for i in graveCandidate:
                if i[0] == giruda: 
                    tempList.append(i)
            for i in tempList:
                graveCandidate.remove(i)#논기루만 남긴다
                print(i)

            while len(graveCandidate) > len(grave): #버릴만큼 남을때까지
                findMax = 0
                findMaxIndex = 0
                for i in graveCandidate: #최대값 카드를 찾는 loop
                    if i[1] > findMax:
                        findMax = i[1]
                        findMaxIndex = graveCandidate.index(i)
                graveCandidate.pop(findMaxIndex) #여기 버릴만큼만 남았다
                
        else: #기루 아닌게 버리기 부족할때. 논기루 1개 놔두고 나머지는 기루에서 버린다. 
            giruset = gf.shapeCollector(graveCandidate, giruda)
            nonGiruset = graveCandidate +[]
            if len(giruset) != len(graveCandidate): #기루 아닌것도 들고있을때 있을 때
                for k in range(len(graveCandidate) - len(giruset) - 1): #기루중에서 최종적으로 남길 걸 없앤다
                    giruMax = 0
                    findMaxIndex = 0
                    for i in giruset:
                        if i[1] > giruMax:
                            giruMax = i[1]
                            findMaxIndex = giruset.index(i)
                        if i in nonGiruset: nonGiruset.remove(i) #하는김에 논기루셋 만들어놓기
                    giruset.pop(findMaxIndex)
                for k in range(len(nonGiruset)-1): #논기루 최대 하나만 남겨야 해
                    findMin = 15
                    findMinIndex = 0
                    for i in nonGiruset:
                        if i[1] < findMin:
                            findMin = i[1]
                            findMinIndex = nonGiruset.index(i)
                    nonGiruset.pop(findMinIndex) #논기루 min 제거한다.
                graveCandidate = giruset + nonGiruset #여기 버릴만큼만 남았다
            else: #논기루 없을때 (다 기루임 ㄷㄷ)
                for k in range(len(graveCandidate) - len(grave)): #무덤 갯수만큼 남겨야 함, 맥스를 쓰레기 후보에서 제거
                    giruMax = 0
                    findMaxIndex = 0
                    for i in graveCandidate:
                        if i[1] > giruMax:
                            giruMax = i[1]
                            findMaxIndex = graveCandidate.index(i)
                    graveCandidate.pop(findMaxIndex)#여기 버릴만큼만 남았다
        
        self.hand = self.hand + grave
        for i in graveCandidate:
            self.hand.remove(i)
        graveAgain = graveCandidate
        return graveAgain

        
    def callFriend(self, giruda):
        mighty, jokerCall = gf.setMightyJokercall(giruda)
        if mighty not in self.hand:
            return mighty
        elif joker not in self.hand:
            return joker
        elif giruda == 'noGiru':
            if ['S', 14] not in self.hand:
                return ['S', 14]
            elif ['H', 14] not in self.hand:
                return ['H', 14]
            elif ['C', 14] not in self.hand:
                return ['C', 14]
            elif ['D', 14] not in self.hand:
                return ['D', 14]
            elif ['C', 13] not in self.hand:
                return ['C', 13]
            elif ['D', 13] not in self.hand:
                return ['D', 13]
            elif ['H', 13] not in self.hand:
                return ['H', 13]
            elif ['S', 13] not in self.hand:
                return ['S', 13]
            elif ['C', 12] not in self.hand:
                return ['S', 12]
        elif [giruda, 14] not in self.hand:
            return [giruda, 14]
        elif [giruda, 13] not in self.hand:
            return [giruda, 13]
        elif [giruda, 12] not in self.hand:
            return [giruda, 12]
        elif [giruda, 11] not in self.hand:
            return [giruda, 11]
        elif [giruda, 10] not in self.hand:
            return [giruda, 10]
        elif [giruda, 9] not in self.hand:
            return [giruda, 9]
        elif [giruda, 8] not in self.hand:
            return [giruda, 8]
        elif [giruda, 7] not in self.hand:
            return [giruda, 7]
        elif [giruda, 6] not in self.hand:
            return [giruda, 6]
        else: return "noFriend"
        print("친구고르기")
    
    def possibleOptions(self, turnShape, mighty): 
        if turnShape == 'all':
            count = 0
        else:
            count = gf.shapeCounter(self.hand, turnShape)
        if count > 0:
            options = gf.shapeCollector(self.hand, turnShape)
            if mighty in self.hand:
                options.append(mighty)
            if joker in self.hand:
                options.append(joker)
        else:
            options = self.hand.copy()
        return options

    def sayShape(self):
        # when startCard is 'joker', then first player needs to say shape.
        return 'S'


    def pickCard(self, bits, turnShape, mighty):        #젤어렵겠다... AI 구현 with TF
#         print('카드 고르기')
#     self.hand[random.randrange(0,len(self.hand))]
        myOptions = self.possibleOptions(turnShape, mighty)
        myPick = myOptions[random.randrange(0,len(myOptions))]
        self.hand.remove(myPick)
        return myPick

    def jokerCallPick(self, bits, turnShape, mighty):
        if joker in self.hand:
            self.hand.remove(joker)
            return joker
        else:
            return self.pickCard(bits, turnShape, mighty)
# # 인풋은 뭐뭐여야 할까
# # 내가 선일때, 선 아닐때를 구분해야 할까...
#         if len(self.hand) > 0:
#             return self.hand.pop()
#         else: 
#             print('noCardError')
#             return False
# #         list.count(s) #리스트 내 s를 세는 함수




"""
용어 수정할까나
    주공      President, Declarer
    공약      bidding, bid
    선       lead
    야당      defender

선을 뭐라고 부르지...roundShape?
"""