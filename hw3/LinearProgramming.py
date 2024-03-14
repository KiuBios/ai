from pulp import *

# 創建問題
prob = LpProblem("Maximize_Function", LpMaximize)

# 定義變數
x = LpVariable("x", lowBound=0)
y = LpVariable("y", lowBound=0)
z = LpVariable("z", lowBound=0)

# 定義目標函數
prob += 3*x + 2*y + 5*z

# 添加約束
prob += x + y <= 10
prob += 2*x + z <= 9
prob += y + 2*z <= 11

prob.solve()

print("最大值:", value(prob.objective))
print("x:", value(x))
print("y:", value(y))
print("z:", value(z))
