from collections import Counter


# 's'----------->黑桃
# 'c'----------->梅花
# 'h'----------->红桃
# 'd'----------->方片
#  皇家同花顺-->同花顺-->四条-->葫芦-->同花-->顺子-->三条-->两对-->对子-->高牌
#  牌值的表示形式：'0xbc'  前三位用16进制表示数值，最后一位表示花色

class judge_pattern:
    def __init__(self,list):
        self.poke=list
        self.poke_number_single= [list[0][:3],list[1][:3],list[2][:3],list[3][:3],list[4][:3],list[5][:3],list[6][:3]]
        self.poke_attr_single= [list[0][3],list[1][3],list[2][3],list[3][3],list[4][3],list[5][3],list[6][3]]
        self.poke_array = [self.poke_number_single,self.poke_attr_single]

    def judge_SITIAO(self):                #直接调用，返回 true/false 和 牌型

        cout = dict(Counter(self.poke_array[0]))
        # times = {v: k for k, v in cout.items()}        翻转字典
        fuben = self.poke_array[0][:]
        index = []
        pokes = []
        tab = None
        for i in range(0,len(cout.values())):
            if list(cout.values())[i] == 4:
                tab = list(cout.keys())[i]
        if tab:
            for j in range(0,len(fuben)):
                try:
                    index.append(fuben.index(str(tab)))
                    fuben[fuben.index(str(tab))]='0x0'
                except:
                    break
            for k in range(0,len(fuben)):
                fuben[k]=int(fuben[k],16)
            fuben.sort(reverse=True)
            index.append(self.poke_array[0].index(str(hex(fuben[0]))))
            for k in index:
                pokes.append(self.poke[k])
            return True,pokes
        else:
            return False,pokes

    def judge_HULU_mid(self):                     #判断是否为葫芦，是否为三条，是否为两对，是否为对子，和高牌的牌型 注：使用前提是已经判断过同花、顺子和四条
        cout = dict(Counter(self.poke_array[0]))               #返回值表示：1-->葫芦  2-->三条   3-->两对  4-->对子   5-->高牌
        santiao_number = []          #记录三条
        duizi_number = []            #记录对子
        santiao=[]                   #记录组成三条的牌的位置
        duizi=[]                     #记录组成对子的牌的位置
        for i,j in cout.items():
            if j == 3:
                santiao_number.append(hex(int(i,16)))
            elif j == 2:
                duizi_number.append(hex(int(i,16)))
            else:
                continue
        santiao_number.sort(reverse=True)
        duizi_number.sort(reverse=True)
        fuben = self.poke_array[0][:]
        for k in range(0,len(fuben)):
            try:
                santiao.append(fuben.index(str(santiao_number[0])))
                fuben[fuben.index(str(santiao_number[0]))]='0x0'
            except:
                continue
        for j in range(0,len(fuben)):
            try:
                duizi.append(fuben.index(str(duizi_number[0])))
                fuben[fuben.index(str(duizi_number[0]))]='0x0'
            except:
                continue
        mid = []                     #mid是fuben的复制，不过元素是以16进制数形式
        for i in fuben:
            mid.append(hex(int(i,16)))
        if santiao and duizi:
            pokes = []
            for i in santiao:
                pokes.append(self.poke[i])
            for j in duizi:
                pokes.append(self.poke[j])
            return True,pokes,1                     #返回葫芦牌型
        elif santiao:
            number = []
            for i in range(0,2):
                try:
                    number.append(mid.index(max(mid)))
                    mid[mid.index((max(mid)))]='0x0'
                except:
                    continue
            pokes = []
            for i in santiao:
                pokes.append(self.poke[i])
            for j in number:
                pokes.append(self.poke[j])
            return False,pokes,2                       #返回三条牌型
        elif len(duizi_number)>=2:
            pokes = []
            for i in  range(0,2):
                for j in range(0, len(fuben)):
                    try:
                        duizi.append(mid.index(str(duizi_number[i])))
                        mid[mid.index(str(duizi_number[i]))] = '0x0'
                    except:
                        continue
            for k in duizi:
                pokes.append(self.poke[k])
            pokes.append(self.poke[mid.index(max(mid))])
            return False,pokes,3                        #返回两对牌型
        elif len(duizi_number) == 1:
            pokes = []
            for i in duizi:
                pokes.append(self.poke[i])
            for i in range(0,3):
                try:
                    pokes.append(self.poke[mid.index(max(mid))])
                    mid[mid.index(max(mid))]='0x0'
                except:
                    continue
            return False,pokes,4                         #返回一对牌型
        else:
            pokes=[]
            for i in range(0,5):
                pokes.append(self.poke[mid.index(max(mid))])
                mid[mid.index(max(mid))]='0x0'
            return False,pokes,5                        #返回高牌牌型

    def judge_HULU(self):
        yorn, pokes, typ = self.judge_HULU_mid()
        if typ == 1:
            return True, pokes
        else:
            return False, []

    def judge_SANTIAO(self):              #直接调用，返回 true/false 和 三条的牌
        yorn,pokes,typ = self.judge_HULU_mid()
        if typ == 2:
            return True,pokes
        else:
            return False,[]

    def judge_LIANGDUI(self):
        yorn, pokes, typ = self.judge_HULU_mid()
        if typ == 3:
            return True, pokes
        else:
            return False,[]

    def judge_DUIZI(self):
        yorn, pokes, typ = self.judge_HULU_mid()
        if typ == 4:
            return True, pokes
        else:
            return False, []

    def judge_GAOPAI(self):
        yorn, pokes, typ = self.judge_HULU_mid()
        if typ == 5:
            return True, pokes
        else:
            return False, []

    def judge_SHUNZI_mid(self):                        #求所有能组成顺子的牌
        i = None
        all_all_sign =  False
        pokes = []
        for i in range(0xe,0x5,-1):            #sort之后断点连续查值 比这个应该要高效
            all_sign = True
            pokes_mid= []
            for k in range(i-4,i+1):
                sign = False
                for j in range(0,7):  #循环判断7张牌里有没有顺子要有的数
                    if k == int(self.poke_array[0][j],16):
                        pokes_mid.append(j)   #如果有，选出这张牌
                        sign = True
                if sign == True:     #如果找到这一位，判断下一位
                    continue
                else:                #如果没找到这一位，all_sign为假
                    all_sign=False
                    break
            if all_sign == False:    #如果该顺子组合不符合，判断下一个顺子组合
                continue
            else:
                all_all_sign=True    #如果该顺子组合成立，all_all_sign为真
                pokes = [self.poke_array[0][x]+self.poke_array[1][x] for x in pokes_mid]
                break
        if all_all_sign == True:
            return pokes
        else:
            pokes_mid= []
            all_sign = True
            for j in range(0x1,0x6):
                sign = False
                if j == 0x1:
                    for k in range(0,7):
                        if int(self.poke_array[0][k],16) == 14:
                            sign = True
                            pokes_mid.append(k)
                else:
                    for k in range(0,7):
                        if int(self.poke_array[0][k],16) == j:
                            sign = True
                            pokes_mid.append(k)
                if sign == True:
                    continue
                else:
                    all_sign=False
                    break
            if all_sign == True:
                pokes = [self.poke_array[0][x] + self.poke_array[1][x] for x in pokes_mid]
                return pokes
            else:
                return pokes

    def judge_TONGHUA(self):                                 #直接调用，返回 true/false 和 牌型
        poke_attr = self.poke_array[1]
        attr = {'s':[],'d':[],'h':[],'c':[]}
        pokes_mid = []
        pokes = []
        for i in range(0,len(self.poke_array[1])):
            attr[self.poke_array[1][i][0]].append(i)
        for j in attr:
            if len(attr[j])>=5:
                pokes_mid = attr[j][:]
        if pokes_mid:
            list={}
            for i in pokes_mid:
                list[i] = int(self.poke_array[0][i],16)
            sorted(list.items(),key = lambda x:x[1],reverse = True)         #字典以value排序
            for j in list:
                pokes.append(self.poke[j])
            return True,pokes
        else:
            return False,pokes


    def judge_TONGHUASHUN(self,judge_type=1):        #judge_type取1时，判断是否为同花顺；为2时，仅判断是否为顺子；返回牌型
        list = self.judge_SHUNZI_mid()
        if judge_type == 2:
            if list:
                return True,list
            else:
                return False,list
        else:
            attr = {'c': 0, 's': 0, 'd': 0, 'h': 0}
            pokes = []
            def re(i,attr,pokes):
                if i==len(list):
                    for l in attr :
                        if attr[l] == 5:
                            return True,pokes
                    return False,list
                else:
                    if i == len(list)-1:
                        attr[list[i][3]] += 1
                        pokes.append(list[i])
                        return re(i + 1, attr, pokes)
                    elif int(list[i][:3],16) == int(list[i+1][:3],16):
                            return re(i+1,attr,pokes)
                    else:
                        attr[list[i][3]]+=1
                        pokes.append(list[i])
                        return re(i+1,attr,pokes)
            return re(0,attr,pokes)

    def judge_SHUNZI(self):                                    #返回非同花顺子的牌型
        x,array = self.judge_TONGHUASHUN(1)
        pokes = []
        if array:
            for  i in range(0,len(array)) :
                if i == len(array)-1:
                    pokes.append(array[i])
                elif int(array[i][:3],16) ==  int(array[i+1][:3],16):
                    continue
                else:
                    pokes.append(array[i])
            return True,pokes
        else:
            return False,pokes
