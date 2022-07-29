# coding = utf-8

import world
from world import x as x2 #加点时会引用的是主文件 报错 No module named '__main__.world'; '__main__' is not a package

x = "111"

print(x2)
print(x)
print(world.z)
