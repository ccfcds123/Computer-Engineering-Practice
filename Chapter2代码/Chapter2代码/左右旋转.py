# 导入XGO库
from xgolib import XGO
# 导入时间库
import time

# 初始化机器狗对象
dog = XGO("xgolite")

# 机器狗左转90°/s
dog.turn(90)
time.sleep(2)

# 机器狗右转90°/s
dog.turn(-90)
time.sleep(2)

dog.stop()