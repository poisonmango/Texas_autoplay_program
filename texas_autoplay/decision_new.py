import math
from meng import mengtekaluo
import socket
import re



def count_rua(money,forwin,test,cb1,cb2):
    if money >= 6666 or forwin == 1:
        return 0
    elif cb1 <= 800 and cb2 >= 2400 and test == 1:
        return 1
    elif cb2 >=4800 and test == 1:
        return 2
    elif test == 1:
        return 3
    elif money <= -3800+44*number:
        return 4
    elif cb1 <= 800 and cb2 >= 3200:
        return 1
    elif cb2 >=5000:
        return 2
    else:
        return 3


def count_small(f1):         #计算small的值
    if f1 == 0:
        return 0
    elif f1>0:
        return 1
    else:
        return -1


def count_rate(cb2,Eb):
    if cb2 >= 0 and cb2 <= 150:
        return 0.04*math.log(30/180)+0.01
    elif cb2 > 150 and cb2 <= 1100:
        if (cb2-Eb/4-100)<=0:
            return -0.02
        else:
            return 0.04*math.log((cb2-Eb/4-100)/180)+0.03
    elif cb2 > 1100 and cb2 <= 3200:
        if (cb2-Eb/4-1100)<=0:
            return 0.09
        else:
            return 0.000008*pow(cb2-Eb/4-1100,1.3)+0.10
    else:
        if (cb2-Eb/4-100)<=0:
            return 0.30
        else:
            return 0.04*math.log((cb2-Eb/4-100)/180)/math.log(2)+0.10


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

def rcv(sk,teshu):
    while True:
        recv = sk.recv(1024*10)
        message = str(recv,encoding="utf-8")
        if not message == "":
            if "fold" in message and "earn" in message:
                teshu = 1
                print(message)
                return message,teshu

            else:
                print(message)
                return message,teshu

def sed(send,sk):
    sk.sendall(bytes(send,encoding="utf-8"))


ip_address = input("请输入平台ip地址：")
port = input("请输入平台端口号：")
#socket连接
sk = socket.socket()
sk.connect((ip_address,int(port)))
message = rcv(sk)
if "name" in message:
    sed("beep",sk)

#对局开始
money = 0
teshu = 0
number = 1
test = 0
lang = 0
while True:
    # try:
    if teshu == 1:
        money += int(re.search("earn (.*?)preflop",message).group(1))
        number+=1
        message = re.search("preflop.*",message).group(0)
        continue
    else:
        message,teshu=rcv(sk,teshu)
    if "oppo" in message:
        message,teshu=rcv(sk,teshu)
    if message[8] == "B":
        player_type = 'b'
    else:
        player_type = 's'
    hands = []
    wr = 0
    safe = 0
    cb1 = 0
    cb2 = 0
    ch1 = 20000-cb1
    ch2 = 20000-cb2
    ct1 = 0
    ct2 = 0
    turn_to_end = 0
    if money<=-3000:
        lang=1
    if money<= -8000:
        test = 1
    forwin = 0
    if money>(70-number)*75+100:
        forwin = 1
    #preflop参数预处理
    find = re.search(".*?\|.*?\|<(.*?),(.*?)><(.*?),(.*?)>", message)
    hands.append(find.group(1)+str(hex(int(find.group(2))))[2])
    hands.append(find.group(3)+str(hex(int(find.group(4))))[2])
    print(hands)
    R = 200
    PM = 0
    if player_type == 'b':
        cb1 += 100
        ch1 = 20000-cb1
        cb2 += 50
        ch2 = 20000-cb2
    else:
        cb1 += 50
        ch1 = 20000 - cb1
        cb2 += 100
        ch2 = 20000 - cb2
    f1 = cb2-cb1
    small = count_small(f1)
    operater = 'p'
    #preflop阶段
    while True:
        if wr == 0 and safe == 0:
            wr,safe,sign,hands=mengtekaluo(hands,operater)
            if sign == -1:
                hands.pop()
                hands.pop()
                wr = 0
                safe = 0
                continue
        if player_type == 'b':
            if  "pre" in message:
                message,teshu = rcv(sk,teshu)
                if teshu == 1:
                    message = re.search("preflop.*", message)
                    break
            elif "flop" in message:
                break
            elif "raise" in message:
                chouma = int(message.split()[1])
            elif  "call" in message:
                chouma = 100
            elif  "allin" in message:
                cb2 = 0
                chouma = 20000
            else:
                turn_to_end = 1
                break
        else:
            if  "pre" in message:
                chouma = 100
            elif "flop" in message:
                break
            elif "raise"in message:
                chouma = int(message.split()[1])
            elif "allin" in message:
                cb2 = 0
                chouma = 20000
            else:
                turn_to_end = 1
                break
        cb2 = chouma
        ch2 = 20000-cb2
        PM = chouma
        if not PM == 0:
            R = 2 * PM
        f1 = cb2 - cb1
        Ef = -cb1
        Eb = wr * cb2 - (1 - safe) * cb2
        Er = 2 * Eb
        rate = count_rate(cb2, Eb)
        rua = count_rua(money, forwin, test, cb1, cb2)
        small = count_small(f1)
        print("wr:"+str(wr)+" safe:"+str(safe)+" f1:"+str(f1)+" Ef:"+str(Ef)+" Eb:"+str(Eb)+" Er:"+str(Er)+" rate:"+str(rate)+" rua:"+str(rua)+" small:"+str(small)+" PM:"+str(PM)+" cb1:"+str(cb1)+" cb2:"+str(cb2) +" 主程序处理开始--->>>")
        print("ct1:"+str(ct1)+" ct2:"+str(ct2))
        fold1=0
        check1=0
        call1=0
        r1=0
        allin1=0
        if rua==0:
            if small == 0:
                if safe - rate - number * 0.002 >= 0.80:
                    r1 = 1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small == 1:
                if safe >= 0.73 and safe - rate - number * 0.002 > 0.63:
                    call1 = 1
                else:
                    fold1 = 1
        elif rua==1:
            if small == 0:
                if "check" in message:
                    call1 = 1
                else: check1 = 1
            elif small == 1:
                if safe >= 0.65 and safe-wr<=0.08:
                    call1 = 1
                elif safe >= 0.65:
                    call1 = 1
                else:
                    fold1 = 1
        elif rua==2:
            if small == 0:
                if "check" in message:
                    call1=1
                else: check1 = 1
            elif small == 1:
                if cb1 > 3200 or safe >= 0.65:
                    if safe-wr <= 0.08:
                        call1 = 1
                    elif safe >= 0.65:
                        call1 = 1
                    else:
                        fold1 = 1
                else:
                    fold1 = 1
        elif rua==3:
            if small == 0:
                if safe - rate >= 0.67:
                    r1 = 1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small == 1:
                if safe - rate >= 0.67:
                    r1 = 1
                elif safe - rate > 0.45:
                    call1 = 1
                elif safe>0.6 and safe - rate > 0.4:
                     call1 = 1
                else:
                    fold1 = 1
        else:
            if small == 0:
                if safe - rate >= 0.67:
                    r1 = 1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small == 1:
                if safe - rate > 0.67:
                    r1 = 1
                elif safe - rate > 0.48:
                    call1 = 1
                elif safe>0.50 and safe - rate > 0.28:
                     call1 = 1
                else:
                    fold1 = 1
        if fold1==1:
            print("决策：fold")
            sed("fold",sk)
            turn_to_end = 1
            break
        elif check1==1:
            print("决策：check")
            sed("check",sk)
            message,teshu = rcv(sk,teshu)
            break
        elif call1==1:
            print("决策：call")
            sed("call",sk)
            cb1=cb2
            ch1=20000-cb1
            if cb1 == 20000:
                turn_to_end = 1
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        elif r1==1:
            a = R
            print("决策：raise "+str(a))
            sed("raise "+str(a),sk)
            PM = a
            if not PM == 0:
                R = PM * 2
            cb1 = ct1+a
            ch1 = 20000 - cb1
            message,teshu = rcv(sk,teshu)
            if teshu == 1 :
                break
        else:
            print("决策：allin")
            sed("allin",sk)
            cb1 = 20000
            ch1 = 0
            turn_to_end=1
            break
    if teshu == 1 :
        continue
    cb2=cb1
    ch2=20000-cb2
    ct1 = cb1
    ct2 = cb2
    R = 200
    PM = 0
    f1 = cb2 - cb1
    small = count_small(f1)
    operater = 'f'
    wr = 0
    safe = 0
    if not turn_to_end == 1:
        find = re.search(".*?\|<(.*?),(.*?)><(.*?),(.*?)><(.*?),(.*?)>", message)
        hands.append(find.group(1) + str(hex(int(find.group(2))))[2])
        hands.append(find.group(3) + str(hex(int(find.group(4))))[2])
        hands.append(find.group(5) + str(hex(int(find.group(6))))[2])
        print(hands)
    #flop阶段
    while True:
        if turn_to_end==1:
            break
        if wr == 0 and safe == 0:
            wr,safe,sign,hands=mengtekaluo(hands,operater)
            if sign == -1:
                hands.pop()
                hands.pop()
                hands.pop()
                wr = 0
                safe = 0
                continue
        if player_type == 'b':
            if "flop" in message:
                chouma = 0
            elif  "turn" in message:
                break
            elif "raise" in message:
                chouma = int(message.split()[1])
            elif "allin" in message:
                cb2 = 0
                ct2 = 0
                chouma = 20000
            else:
                turn_to_end = 1
                break
        else:
            if "flop" in message:
                message,teshu = rcv(sk,teshu)
                if teshu == 1:
                    continue
            elif "turn" in message:
                break
            elif "check" in message:
                chouma = 0
            elif "raise" in message:
                chouma = int(message.split()[1])
            elif "allin" in message:
                cb2 = 0
                ct2 = 0
                chouma = 20000
            else:
                turn_to_end =1
                break
        cb2 = ct2 + chouma
        ch2 = 20000-cb2
        PM = chouma
        if not PM == 0:
            R = 2 * PM
        f1 = cb2 - cb1
        Ef = -cb1
        Eb = wr * cb2 - (1 - safe) * cb2
        Er = 2 * Eb
        rate = count_rate(cb2, Eb)
        rua = count_rua(money, forwin, test, cb1, cb2)
        small = count_small(f1)
        print("wr:" + str(wr) + " safe:" + str(safe) + " f1:" + str(f1) + " Ef:" + str(Ef) + " Eb:" + str(
            Eb) + " Er:" + str(Er) + " rate:" + str(rate) + " rua:" + str(rua) + " small:" + str(
            small) + " PM:" + str(PM) + " cb1:" + str(cb1) + " cb2:" + str(cb2) + " 主程序处理开始--->>>")
        print("ct1:" + str(ct1) + " ct2:" + str(ct2))
        fold1 = 0
        check1 = 0
        call1 = 0
        bet1 = 0
        bet2 = 0
        r1 = 0
        r2 = 0
        allin1 = 0
        if rua == 0:
            if small == 0:
                if safe-rate-number*0.002>=0.80:
                    bet1=1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small == 1:
                if safe>=0.78 and safe-rate-number*0.002>0.66:
                    call1=1
                else:
                    fold1=1
        elif rua == 1:
            if small == 0:
                if wr>=0.84 :
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif "check" in message:
                    call1 = 1
                else: check1 = 1
            elif small == 1:
                if wr>=0.84:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif safe >= 0.80 and safe-wr<=0.08:
                    call1 = 1
                elif safe >= 0.84:
                    call1 = 1
                else:
                    fold1 = 1
        elif rua == 2:
            if small == 0:
                if wr>=0.83:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif "check" in message:
                    call1 = 1
                else: check1 = 1
            elif small == 1:
                if wr>=0.83:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif cb1 > 4000 or safe >= 0.77:
                    if safe-wr <= 0.08:
                        call1 = 1
                    elif safe >= 0.83:
                        call1 = 1
                    else:
                        fold1 = 1
                else:
                    fold1 = 1
        elif rua == 3:
            if small==0:
                if safe-rate>=0.64:
                    bet1=1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small==1:

                if safe-rate>0.66:
                    r1=1
                elif safe-rate>0.50:
                    call1=1
                else:
                    fold1=1
        else:
            if small==0:
                if cb2>2000 and safe>0.63:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif safe-rate>=0.52:
                    bet2=1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small==1:
                if cb2>2000 and safe>0.63:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif safe-rate>0.52:
                    r2=1
                elif safe-rate>0.37:
                    call1=1
                else:
                    fold1=1
        if fold1==1:
            print("决策：fold")
            sed("fold",sk)
            turn_to_end = 1
            break
        elif check1==1:
            print("决策：check")
            sed("check",sk)
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        elif call1==1:
            print("决策：call")
            sed("call",sk)
            cb1=cb2
            ch1=20000-cb1
            if cb1 == 20000:
                turn_to_end = 1
            message,teshu = rcv(sk,teshu)
            break
        elif bet1==1:
            a=R
            print("决策：bet "+str(a))
            sed("raise "+str(a),sk)
            cb1 = ct1+a
            ch1 = 20000-cb1
            PM = a
            if not PM == 0:
                R = PM * 2
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        elif r1==1:
            a = R
            print("决策：raise "+str(a))
            sed("raise "+str(a),sk)
            PM = a
            if not PM == 0:
                R = PM * 2
            cb1 = ct1+a
            ch1 = 20000 - cb1
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        elif bet2==1:
            c = 3*R
            print("决策：bet "+str(c))
            sed("raise "+str(c),sk)
            cb1 = ct1 + c
            ch1 = 20000-cb1
            PM = c
            if not PM ==0:
                R = 2 * PM
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        elif r2==1:
            c = 3*R
            print("决策：raise "+str(c))
            sed("raise "+str(c),sk)
            PM = c
            if not PM ==0:
                R = 2 * PM
            cb1 = ct1+c
            ch1 = 20000-cb1
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        else:
            print("决策：allin")
            sed("allin",sk)
            cb1 = 20000
            ch1 = 0
            turn_to_end=1
            break
    if teshu == 1:
        continue
    cb2 = cb1
    ch2 = 20000-cb2
    ct1 = cb1
    ct2 = cb2
    R = 400
    PM = 0
    f1 = cb2 - cb1
    small = count_small(f1)
    operater = 't'
    wr = 0
    safe = 0
    if not turn_to_end == 1:
        find = re.search(".*?\|<(.*?),(.*?)>", message)
        hands.append(find.group(1) + str(hex(int(find.group(2))))[2])
        print(hands)
    # turn阶段
    while True:
        if turn_to_end == 1:
            break
        if wr == 0 and safe == 0:
            wr, safe, sign, hands = mengtekaluo(hands, operater)
            if sign == -1:
                hands.pop()
                wr = 0
                safe = 0
                continue
        if player_type == 'b':
            if "turn" in message:
                chouma = 0
            elif "river" in message:
                break
            elif "raise" in message:
                chouma = int(message.split()[1])
            elif "allin" in message:
                cb2 = 0
                ct2 = 0
                chouma = 20000
            else:
                turn_to_end = 1
                break
        else:
            if "turn" in message:
                message,teshu = rcv(sk,teshu)
                if teshu == 1:
                    break
                continue
            elif "river" in message:
                break
            elif "check" in message:
                chouma = 0
            elif "raise" in message:
                chouma = int(message.split()[1])
            elif "allin" in message:
                cb2 = 0
                ct2 = 0
                chouma = 20000
            else:
                turn_to_end =1
                break
        cb2 = ct2 + chouma
        ch2 = 20000-cb2
        PM = chouma
        if not PM == 0:
            R = 2 * PM
        f1 = cb2 - cb1
        Ef = -cb1
        Eb = wr * cb2 - (1 - safe) * cb2
        Er = 2 * Eb
        rate = count_rate(cb2, Eb)
        rua = count_rua(money, forwin, test, cb1, cb2)
        small = count_small(f1)
        print("wr:" + str(wr) + " safe:" + str(safe) + " f1:" + str(f1) + " Ef:" + str(Ef) + " Eb:" + str(
            Eb) + " Er:" + str(Er) + " rate:" + str(rate) + " rua:" + str(rua) + " small:" + str(
            small) + " PM:" + str(PM) + " cb1:" + str(cb1) + " cb2:" + str(cb2) + " 主程序处理开始--->>>")
        print("ct1:" + str(ct1) + " ct2:" + str(ct2))
        fold1 = 0
        check1 = 0
        call1 = 0
        bet1 = 0
        bet2 = 0
        r1 = 0
        r2 = 0
        allin1 = 0
        if rua == 0:
            if small ==0:
                if safe-rate-number*0.002>=0.80:
                    bet1=1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small==1:
                if safe>=0.78 and safe-rate-number*0.002>0.66:
                    call1=1
                else:
                    fold1=1
        elif rua == 1:
            if small == 0:
                if wr>=0.85:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif "check" in message:
                    call1 = 1
                else: check1 = 1
            elif small == 1:
                if wr>=0.85:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif safe >= 0.80 and safe-wr<=0.08:
                    call1 = 1
                elif safe >= 0.85:
                    call1 = 1
                else:
                    fold1 = 1
        elif rua == 2:
            if small == 0:
                if wr>=0.84:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif "check" in message:
                    call1 = 1
                else: check1 = 1
            elif small == 1:
                if wr>=0.84:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif cb1 > 4000 or safe >= 0.78:
                    if safe-wr <= 0.08:
                        call1 = 1
                    elif safe >= 0.84:
                        call1 = 1
                    else:
                        fold1 = 1
                else:
                    fold1 = 1

        elif rua == 3:
            if small ==0:
                if safe-rate>=0.64:
                    bet1=1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small==1:
                if safe-rate>0.66:
                    r1=1
                elif safe-rate>0.50:
                    call1=1
                else:
                    fold1=1
        else:
            if small==0:
                if cb2>1600 and safe>0.63:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif safe-rate>=0.52:
                    bet2=1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small==1:
                if cb2>1600 and safe>0.63:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif safe-rate>0.52:
                    r2=1
                elif safe-rate>0.37:
                    call1=1
                else:
                    fold1=1
        if fold1==1:
            print("决策：fold")
            sed("fold",sk)
            turn_to_end = 1
            break
        elif check1==1:
            print("决策：check")
            sed("check",sk)
            message,teshu  = rcv(sk,teshu)
            if teshu == 1:
                break
        elif call1==1:
            print("决策：call")
            sed("call",sk)
            cb1=cb2
            ch1=20000-cb1
            if cb1 == 20000:
                turn_to_end = 1
            message,teshu = rcv(sk,teshu)
            break
        elif bet1==1:
            a=R
            print("决策：bet "+str(a))
            sed("raise "+str(a),sk)
            cb1 = ct1+a
            ch1 = 20000-cb1
            PM = a
            if not PM == 0:
                R = PM * 2
            message,teshu = rcv(sk,teshu)
            if teshu ==1 :
                break
        elif r1==1:
            a = R
            print("决策：raise "+str(a))
            sed("raise "+str(a),sk)
            PM = a
            if not PM == 0:
                R = PM * 2
            cb1 = ct1+a
            ch1 = 20000 - cb1
            message,teshu  = rcv(sk,teshu)
            if teshu == 1:
                break
        elif bet2==1:
            c = 3*R
            print("决策：bet "+str(c))
            sed("raise "+str(c),sk)
            cb1 = ct1 + c
            ch1 = 20000-cb1
            PM = c
            if not PM ==0:
                R = 2 * PM
            message,teshu = rcv(sk,teshu)
            if teshu== 1:
                break
        elif r2==1:
            c = 3*R
            print("决策：raise "+str(c))
            sed("raise "+str(c),sk)
            PM = c
            if not PM ==0:
                R = 2 * PM
            cb1 = ct1+c
            ch1 = 20000-cb1
            message,teshu = rcv(sk,teshu)
            if teshu ==1:
                break
        else:
            print("决策：allin")
            sed("allin",sk)
            cb1 = 20000
            ch1 = 0
            turn_to_end=1
            break
    if teshu ==1:
        continue
    cb2 = cb1
    ch2 = 20000 - cb2
    ct1 = cb1
    ct2 = cb2
    R = 600
    PM = 0
    f1 = cb2 - cb1
    small = count_small(f1)
    operater = 'r'
    wr = 0
    safe = 0
    if not turn_to_end == 1:
        find = re.search(".*?\|<(.*?),(.*?)>", message)
        hands.append(find.group(1) + str(hex(int(find.group(2))))[2])
        print(hands)
    # river阶段
    while True:
        if turn_to_end == 1:
            break
        if wr == 0 and safe == 0:
            wr, safe, sign, hands = mengtekaluo(hands, operater)
            if sign == -1:
                hands.pop()
                wr = 0
                safe = 0
                continue
        if player_type == 'b':
            if "river" in message:
                chouma = 0
            elif  "earn" in message:
                break
            elif "fold" in message:
                break
            elif "raise" in message:
                chouma = int(message.split()[1])
            elif "allin" in message:
                cb2 = 0
                ct2 = 0
                chouma = 20000
            else:
                turn_to_end = 1
                break
        else:
            if "river" in message:
                message,teshu = rcv(sk,teshu)
                continue
            elif "fold" in message:
                break
            elif "earn" in message:
                break
            elif "check" in message:
                chouma = 0
            elif  "raise" in message:
                chouma = int(message.split()[1])
            elif "allin" in message:
                cb2 = 0
                ct2 = 0
                chouma = 20000
            else:
                turn_to_end =1
                break
        cb2 = ct2 + chouma
        ch2 = 20000 - cb2
        PM = chouma
        if not PM == 0:
            R = 2 * PM
        f1 = cb2 - cb1
        Ef = -cb1
        Eb = wr * cb2 - (1 - safe) * cb2
        Er = 2 * Eb
        rate = count_rate(cb2, Eb)
        rua = count_rua(money, forwin, test, cb1, cb2)
        small = count_small(f1)
        print("wr:" + str(wr) + " safe:" + str(safe) + " f1:" + str(f1) + " Ef:" + str(Ef) + " Eb:" + str(
            Eb) + " Er:" + str(Er) + " rate:" + str(rate) + " rua:" + str(rua) + " small:" + str(
            small) + " PM:" + str(PM) + " cb1:" + str(cb1) + " cb2:" + str(cb2) + " 主程序处理开始--->>>")
        print("ct1:" + str(ct1) + " ct2:" + str(ct2))
        fold1 = 0
        check1 = 0
        call1 = 0
        bet1 = 0
        bet2 = 0
        r1 = 0
        r2 = 0
        allin1 = 0
        if rua == 0:
            if small==0:
                if safe-rate-number*0.002>=0.80:
                    bet1=1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small==1:
                if safe-rate-number*0.002>=0.73:
                    r1=1
                elif safe>=0.77 and safe-rate-number*0.002>0.64:
                    call1=1
                else:
                    fold1=1
        elif rua == 1:
            if small == 0:
                if wr>=0.85:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif "check" in message:
                    call1 = 1
                else: check1 = 1
            elif small == 1:
                if wr>=0.85:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif safe >= 0.80 and safe-wr<=0.08:
                    call1 = 1
                elif safe >= 0.85:
                    call1 = 1
                else:
                    fold1 = 1
        elif rua == 2:
            if small == 0:
                if wr>=0.84:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif "check" in message:
                    call1 = 1
                else: check1 = 1
            elif small == 1:
                if wr>=0.84:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif cb1 > 4000 or safe >= 0.78:
                    if safe-wr <= 0.08:
                        call1 = 1
                    elif safe >= 0.84:
                        call1 = 1
                    else:
                        fold1 = 1
                else:
                    fold1 = 1
        elif rua == 3:
            if small==0:
                if safe-rate>=0.64:
                    bet1=1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small==1:
                if safe-rate>0.66:
                    r1=1
                elif safe-rate>0.50:
                    call1=1
                else:
                    fold1=1
        else:
            if small==0:
                if cb2>1600 and safe>0.63:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif safe-rate>=0.56:
                    bet2=1
                else:
                    if "check" in message:
                        call1 = 1
                    else:
                        check1 = 1
            elif small==1:
                if cb2>1600 and safe>0.63:
                    if "allin" in message:
                        call1=1
                    else: allin1=1
                elif safe-rate>0.56:
                    r2=1
                elif safe-rate>0.37:
                    call1=1
                else:
                    fold1=1
        if fold1==1:
            print("决策：fold")
            sed("fold",sk)
            break
        elif check1==1:
            print("决策：check")
            sed("check",sk)
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        elif call1==1:
            print("决策：call")
            sed("call",sk)
            cb1=cb2
            ch1=20000-cb1
            message,teshu= rcv(sk,teshu)
            break
        elif bet1==1:
            a=R
            print("决策：bet "+str(a))
            sed("raise "+str(a),sk)
            cb1 = ct1+a
            ch1 = 20000-cb1
            PM = a
            if not PM == 0:
                R = PM * 2
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        elif r1==1:
            a = R
            print("决策：raise "+str(a))
            sed("raise "+str(a),sk)
            PM = a
            if not PM == 0:
                R = PM * 2
            cb1 = ct1+a
            ch1 = 20000 - cb1
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        elif bet2==1:
            c = 3*R
            print("决策：bet "+str(c))
            sed("raise "+str(c),sk)
            cb1 = ct1 + c
            ch1 = 20000-cb1
            PM = c
            if not PM ==0:
                R = 2 * PM
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        elif r2==1:
            c = 3*R
            print("决策：raise "+str(c))
            sed("raise "+str(c),sk)
            PM = c
            if not PM ==0:
                R = 2 * PM
            cb1 = ct1+c
            ch1 = 20000-cb1
            message,teshu = rcv(sk,teshu)
            if teshu == 1:
                break
        else:
            print("决策：allin")
            sed("allin",sk)
            cb1 = 20000
            ch1 = 0
            break
    while True:
        if  "earn" in message:
            money += int(message.split()[1])
            break
        else:
            message,teshu= rcv(sk,teshu)
            if teshu == 1:
                break
    if teshu == 1:
        continue
    number+=1
    print("本局结束---->money:"+str(money)+" number:"+str(number))
    # except:
    #     print("本局出现异常问题，从新启动本局----->>>")
    #     continue



















