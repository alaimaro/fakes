
from random import randint

import ecdsa
import time

def show_points(p, a, b):
    return [(x, y) for x in range(p) for y in range(p) if (y*y - (x*x*x + a*x + b)) % p == 0]
def findModReverse(v):
    v1=v
    v1[1]=-v[1]
    return v1
#print(show_points(p=23, a=1, b=1))
def add_points(point1, point2,curve):



    # 将点1和点2转换为曲线上的点对象
    p1 = ecdsa.ellipticcurve.Point(curve, point1[0], point1[1])
    p2 = ecdsa.ellipticcurve.Point(curve, point2[0], point2[1])

    # 计算点1和点2的和
    p3 = p1 + p2

    # 返回计算结果
    return [p3.x(), p3.y()]


# 实现 kC1
def Multiply(c1,k,curve):
    point = ecdsa.ellipticcurve.Point(curve, c1[0], c1[1])
    result_point = point * k
    return [result_point.x(),result_point.y()]

def Encryptkeyword(t, P, C,A, m,curve):

    r1 = randint(2, t-2)

    C_w = add_points(Multiply(C, m,curve),Multiply(A, r1,curve),curve)
    #print("Multiply(C, m):", Multiply(C, m,curve))
    #print("Multiply(A, r1):", Multiply(A, r1,curve))
    R = Multiply(P, r1,curve)
    #print("r1:", r1)
    #print("R:", R)
    return C_w, R

def Trapdoor(t, P, c,A,m2,curve):

    r2 = randint(2, t-2)

    #print("r2:",r2)
    y=Multiply(A, m2,curve)
    T_w = add_points(Multiply(y, c,curve),Multiply(A, r2,curve),curve)
    M = Multiply(P, r2,curve)
    return T_w,M

# 验证Test (𝑪_𝒘∙ 𝑹^(−𝒂))^a = 〖 𝑻〗_𝒘 𝑴^(−𝒂)
def Test(t, P, C_w,T_w, R,M,a,curve):
    v = Multiply(R, a,curve)


    v1=findModReverse(v)

    #print("v1:",v1)
    #print("R:",R)


    Left_v = Multiply(add_points(C_w,v1,curve),a,curve)
    x = Multiply(M, a,curve)
    Right_v = add_points(T_w , findModReverse(x),curve)
    print("Left_v:",Left_v)
    print("Right_v:",Right_v)
    if Left_v==Right_v:
        print("They are the same!")
    else:
        print("Nooooooooooo!")

def main():

    # 创建secp256k1曲线对象
    curve = ecdsa.SECP256k1.curve
    t = 2 ** 256 - 2 ** 32 - 2 ** 9 - 2 ** 8 - 2 ** 7 - 2 ** 6 - 2 ** 4 - 1
    #x,y =23,46
    m=1237
    #x1,y1=23,46
    m2=1237

    # base point
    #P=[55066263022277343669578718895168534326250603453777594175500187360389116729240,32670510020758816978083085130507043184471273380659243275938904335757337482424]
    # 获取基点G的对象
    G = ecdsa.SECP256k1.generator
    P = (G.x(), G.y())
    #print("P:", P)
    #print(show_points(t, a1, a2))
    a = randint(2, t-2)
    b = randint(2, t-2)
    c = randint(2, t-2)
    #print("a:", a)
    A = Multiply(P, a,curve)

    #print("A:", A)
    B = Multiply(P, b,curve)
    #print("b:", b)
    #print("B:", B)
    C = Multiply(P,c,curve)
    #print("c:", c)
    #print("C:", C)
    #t1 = time.time()
    #for i in range(1, 101):
    C_w,R = Encryptkeyword(t,P,C,A,m,curve)
    #t2 = time.time()

    #print("C_w:t:",(t2-t1))

    print("C_w:", C_w)

    #t3 = time.time()
    #for i in range(1, 101):
    T_w,M = Trapdoor(t,P,c,A,m2,curve)
    #t4 = time.time()
    #print("T_w:t:",(t4 - t3))
    print("T_w:", T_w)

    #t5 = time.time()
    #for i in range(1, 101):
    Test(t, P, C_w, T_w, R, M, a,curve)
    #t6 = time.time()
    #print("T_w:t:",(t4 - t3))

if __name__ == '__main__':
    main()