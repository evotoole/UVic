import math as m

x1 = 198
x2 = 140
x3 = 133
x_arr = [x1,x2,x3]
n1 = 400
n2 = 350
n3 = 350
n_arr = [n1,n2,n3]
p_h0 = 471/1100

answer = 0
for index in range(0,3):
    answer += (x_arr[index])*m.log(x_arr[index]/(n_arr[index]*p_h0)) + (n_arr[index] - x_arr[index])\
    *m.log((n_arr[index] - x_arr[index])/(n_arr[index]*(1-p_h0)))

print(answer) 