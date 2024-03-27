import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm
from micrograd2023.engine import Value

# x = np.array([0, 1, 2, 3, 4], dtype=np.float32)
# y = np.array([2, 3, 4, 5, 6], dtype=np.float32)
x = np.array([Value(0), Value(1), Value(2), Value(3), Value(4)])
y = np.array([Value(1.9), Value(3.1), Value(3.9), Value(5.0), Value(6.2)])

def predict(a, xt):
	return a[0]+a[1]*xt

def MSE(a, x, y):
	total = 0
	for i in range(len(x)):
		total += (y[i]-predict(a,x[i]))**2
	return total

def loss(p):
	return MSE(p, x, y)

# 使用梯度下降法尋找函數最低點
def gradientDescendent(f, p0, h=0.01, max_loops=100000, dump_period=1000):
    p = p0.copy()
    for i in range(max_loops):
        fp = f(p)
        fp.backward() # 計算梯度
        gp = []
        for j in p :
            gp.append(j.grad)
        glen = norm(gp) # norm = 梯度的長度 (步伐大小)
        if i%dump_period == 0: 
            print(i,':f(p)=',fp ,'p=',str(p), 'gp= ',str(gp) ,'glen= ',round(glen,5))
            #print('{:05d}:f(p)={:.3f} p={:s} gp={:s} glen={:.5f}'.format(i, fp, str(p), str(gp), glen))
        if glen < 0.00001: # 如果步伐已經很小了，那麼就停止吧！
            break
        gh = np.multiply(gp, -1*h) # gh = 逆梯度方向的一小步
        p +=  gh # 向 gh 方向走一小步
    #print(i,':f(p)=',fp ,'p=',str(p), 'gp= ',str(gp) ,'glen= ',glen)
    print(i,':f(p)=',fp ,'p=',str(p), 'gp= ',str(gp) ,'glen= ',round(glen,5))
    return p # 傳回最低點！

p = [Value(0.0), Value(0.0)]
plearn = gradientDescendent(loss, p, max_loops=3000, dump_period=1)
# Plot the graph
y_predicted = list(map(lambda t: plearn[0]+plearn[1]*t, x))
print('y_predicted=', y_predicted)

# Extracting numerical values from Value objects
x_values = [v.data for v in x]
y_values = [v.data for v in y]
y_predicted_values = [v.data for v in y_predicted]

# Plot the graph
plt.plot(x_values, y_values, 'ro', label='Original data')
plt.plot(x_values, y_predicted_values, label='Fitted line')
plt.legend()
plt.show()
