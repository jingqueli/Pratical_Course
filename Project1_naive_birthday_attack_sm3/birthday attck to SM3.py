import hashlib
import binascii
import struct
import random
import string
from time import time
IV0=[0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
     0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
#bin()的结果类型是字符串
mask=0xFFFFFFFF#按位取反掩码
#IV=[]
def P1(byte_str):#跟别人的有不同，移位位数不同
    #输入的x的类型是字节串
    byte_int=int(byte_str.hex(),16)
    a=left_rotate(byte_int,9)
    #print('byte_int',byte_int)
    #print(a)
    a=int(a,16)
    #print(a)
    #print('hexa',hex(a))
    b=right_rotate(byte_int,23)
    b=int(b,16)
    P=byte_int^(a | b)#这时得到的结果为int
    return P
    
def P0(num):#接收十进制整数
    a=int(left_rotate(num,9),16)
    b=int(left_rotate(num,17),16)
    re=(num | a)
    re=(num | b)
    #re是十进制数
    return re
    
def byte_stream_xor(c,d):
    #接收两个字节串，返回一个字节串
    result = bytes([a ^ b for a, b in zip(c, d)])
    return result

def T_func(i):
    if(i<=15):
        return '79cc4519'
    else:
        return '7a879d8a'
    #十六进制字符串

def ff(A,B,C):
    return (A & B) | ((A^mask) & C)#接收三个整数，返回一个整数（十进制）

def gg(X,Y,Z):
    return  (X & Y) | (X & Z) | (Y & Z)
    
def compression_func(IV_0,data):
    #首先是消息扩展，传入的参数是明文的分组(字节流形式)
    #传入的消息是512bit，是64字节,64字节对应64个字符
    W=[]
    #应该拆成四字节，每四个字节是一个字
    for i in range(0,16):
        
        W.append(data[i*4:(i+1)*4])#w里面装的是字节串
        #if(data[i*4:(i+4)*4]==' ')
    
    #print(W)
    #前十六个应该是没问题
    for i in range(16,68):
        P1_data=byte_stream_xor(W[i-16],W[i-9])
        #print('P1_data',P1_data)
        hex_int=int(W[i-3].hex(),16)#直接一步到位把w中的字节串转为10进制数
            
        #print(hex_int)
        #转为16进制整数的目的是进行循环移位(转不成，还是弄成十进制数了)
        #在进行字节流异或时需要转换回去
        hex_str=left_rotate(hex_int,15)[2:]#循环左移15位,得到十六进制字符串
        decimal_integer=int(hex_str,16)#将十六进制字符串转换为十进制整数
        #print('hex_str',hex_str)
        byte_string = decimal_integer.to_bytes((decimal_integer.bit_length() + 7) // 8, 'big')#十进制整数转为字节串
        
        #if(hex_str!='0'):
        #    byte_hex=bytes.fromhex(hex_str)#转换为字节串
        #if(hex_str=='0'):
        #    byte_hex=b'0'
        if(byte_string==b''):
            byte_string=b'\x00\x00\x00\x00'
        #print('byte_string',byte_string)
        P1_data=byte_stream_xor(P1_data,byte_string)
        #P1_data也是四字节的
        #print("即将输入P1函数的数据是",P1_data)
        P1_re=P1(P1_data)&mask#P1_re  is  int
        #P1_re一直都是四字节的数据（整数，十进制）
        hex_int=int(W[i-13].hex(),16)&mask
        #print(hex(hex_int))
        #hex_int是十进制整数
        hex_int2=int(W[i-6].hex(),16)&mask
        #print(hex(hex_int2))
        re=(P1_re^hex_int^hex_int2)&mask#得到十进制整数
        #print('re:',re)
        W.append(str(re).encode())#也是按十六进制编码
        #print('Wi:',W[i])
    for i in range(68,132):
        op_num=int(W[i-68].hex(),16)
        op_num2=int(W[i-64].hex(),16)
        op_num=op_num^op_num2
        W.append(hex(op_num).encode())
    #print('W输出',W)
    #以上是消息扩展
    #SS1
    A=IV_0[0]#是整数
    B=IV_0[1]
    C=IV_0[2]
    D=IV_0[3]
    E=IV_0[4]
    F=IV_0[5]
    G=IV_0[6]
    H=IV_0[7]
    for i in range(0,32):
        A_shift=left_rotate(A,12)#0x str
        A_shift=int(A_shift,16)
        Tj=T_func(i)#Tj是十六进制字符串
        Tj=int(Tj,16)
        Tj_shift=int(left_rotate(Tj,i),16)
        SS1=(A_shift+E+Tj_shift)&mask#与掩码做或，只取低32位,操作后得到整数(十进制)
        SS1=int(left_rotate(SS1,7),16)
        SS2=SS1^A_shift#SS2为整数，十进制
        TT1=ff(A,B,C)+D+SS2+int(W[i+68].hex(),16)#TT1是整数，十进制
        TT2=gg(E,F,G)+H+SS1+int(W[i].hex(),16)#十进制
        D=C#D是十六进制
        C=int(left_rotate(B,9),16)#C是十六进制
        B=A#16进制
        A=int(hex(TT1),16)#十六进制
        H=G
        G=int(left_rotate(F,19),16)#十六进制
        F=E
        E=int(hex(P0(TT2)),16)#16进制
        #循环一轮后，更新的A-H仍然全都是十六进制数
    IV=[]
    IV.append(int(hex(IV_0[0]^A),16)&mask)
    IV.append(int(hex(IV_0[1]^B),16)&mask)
    IV.append(int(hex(IV_0[2]^C),16)&mask)
    IV.append(int(hex(IV_0[3]^D),16)&mask)
    IV.append(int(hex(IV_0[4]^E),16)&mask)
    IV.append(int(hex(IV_0[5]^F),16)&mask)
    IV.append(int(hex(IV_0[6]^G),16)&mask)
    IV.append(int(hex(IV_0[7]^H),16)&mask)
    return IV
    

def left_rotate(num, shift):#需要的参数是整数,可以是十六进制
    num_bits = 32
    shift=shift%32
    shifted_num = ((num << shift) | (num >> (num_bits - shift))) & ((1 << num_bits) - 1)
    
    return hex(shifted_num)

def right_rotate(num,shift):#同上
    num_bits=32
    shift=shift%32
    shifted_num=((num<<(num_bits-shift)) | (num>>shift)) & ((1<<num_bits)-1)
    return hex(shifted_num)


def padding_func(data):
    binary_data = ''.join(format(byte, '08b') for byte in data)
    #print(binary_data)
    


    #len()输出字节流长度
    length=len(data)*8#length of bit stream
    #print('length',length)
    bin_length=bin(length)[2:]
    #print('消息的二进制长度为:',len(bin_length))
    padding_length=64-len(bin_length)
    #所以padding_length是在长度位上不满64位填充的0，和表示长度的bin_length之和应该是64位
    padding_length='0'*padding_length
    
    data_remaining_length=len(bin_length)%512
    length0=512-length-64-1#该数值表示需要填充的零的个数
    pad0='0'*length0
    binary_string=binary_data+'1'+pad0+padding_length+bin_length
    #print('binary_string长度',len(binary_string))

    #以下将二进制字符串转换为字节串
    byte_array = bytearray()
    for i in range(0, len(binary_string), 8):
        byte = int(binary_string[i:i+8], 2)  # 将每个八位二进制数转换为整数
        byte_array.append(byte)  # 添加到字节串中

    bytes_result = bytes(byte_array)  # 转换为字节串
    return bytes_result
    
def seg_func(data):
    #输入信息类型为bit stream
    #data=b'Hello World You are so happy'
    IV=[]
    group_number=int(len(data)/64)+1#64byte per group
    #print("group number",group_number)
    if(group_number==1):
        padding_data=padding_func(data[:])
        IV=compression_func(IV0,padding_data)
        for i in range(0,8):
            IV[i]=hex(IV[i])[2:]
        padded_IV=[s.zfill(8) for s in IV]
        final_IV=''.join(padded_IV)
        return final_IV
    for i in range(0,group_number):
        if(i==0):
            IV=compression_func(IV0,data[0:64])
            continue
        if(i==group_number-1):
            padding_data=padding_func(data[64*i:])
            #获得填充后信息
            IV=compression_func(IV,padding_data)
            for i in range(0,8):
                IV[i]=hex(IV[i])[2:]
            padded_IV = [s.zfill(8) for s in IV]
            final_IV=''.join(padded_IV)
            return final_IV
        else:
            IV=compression_func(IV,data[64*i:64*(i+1)])
            continue
        

#下面是库函数的hash_SM3    
def sm3_hash(data):
    hash_object = hashlib.new('sm3')
    hash_object.update(data)
    hash_value = hash_object.hexdigest()
    return hash_value

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.sample(characters, length))
    return random_string
def f(x,n):
    x=(x**2)%n
    return x

#1测试手写sm3时间
data=b'I am not superman,I am joker akdjmfkalsd aslkdjfalks qwlkejtrflkqwje'
t1=time()
re1=seg_func(data)
print(re1)
t2=time()
print('sm3_myself take time:',(t2-t1),'s')
#2 测试库函数sm3时间
t1=time()
print(sm3_hash(data))
t2=time()
print('sm3 by library function take time:',(t2-t1),'s')
#3进行朴素生日攻击并测试时间
Index=3#标志要寻找多少位的碰撞
t1=time()
while True:#朴素的生日攻击，随机选取消息计算hash寻找碰撞
    a=random.getrandbits(256)
    a=str(a).encode()
    b=random.getrandbits(256)
    b=str(b).encode()
    re1=seg_func(a)
    re2=seg_func(b)
    if(re1[0:Index]==re2[0:Index]):
        print('find',re1[0:Index])
        print('r1',re1)
        print('r2',re2)
        break
t2=time()
print('time',(t2-t1),'s')
#到此结束，下面是测试时使用的一些代码，已被注释
'''
n=random.getrandbits(32)
x=2
t3=time()
while True:
    x=f(x,n)
    x2=f(x,n)
    x_str=str(x).encode()
    re1=seg_func(x_str)
    x2_str=str(x2).encode()
    re2=seg_func(x2_str)
    if(re1[0:3]==re2[0:3]):
        print('find',re1[0:3])
        break
t4=time()
print('time',(t4-t3))
        
'''        
   

#W=b'AjdklfHdfn'
#print(hex(W.decode()))
#print(int('Test'.hex(),16))
#print(hex(70655608415212328466912085763263534874646195139384))
#print(b'\x00\x00\x00\x00'.hex())
#print(byte_stream_xor(b'\x00\x00\x00\x00',b'er\x80\x00'))
#print(P1(b'er\x80\x00'))



