# 导入XGO库和时间模块
from xgolib import XGO
import time

# 初始化机器狗对象
dog = XGO("xgolite")

# 假设我们有一个函数check_condition()来检测是否满足条件
def check_condition():
    # 这里应该是条件检测的代码，现在我们简单返回True
    return True
# 机器狗根据条件判断进行运动
while not check_condition():
    dog.move('x', 10)  # 前进
    time.sleep(0.5)
    dog.move('x', -10)  # 后退
    time.sleep(0.5)
    print('Keep moving!')

dog.stop()


