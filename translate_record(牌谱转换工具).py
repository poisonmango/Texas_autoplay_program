import os
import re

file_name = input("请输入文件名：")
file = open(file_name,"r+")
file_write = open(file_name[:-4]+"_translate.txt",'w')
all = file.readline()
times = 0
for i in all:
    if all.find(';')<0:
        break
    dex = all.find(';')
    file_write.write(all[:dex+1]+'\n')
    all = all[dex+1:]
    print("完成第" + str(times + 1) + "个转换")
    times+=1
file_write.write(all)
file.close()
file_write.close()
print("完成")
