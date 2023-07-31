#try to impl ECDSA 
#from sympy import randprime
from hashlib import sha256
from random import randint
import random
import hashlib
from gmpy2 import invert

p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
q = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123

Px=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Py=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = (0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7, 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0)


#群的阶为q，P是加法群的生成元


# 点的加法运算
def point_add(P,Q):
    
    
    if P is None:
        return Q
    elif Q is None:
        return P
    elif P[0]==Q[0] and P[1]!=Q[1]:
        return None
    #elif P == point_neg(Q):
        return None

    x1, y1 = P[0], P[1]
    x2, y2 = Q[0], Q[1]
    
    if P == Q:
        lam = ((3 * x1 * x1 + a) * invert(2*y1,p)) % p
    else:
        lam = ((y2 - y1) * invert(x2-x1,p)) % p

    x3 = (lam * lam - x1 - x2) % p
    y3 = (lam * (x1 - x3) - y1) % p
    
    return (x3,y3)

# 点的取反运算
def point_neg(P):
    if P is None:
        return None

    x, y = P
    return x, (-y) % p

# 标量乘运算

def point_mul(P,h):
    h=h%q
    if h % q == 0 or P is None:
        return None

    if h < 0:
        #return point_neg(point_mul(-k, P))
        return point_mul(P,q-h)
    
    Q = None
    while h:
        if h & 1:
            Q = point_add(Q, P)
        P = point_add(P, P)
        h >>= 1
    return Q


#下面是库函数的hash_SM3    
def sm3_hash(data):
    hash_object = hashlib.new('sm3')
    hash_object.update(data)
    hash_value = hash_object.hexdigest()
    return hash_value

def key_gen():
    d = random.getrandbits(256) % q
    print('d',d)
    Q = point_mul(G,d)
    print('Q',Q)
    return (d,Q)

def signature(mes,d):
    k=random.getrandbits(256)%q
    R=point_mul(G,k)
    r=R[0]%q
    e=sm3_hash(mes.encode())
    e=int(e,16)
    s=(invert(k,q)*(e+d*r))%q
    return (r,s)

def signature_forge(P_Satoshi):
    u=random.getrandbits(256)%q
    v=random.getrandbits(256)%q
    R_forge=point_add(point_mul(G,u),point_mul(P_Satoshi,v))
    Rx_forge=R_forge[0]
    e_forge=(Rx_forge*u*invert(v,q))%q
    s_forge=(invert(v,q)*Rx_forge)%q
    print('伪造的签名是',(Rx_forge,s_forge))
    return (Rx_forge,s_forge),e_forge


    
def verify_sig(e,Q,sig):
    #e=sm3_hash(mes.encode())
    #e=int(e,16)
    r=sig[0]
    s=sig[1]
    w=invert(s,q)
    ewG=point_mul(G,e*w)
    #print('r',r)
    rwP=point_mul(Q,r*w)
    (r1,s1)=point_add(ewG,rwP)
    if r1==r:
        print('签名验证成功')
    else:
        print('签名验证失败')

if __name__ == "__main__":
    #mes='O my Luve is like a red, red rose,That is newly sprung in June,O my Luve is like the melodyThat is sweetly played in tune.RuoYan'
    #d,Q=key_gen()
    P_Satoshi=(26877259512020005462763638353364532382639391845761963173968516804546337027093,48566944205781153898153509065115980357578581414964392335433501542694784316391)
    #sig=signature(mes,d)
    sig_Satoshi=(41159732757593917641705955129814776632782548295209210156195240041086117167123, 57859546964026281203981084782644312411948733933855404654835874846733002636486)
    sig_forge,e_forge=signature_forge(P_Satoshi)
    verify_sig(e_forge,P_Satoshi,sig_forge)




