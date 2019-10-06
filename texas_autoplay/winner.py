

def judge_winner(type1,hands1,type2,hands2):           #输入牌型1，手牌1，牌型2，手牌2；输出result（胜负信号）和tie（平手信号）  result为1时，2者胜；为0时，1者胜   tie为1时为平手
    if type1>type2:
        return  0,0
    elif type1<type2:
        return  1,0
    else:
        if type1==0:
            for i in range(0,5):
                if int(hands1[i][:3],16)>int(hands2[i][:3],16):
                    return 0,0
                elif int(hands1[i][:3],16)<int(hands2[i][:3],16):
                    return 1,0
                else:
                    continue
            return 0,1
        elif type1==1:
            for i in range(0,5):
                if int(hands1[i][:3],16)>int(hands2[i][:3],16):
                    return 0,0
                elif int(hands1[i][:3],16)<int(hands2[i][:3],16):
                    return 1,0
                else:
                    continue
            return 0,1
        elif type1==2:
            for i in range(0,5):
                if int(hands1[i][:3],16)>int(hands2[i][:3],16):
                    return 0,0
                elif int(hands1[i][:3],16)<int(hands2[i][:3],16):
                    return 1,0
                else:
                    continue
            return 0,1
        elif type1==3:
            for i in range(0,5):
                if int(hands1[i][:3],16)>int(hands2[i][:3],16):
                    return 0,0
                elif int(hands1[i][:3],16)<int(hands2[i][:3],16):
                    return 1,0
                else:
                    continue
            return 0,1
        elif type1==4:
            hands1.reverse()
            hands2.reverse()
            for i in range(0,5):
                if int(hands1[i][:3],16)>int(hands2[i][:3],16):
                    return 0,0
                elif int(hands1[i][:3],16)<int(hands2[i][:3],16):
                    return 1,0
                else:
                    continue
            return 0,1
        elif type1==5:
            mid1 = [  int(i[:3],16)  for i in hands1]
            mid2 = [  int(i[:3],16)  for i in hands2]
            mid1.sort()
            mid2.sort()
            for i in range(0,5):
                if mid1[i]>mid2[i]:
                    return 0,0
                elif mid1[i]<mid2[i]:
                    return 1,0
                else:
                    continue
            return 0,1
        elif type1==6:
            for i in range(0,5):
                if int(hands1[i][:3],16)>int(hands2[i][:3],16):
                    return 0,0
                elif int(hands1[i][:3],16)<int(hands2[i][:3],16):
                    return 1,0
                else:
                    continue
            return 0,1
        elif type1==7:
            for i in range(0,5):
                if int(hands1[i][:3],16)>int(hands2[i][:3],16):
                    return 0,0
                elif int(hands1[i][:3],16)<int(hands2[i][:3],16):
                    return 1,0
                else:
                    continue
            return 0,1
        elif type1==8:
            hands1.reverse()
            hands2.reverse()
            for i in range(0, 5):
                if int(hands1[i][:3], 16) > int(hands2[i][:3], 16):
                    return 0, 0
                elif int(hands1[i][:3], 16) < int(hands2[i][:3], 16):
                    return 1, 0
                else:
                    continue
            return 0, 1



