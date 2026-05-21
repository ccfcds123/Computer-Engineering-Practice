# 导入XGO库和时间模块
from xgolib import XGO
import time
# 初始化机器狗对象
dog = XGO("xgolite")

# 机器狗前进和后退的循环
steps = 5  # 步数
step_length = 30  # 每步长度
for _ in range(steps):
    dog.move('x', step_length)  # 前进
    time.sleep(1)
    dog.move('x', -step_length)  # 后退
    time.sleep(1)

dog.stop()

