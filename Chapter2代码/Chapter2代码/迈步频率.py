# 导入XGO库和时间模块
from xgolib import XGO
import time

# 初始化机器狗对象
dog = XGO("xgolite")

# 将迈步频率设置为快速
dog.pace('fast')
# 机器狗前进150mm
dog.move('x', 150)
time.sleep(2)
# 恢复默认迈步频率
dog.pace('normal')


dog.stop()

