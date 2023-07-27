import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")

x = np.array([1,2,3,4,5,6])
y = np.array([22,33,44.3,56.1,68.35,81.1])

# 计算回归系数
[slope, intercept] = np.polyfit(x,y,1)

# 绘制拟合曲线
plt.scatter(x, y)
plt.plot(x, slope * x + intercept, color='red')
plt.xlabel("i")
plt.ylabel("V(i)")
plt.title("V(i)={:.4f}i+{:.4f}".format(slope,intercept))
plt.show()
