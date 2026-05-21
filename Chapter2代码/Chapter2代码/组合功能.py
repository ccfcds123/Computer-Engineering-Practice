# 导入XGO库
from xgolib import XGO
# 导入时间库
import time

# 初始化机器狗对象
dog = XGO("xgolite")

def move_and_turn():
    # 前进100mm
    dog.move('x', 100)
    time.sleep(2)

    # 旋转180°，即调头
    dog.turn(180)
    time.sleep(2)

    # 掉头后前进100mm返回原点
    dog.move('x', 100)
    time.sleep(2)

# 调用函数
move_and_turn()

dog.stop()