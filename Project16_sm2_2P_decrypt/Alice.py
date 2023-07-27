import socket
from sm2_myself import *
import json
import random
from gmpy2 import invert
from gmpy2 import mpz

def Key_Gene(d1,d2):
    private_key=invert(d1*d2,q)-1
    public_key=point_mul(G,private_key)
    return private_key,public_key

def Encrypt(P,M):
    k=random.getrandbits(256)%q
    C1=point_mul(G,k)
    (x2,y2)=point_mul(P,k)
    t=KDF(str(x2)+'|'+str(y2),k.bit_length())
    #t为字符串类型
    byte_stream1=M.encode()
    byte_stream2=t.encode()
    if(len(M)>=len(t)):
        C2 = bytes(a ^ b for a, b in zip(byte_stream1, byte_stream2))
    else:
        length = min(len(byte_stream1), len(byte_stream2))
        # 对字节流进行异或操作，只计算到较短字节流的长度
        C2 = bytes(a ^ b for a, b in zip(byte_stream1[:length], byte_stream2[:length]))
    C3=str(x2)+M+str(y2)
    C3=sm3_hash(C3.encode())
    C_dict={'C1':C1,'C2':C2,'C3':C3}
    return C_dict,k

def Decrypt(T2,C1,C2,C3,klen):
    re_C1=point_neg(C1)
    (x2,y2)=point_add(T2,re_C1)
    t=KDF(str(x2)+'|'+str(y2),klen)
    byte_stream1=C2
    byte_stream2=t.encode()
    if(len(C2)>=len(t)):
        M = bytes(a ^ b for a, b in zip(byte_stream1, byte_stream2))
    else:
        length = min(len(byte_stream1), len(byte_stream2))
        # 对字节流进行异或操作，只计算到较短字节流的长度
        M = bytes(a ^ b for a, b in zip(byte_stream1[:length], byte_stream2[:length]))
    M=M.decode()
    u=str(x2)+M+str(y2)
    u=sm3_hash(u.encode())
    if(u==C3):
        print('解密成功')
        print(M)
        return None
    else:
        print('解密失败')
        return None
    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port_Alice = 12345   # 设置端口
port_Bob=10001
s.bind((host, port_Alice))        # 绑定端口
addr=(host,port_Bob)

while True:
    d1=random.getrandbits(256)%q
    #1
    mes,addr=s.recvfrom(4096*16)
    print("Received message from :",addr)
    d2=int(mes.decode(),10)

    private_key,public_key=Key_Gene(d1,d2)
    M='RuoYan'#M定义为字符串类型
    private_key,public_key=Key_Gene(d1,d2)
    C_dict,k=Encrypt(public_key,M)
    klen=k.bit_length()
    T1=point_mul(C_dict['C1'],invert(d1,q))
    #2
    s.sendto(str(T1).encode(),addr)
    #3
    mes,addr=s.recvfrom(4096*16)
    print("Received message from :",addr)
    T2=tuple(mpz(x) for x in eval(mes.decode()))
    #T2=int(T2,10)
    Decrypt(T2,C_dict['C1'],C_dict['C2'],C_dict['C3'],klen)
    break
s.close()
    
    

