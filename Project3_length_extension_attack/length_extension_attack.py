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


def padding_func_fake(data):
    data=data.encode()
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
def seg_func_fake(data,IV_fake):
    #输入信息类型为bit stream
    #data=b'Hello World You are so happy'
    IV=[]
    group_number=int(len(data)/64)+1#64byte per group
    #print("group number",group_number)
    if(group_number==1):
        padding_data=padding_func(data[:])
        IV=compression_func(IV_fake,padding_data)
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

'''
def sha256_padding(input_bytes):
    original_length = len(input_bytes) * 8  # 原始消息的比特长度
    padding_length = 512 - ((original_length + 1 + 64) % 512)  # 填充长度
    padding = b'\x80' + b'\x00' * (padding_length // 8 - 1)  # 添加比特为1的位和零填充
    length_bytes = original_length.to_bytes(8, 'big')  # 将原始长度转换为8字节的大端序列
    padded_message = input_bytes + padding + length_bytes  # 拼接填充后的消息
    return padded_message
'''

def length_extension_attack(re_hash,data_after,data):
    
    #re_hash表示之前信息的hash值，data_after表示之后要扩展的信息,data表示原始消息
    #如果直接从data_after开始计算hash，即直接把初始IV换成返回的hash值的hash即可
    #额外写了一个seg_func_fake,不同于普通hash的是，该函数可以指定初始IV,从而达到更换IV0的目的
    IV_fake=[]
    for i in range(0,8):
        IV_i=re_hash[i:i+8]#字符串类型
        IV_i=int(IV_i,16)
        IV_fake.append(IV_i)
    #print('IV_fake',IV_fake)
    #经过该循环，做出假的初始IV进行替换
    data0=seg_func_fake(data_after.encode(),IV_fake)
    print(seg_func_fake(data_after.encode(),IV_fake))#从data_after开始，算出的hash值
    #接下来把data_after直接拼接在原消息(padded)后面，重新开始计算一个hash值
    group_number=int(len(data)/64)+1#64byte per group
    if(group_number==1):
        padding_data=padding_func(data[:].encode())
        data=padding_data+data_after.encode()
        
    else:
        data_front=data[0:(group_number-1)*64]
        padding_data=padding_func_fake(data[64*(group_number-1):])
        data=data_front.encode()+padding_data+data_after.encode()
    print('data 拼接后：',data)
    data=seg_func(data)
    print(data0)
    

data='RuoYanadjkfaddg'
re_hash=seg_func(data.encode())
data_after='Dancing with the ghost'
length_extension_attack(re_hash,data_after,data)



