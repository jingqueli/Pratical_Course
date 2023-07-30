from hashlib import sha256
from hmac import HMAC
#from ecpy.curves import Curve
#from ecpy.keys import ECPrivateKey
from sm2_myself import *
import hashlib


def hmac_sha256_kdf(key: bytes, data: bytes, length: int) -> bytes:
    return HMAC(key, data, sha256).digest()[:length]

def generate_k(mes,d):
    #q = sm2_curve.field
    #n = sm2_curve.order
    #G = sm2_curve.generator

    #d = private_key.d
    m=sm3_hash(mes.encode()).encode()
    
    h = sha256(m).digest()

    xlen = (p.bit_length() + 7) // 8
    hlen = len(h)
    v = b'\x01' * hlen
    k = b'\x00' * hlen

    k = hmac_sha256_kdf(k, v + b'\x00' + d.to_bytes(xlen, 'big') + h, hlen)
    v = hmac_sha256_kdf(k, v, hlen)
    k = hmac_sha256_kdf(k, v + b'\x01' + d.to_bytes(xlen, 'big') + h, hlen)
    v = hmac_sha256_kdf(k, v, hlen)

    while True:
        t = b''
        while len(t) < xlen:
            v = hmac_sha256_kdf(k, v, hlen)
            t += v

        k_candidate = int.from_bytes(t[:xlen], 'big')
        if 1 <= k_candidate < q:
            return k_candidate

        k = hmac_sha256_kdf(k, v + b'\x00', hlen)
        v = hmac_sha256_kdf(k, v, hlen)

# 示例用法：

if __name__=='__main__':
    #d_A=randint(2,q-1)
    ENTL_A='ENTLA'
    ID_A='RuoYan'
    mes='O my Luve is like a red, red rose,That is newly sprung in June,O my Luve is like the melodyThat is sweetly played in tune.'
    #M初始为字符串类型
    G=(Px,Py)
    d_A,Q=key_gen()
    k_with_RFC6979 = generate_k(mes,d_A)
    print('k_with_RFC6979 :',k_with_RFC6979)
    #print('Q',Q)
    x_A=Q[0]#分别取出x and y
    y_A=Q[1]
    ZA=Precompute(ENTL_A,ID_A,x_A,y_A)

    sig,P_A=signature(ENTL_A,ID_A,d_A,mes,k_with_RFC6979)
    verify_signature(sig,mes,P_A,ENTL_A,ID_A)



