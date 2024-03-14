from random import random, randint, choice, uniform
import numpy as np


x1 = 0
x2 = 0

while .32*x1 + .22*x2 < 8 or .11*x1 + .09*x2 < 3 or .15*x1 + .10*x2 < 4 :   
     x1 = randint(0,50)
     x2 = randint(0,50)


def price(a, b):
     p = 35*a + 25*b
     return p

def neighbor(x1, x2):    # 雙變數解答的鄰居函數。
        nx1 = x1
        nx2 = x2
        nx1 = uniform(0,50)
        nx2 = uniform(0,50)
        while .32*nx1 + .22*nx2 < 8 or .11*nx1 + .09*nx2 < 3 or .15*nx1 + .10*nx2 < 4 :
            nx1 = uniform(0,50)
            nx2 = uniform(0,50)
        return nx1, nx2      # 建立新解答並傳回。


def hillClimbing(x1, x2, price, neighbor, max_fail):
    print("start: x1 = ", x1, ", x2 = ", x2)             # 印出初始解
    fail = 0
    gens = 0
    while True:
        n1, n2 = neighbor(x1, x2)
        #print(n1,n2,x1,x2)
        if price(n1, n2) < price(x1, x2):
            x1, x2 = n1, n2
            gens += 1
            print(gens,  ':', price(x1, x2), x1, x2)
            fail = 0
        else:
            fail += 1
            if fail > max_fail:
                print("solution: price = ", price(x1, x2), "x1 = ", x1, "x2 = ", x2)
                return x1, x2

# 執行爬山演算法
hillClimbing(x1, x2, price, neighbor, max_fail=10000)
