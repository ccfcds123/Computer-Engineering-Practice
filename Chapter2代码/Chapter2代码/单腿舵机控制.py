# 导入XGO库和时间模块
from xgolib import XGO
import time

# 初始化机器狗对象
dog = XGO("xgolite")

dog.leg(2,[10,-12,90])

time.sleep(3)

# 停止原地踏步
dog.reset()

dog.stop()

