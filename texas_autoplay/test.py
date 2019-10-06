import  re

t = "fold|earn -200preflop|<2,3>"
t1 = int(re.search("earn (.*?)preflop",t).group(1))
print(t1)