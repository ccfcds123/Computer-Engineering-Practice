# 导入XGO库和时间模块
from xgolib import XGO
import time

# 初始化机器狗对象
dog = XGO("xgolite")

# 机器狗原地踏步，抬腿高度为20mm
dog.mark_time(20)
# 踏步持续3秒
time.sleep(3)

# 停止原地踏步
dog.reset()

dog.stop()