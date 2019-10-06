from judge import judge_pattern
import random
import time
from winner import judge_winner
from collections import Counter
#牌型对应表：
#同花顺-->8
#四条-->7
# 葫芦-->6
# 同花-->5
# 顺子-->4
# 三条-->3
# 两对-->2
# 对子-->1
# 高牌-->0

def check_if_correct(array):               #检查输入是否正确函数   返回True/False  True代表正确，False代表错误
    rp = Counter(array)
    for i in rp.values():
        if i>1:
            return False
    for j in array:
        if j[0]!='0' or j[1]!='x' or int(j[0:3],16)<2 or int(j[0:3],16)>14 or not(j[3]=='c' or  j[3]=='d' or j[3]=='s' or j[3]=='h'):
            return False
    return True


def fapai_7(hand1,hand2,hand3,hand4,hand5,hand6,hand7):      #hand1和hand2表示手牌，hand3,4,5,6,7表示中间牌；输出我方和对方的7张总牌list
    paizu_or = define_paizu()
    paizu = xipai(paizu_or)
    paizu.remove(hand1)
    paizu.remove(hand2)
    paizu.remove(hand3)
    paizu.remove(hand4)
    paizu.remove(hand5)
    paizu.remove(hand6)
    paizu.remove(hand7)
    result = []
    enemy = []
    mid = [hand3, hand4, hand5, hand6,hand7]
    result.append(hand1)
    result.append(hand2)
    for i in range(0, 2):
        enemy.append(paizu[0])
        paizu.pop(0)
    for j in range(0, 5):
        result.append(mid[j])
        enemy.append(mid[j])
    return result, enemy



def fapai_6(hand1,hand2,hand3,hand4,hand5,hand6):             #hand1和hand2表示手牌，hand3,4,5,6表示中间牌；输出我方和对方的7张总牌list
    paizu_or = define_paizu()
    paizu = xipai(paizu_or)
    paizu.remove(hand1)
    paizu.remove(hand2)
    paizu.remove(hand3)
    paizu.remove(hand4)
    paizu.remove(hand5)
    paizu.remove(hand6)
    result = []
    enemy = []
    mid = [hand3, hand4, hand5,hand6]
    result.append(hand1)
    result.append(hand2)
    for i in range(0, 2):
        enemy.append(paizu[0])
        paizu.pop(0)
    mid.append(paizu[0])
    paizu.pop(0)
    for j in range(0, 5):
        result.append(mid[j])
        enemy.append(mid[j])
    return result, enemy

def fapai_5(hand1,hand2,hand3,hand4,hand5):                #hand1,hand2表示手牌，hand3,4,5表示中间牌；输出我方和对手的7张总牌list
    paizu_or = define_paizu()
    paizu = xipai(paizu_or)
    paizu.remove(hand1)
    paizu.remove(hand2)
    paizu.remove(hand3)
    paizu.remove(hand4)
    paizu.remove(hand5)
    result = []
    enemy = []
    mid = [hand3,hand4,hand5]
    result.append(hand1)
    result.append(hand2)
    for i in range(0,2):
        enemy.append(paizu[0])
        paizu.pop(0)
    for k in range(0,2):
        mid.append(paizu[0])
        paizu.pop(0)
    for j in range(0,5):
        result.append(mid[j])
        enemy.append(mid[j])
    return result,enemy



def fapai_2(hand1,hand2):                 #模拟翻牌前发牌过程，输入为2个字符串，表示自己手中的牌；返回两个列表，分别表示自己的总牌和对方的总牌list
    paizu_or = define_paizu()
    paizu = xipai(paizu_or)
    paizu.remove(hand1)
    paizu.remove(hand2)
    result = []
    enemy = []
    mid = []
    result.append(hand1)
    result.append(hand2)
    for i in range(0,2):
        enemy.append(paizu[0])
        paizu.pop(0)
    for j in range(0,5):
        mid.append(paizu[j])
        result.append(mid[j])
        enemy.append(mid[j])
    return result,enemy






def define_paizu():
    paizu = []
    for i in range(0,4):
        if i == 0:
            for j in range(2,15):
                paizu.append(str(hex(j))+'s')
        elif i == 1:
            for j in range(2,15):
                paizu.append(str(hex(j))+'h')
        elif i == 2:
            for j in range(2,15):
                paizu.append(str(hex(j))+'c')
        else:
            for j in range(2,15):
                paizu.append(str(hex(j))+'d')
    return paizu


def xipai(paizu):                              #洗牌函数，传入一个牌组(list)，输出一个牌组(list)   Knuth-Durstenfeld Shuffle算法
    result = paizu[:]
    for i in range(1, len(paizu)):
        j = random.randrange(0, i)
        result[i] = result[j]
        result[j] = paizu[i]
    return result



def judge_type(s):                             #传入一个judge_pattern类型的对象，输出牌型
    tonghuashun,pokes = s.judge_TONGHUASHUN()
    if tonghuashun:              #是同花顺
        return 8,pokes
    else:
        shunzi,pokes = s.judge_SHUNZI()
    if shunzi :
        return 4,pokes
    else:
        sitiao,pokes = s.judge_SITIAO()
    if sitiao:
        return 7,pokes
    else:
        hulu,pokes = s.judge_HULU()
    if hulu:
        return 6,pokes
    else:
        tonghua,pokes = s.judge_TONGHUA()
    if tonghua:
        return 5,pokes
    else:
        santiao,pokes= s.judge_SANTIAO()
    if santiao:
        return 3,pokes
    else:
        liangdui,pokes = s.judge_LIANGDUI()
    if liangdui:
        return 2,pokes
    else:
        duizi,pokes = s.judge_DUIZI()
    if duizi:
        return 1,pokes
    else:
        gaopai,pokes = s.judge_GAOPAI()
        return 0,pokes

def show_hands(hands):
    result =[]
    for i in range(0,5):
        number = int(hands[i][:3],16)
        if number<11:
            result.append(str(number))
        elif number==11:
            result.append('J')
        elif number==12:
            result.append('Q')
        elif number==13:
            result.append('K')
        else:
            result.append('A')
    return result

def translate_cards(t,c):
    if t=='0':
        hand = str(hex(int(c)+2))+'h'
    elif t=='1':
        hand = str(hex(int(c)+2)) + 's'
    elif t=='2':
        hand = str(hex(int(c)+2)) + 'd'
    else:
        hand = str(hex(int(c)+2)) + 'c'
    return hand



def mengtekaluo(hands,operater):
    wr = 0
    safe = 0
    sign = 0
    while True:
        if operater=='0':
            print("退出成功!")
            break
        elif operater=='p':
            while True:
                try:
                    if len(hands) == 0:
                        t1,c1,t2,c2=input("请输入手牌(空格分隔)：").split()
                        hand1 = translate_cards(t1,c1)
                        hand2 = translate_cards(t2,c2)
                        hands.append(t1+str(hex(int(c1)))[2])
                        hands.append(t2+str(hex(int(c2)))[2])
                    else:
                        hand1 = translate_cards(hands[0][0],str(int(hands[0][1],16)))
                        hand2 = translate_cards(hands[1][0], str(int(hands[1][1],16)))
                    if not check_if_correct([hand1,hand2]):
                        print("输入有误!")
                        sign = -1
                        break
                    else:
                        win = 0
                        lost = 0
                        draw = 0
                        t1 = time.clock()
                        for i in range(0, 10000):
                            me, enemy = fapai_2(hand1,hand2)
                            me_oj = judge_pattern(me)
                            enemy_oj = judge_pattern(enemy)
                            me_type, me_hands = judge_type(me_oj)
                            enemy_type, enemy_hands = judge_type(enemy_oj)
                            result, tie = judge_winner(me_type, me_hands, enemy_type, enemy_hands)
                            if tie == 1:
                                draw+=1
                                continue
                            else:
                                if result == 0:
                                    win += 1
                                else:
                                    lost+=1
                        t2 = time.clock()
                        wr = win / (win + lost + draw)
                        safe = (win + draw) / (win + lost + draw)
                        sign = 1
                        print("胜率：", wr)
                        print("保险率：", safe)
                        print("运行时间：", t2 - t1)
                        break
                except:
                    print("输入有误!")
                    sign = -1
                    break
            break
        elif operater=="f":
            while True:
                if len(hands)==2:
                    t1,c1,t2,c2,t3,c3=input("请输入中间牌(空格分隔)：").split()
                    hand1 = translate_cards(hands[0][0],str(int(hands[0][1],16)))
                    hand2 = translate_cards(hands[1][0], str(int(hands[1][1], 16)))
                    hand3 = translate_cards(t1, c1)
                    hand4 = translate_cards(t2, c2)
                    hand5 = translate_cards(t3, c3)
                    hands.append(t1 + str(hex(int(c1)))[2])
                    hands.append(t2 + str(hex(int(c2)))[2])
                    hands.append(t3 + str(hex(int(c3)))[2])
                else:
                    hand1 = translate_cards(hands[0][0], str(int(hands[0][1], 16)))
                    hand2 = translate_cards(hands[1][0], str(int(hands[1][1], 16)))
                    hand3 = translate_cards(hands[2][0], str(int(hands[2][1], 16)))
                    hand4 = translate_cards(hands[3][0], str(int(hands[3][1], 16)))
                    hand5 = translate_cards(hands[4][0], str(int(hands[4][1], 16)))
                try:
                    if not check_if_correct([hand1,hand2,hand3,hand4,hand5]):
                        print("输入有误!")
                        sign = -1
                        break
                    else:
                        win = 0
                        lost = 0
                        draw = 0
                        t1 = time.clock()
                        for i in range(0,10000):
                            me, enemy = fapai_5(hand1,hand2,hand3,hand4,hand5)
                            me_oj = judge_pattern(me)
                            enemy_oj = judge_pattern(enemy)
                            me_type, me_hands = judge_type(me_oj)
                            enemy_type, enemy_hands = judge_type(enemy_oj)
                            result, tie = judge_winner(me_type, me_hands, enemy_type, enemy_hands)
                            if tie == 1:
                                draw += 1
                                continue
                            else:
                                if result == 0:
                                    win += 1
                                else:
                                    lost += 1
                        t2 = time.clock()
                        wr = win / (win + lost + draw)
                        safe = (win + draw) / (win + lost + draw)
                        sign = 1
                        print("胜率：", wr)
                        print("保险率：", safe)
                        print("运行时间：", t2 - t1)
                        break
                except:
                    print("输入有误!")
                    sign = -1
                    break
            break
        elif operater=="t":
            while True:
                if len(hands) == 5:
                    hand1 = translate_cards(hands[0][0], str(int(hands[0][1], 16)))
                    hand2 = translate_cards(hands[1][0], str(int(hands[1][1], 16)))
                    hand3 = translate_cards(hands[2][0], str(int(hands[2][1], 16)))
                    hand4 = translate_cards(hands[3][0], str(int(hands[3][1], 16)))
                    hand5 = translate_cards(hands[4][0], str(int(hands[4][1], 16)))
                    t1,c1 = input("请输入转牌(空格分隔)：").split()
                    hand6 = translate_cards(t1,c1)
                    hands.append(t1 + str(hex(int(c1)))[2])
                else:
                    hand1 = translate_cards(hands[0][0], str(int(hands[0][1], 16)))
                    hand2 = translate_cards(hands[1][0], str(int(hands[1][1], 16)))
                    hand3 = translate_cards(hands[2][0], str(int(hands[2][1], 16)))
                    hand4 = translate_cards(hands[3][0], str(int(hands[3][1], 16)))
                    hand5 = translate_cards(hands[4][0], str(int(hands[4][1], 16)))
                    hand6 = translate_cards(hands[5][0], str(int(hands[5][1], 16)))
                try:
                    if not check_if_correct([hand1,hand2,hand3,hand4,hand5,hand6]):
                        print("输入有误!")
                        sign = -1
                        break
                    else:
                        win = 0
                        lost = 0
                        draw = 0
                        t1 = time.clock()
                        for i in range(0, 10000):
                            me, enemy = fapai_6(hand1, hand2, hand3, hand4, hand5,hand6)
                            me_oj = judge_pattern(me)
                            enemy_oj = judge_pattern(enemy)
                            me_type, me_hands = judge_type(me_oj)
                            enemy_type, enemy_hands = judge_type(enemy_oj)
                            result, tie = judge_winner(me_type, me_hands, enemy_type, enemy_hands)
                            if tie == 1:
                                draw += 1
                                continue
                            else:
                                if result == 0:
                                    win += 1
                                else:
                                    lost += 1
                        t2 = time.clock()
                        wr = win / (win + lost + draw)
                        safe = (win + draw) / (win + lost + draw)
                        sign = 1
                        print("胜率：", wr)
                        print("保险率：", safe)
                        print("运行时间：", t2 - t1)
                        break
                except:
                    print("输入有误!")
                    sign = -1
                    break
            break
        elif operater=="r":
            while True:
                if len(hands) == 6:
                    hand1 = translate_cards(hands[0][0], str(int(hands[0][1], 16)))
                    hand2 = translate_cards(hands[1][0], str(int(hands[1][1], 16)))
                    hand3 = translate_cards(hands[2][0], str(int(hands[2][1], 16)))
                    hand4 = translate_cards(hands[3][0], str(int(hands[3][1], 16)))
                    hand5 = translate_cards(hands[4][0], str(int(hands[4][1], 16)))
                    hand6 = translate_cards(hands[5][0], str(int(hands[5][1], 16)))
                    t1,c1 = input("请输入河牌(空格分隔)：").split()
                    hand7 = translate_cards(t1,c1)
                    hands.append(t1 + str(hex(int(c1)))[2])
                else:
                    hand1 = translate_cards(hands[0][0], str(int(hands[0][1], 16)))
                    hand2 = translate_cards(hands[1][0], str(int(hands[1][1], 16)))
                    hand3 = translate_cards(hands[2][0], str(int(hands[2][1], 16)))
                    hand4 = translate_cards(hands[3][0], str(int(hands[3][1], 16)))
                    hand5 = translate_cards(hands[4][0], str(int(hands[4][1], 16)))
                    hand6 = translate_cards(hands[5][0], str(int(hands[5][1], 16)))
                    hand7 = translate_cards(hands[6][0], str(int(hands[6][1], 16)))
                try:
                    if not check_if_correct([hand1,hand2,hand3,hand4,hand5,hand6,hand7]):
                        print("输入有误!")
                        sign = -1
                        break
                    else:
                        win = 0
                        lost = 0
                        draw = 0
                        t1 = time.clock()
                        for i in range(0, 10000):
                            me, enemy = fapai_7(hand1, hand2, hand3, hand4, hand5, hand6,hand7)
                            me_oj = judge_pattern(me)
                            enemy_oj = judge_pattern(enemy)
                            me_type, me_hands = judge_type(me_oj)
                            enemy_type, enemy_hands = judge_type(enemy_oj)
                            result, tie = judge_winner(me_type, me_hands, enemy_type, enemy_hands)
                            if tie == 1:
                                draw += 1
                                continue
                            else:
                                if result == 0:
                                    win += 1
                                else:
                                    lost += 1
                        t2 = time.clock()
                        wr = win/(win + lost + draw)
                        safe=(win + draw)/(win + lost + draw)
                        sign = 1
                        print("胜率：", wr)
                        print("保险率：", safe)
                        print("运行时间：", t2 - t1)
                        break
                except:
                    print("输入有误！")
                    sign = -1
                    break
            break
        else:
            sign = -1
            break
    return wr,safe,sign,hands




# t1= time.clock()                                  #专找某一牌型的牌
# counter = 0
# hands_type=0
# while True:
#     counter+=1
#     paizu = define_paizu()
#     paizu = xipai(paizu)
#     hand = [paizu[i] for i in range(0,7)]
#     hands = judge_pattern(hand)
#     hands_type,final_hands = judge_type(hands)
#     if hands_type ==8:
#         print(final_hands)
#         print(show_hands(final_hands))
#         break
# t2= time.clock()
# print(t2-t1)
# print(counter)

# paizu = define_paizu()                                      #模拟一手牌
# paizu = xipai(paizu)
# hand = [paizu[i] for i in range(0,7)]
# hands = judge_pattern(hand)
# hands_type,final_hands = judge_type(hands)
# print(hands_type)
# print(show_hands(final_hands))




# win_times  = 0                        #蒙特卡洛算翻牌前胜率
# all = 0
# t1=time.clock()
# for i in range(0,10000):
#     me,enemy = fapai_7('0xch','0x2d','0x3d','0xcd','0xcc','0xbh','0xbs')
#     me_oj = judge_pattern(me)
#     enemy_oj = judge_pattern(enemy)
#     me_type,me_hands = judge_type(me_oj)
#     enemy_type,enemy_hands = judge_type(enemy_oj)
#     result,tie=judge_winner(me_type,me_hands,enemy_type,enemy_hands)
#     if tie == 1:
#         all+=1
#         continue
#     else:
#         if result==0:
#             win_times+=1
#     all+=1
# t2=time.clock()
# print(win_times/all)
# print(t2-t1)


