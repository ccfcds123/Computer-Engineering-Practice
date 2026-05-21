# 导入XGO库
from xgolib import XGO
# 导入时间库
import time

# 初始化机器狗对象
dog = XGO("xgolite")

# 机器狗前进50mm
dog.move('x', 50)
# 等待2秒
time.sleep(2)

# 机器狗后退50mm
dog.move('x', -50)
# 再次等待2秒
time.sleep(2)

dog.stop()