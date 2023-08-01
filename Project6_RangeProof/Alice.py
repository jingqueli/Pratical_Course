#import hmac
#Alice
import hashlib
import secrets#用于生成随机数128bit
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import socket               # 导入 socket 模块
import json
import base64
import random
import secrets
import string
import time
'''
key=(str(22)+str(100)).encode()
message = b'Hello, world!'
hash_function = hashlib.sha256

hmac_value_k = hmac.new(key, message, hash_function).digest()
print(hmac_value_k)
'''
#下面是库函数的hash_SM3    
def sm3_hash(data):
    hash_object = hashlib.new('sm3')
    hash_object.update(data)
    hash_value = hash_object.hexdigest()
    return hash_value

#私钥
customer_key='-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAmNVYZtnih4UY+bHR+ZlbmZbiwE5E8SDOJQlgdfcbCnRo43cY\n9ELXaBuRG3wEE3M1X5FRwmJvnh7KFXw3IghssvOJj1vFWjcDH1rEv6+khv9xWg4e\nrzM7ljDKNPpSFYywG1mJdr/1KRUt1o3o5DZYR0cJjmjRqU7JYP9WermVf6aTGyA/\n4rH46IGU8p1ulRhLZgc9gaTRmzJ8VyZSRayeaZtQ6KvXsFFVUfDlC3g+vIQc/IBD\nD+q/14ptMNHYo7RSiAKCExFRc+/NCDQ94m+S6je6VlR4W+zYkVR3zvfcC2mMfllN\nNzy+7dzwvT8o0jhvylfGB9DOyjTCskJqEY978QIDAQABAoIBACQEdVSpyQ+4f3IK\n5MneiR6JV09MMsWjvkkurEeosDv2wqhGj0AzR2nuwzP3tksyJbQrvlmh0p2wMl49\nW43e7+T9bV/2V+xilg8L2F23Qj4ZUYiQVs1htMt4nJK/IlyXPwJ3B6UPaHKh3d9Y\nKrgrkYLcvCUOUUjF+0HrcuExvshp5zN8xb+iNKVOvXhsU7teY4HVbdj/srJvOJLx\nUU/I999lNVgci2kchW0QkVCkjFpQp7zoy9MoXzxvfQ3WE7CcqkiQ+ckxGtop8wiX\nKP+gQdXtrpDhamv4uubTbcHGz8RiGSaFWh1KT0AJVFQ0YRvqfH4+ybZgbiuSHZJB\nyGt5TzUCgYEAwQ1mIIX444jCLR2paS6ZNrM3LSSNrUGfU176tZm3b8YWtCM/Xu8L\n1HTpN+miepfa4cMWMNGPfciGaPO0Tu00SVDaZ/fz/MAPCOQLwRZ+4mkUyD0QBbqV\ni4EY42UXiZrUvrX2dn1lhH86EwB7l6AJTYCf+NNNb26xI5B46nXqgb0CgYEAyqrC\n0yFVsrKJ4j7QbFqjlN70HssmJ+hAYQ+1finQFZEdMheLFfOh3B3mvTxTEQrCDUXH\nZOR6cBILlESONA++VN6CFC1wtjS9uiAAuvlLRP2KnY5I1t7mGkv37ThcXsS8YGjE\njkG6zzOOgogdDCI1SwrlvIC8bo+iYgJEgisy1EUCgYAcvDzWXHq2i5Wzl3WvBVOi\n87wjyQwZnOn1Q+73dwD57zdT6uc030oYfqp0Ox+HNfFLp3k3HQpJw75WAuh00xP0\nUcegsCSuG3xha2hgflO2qcOBJq2q3KID2Nx2hIajYduG45ji/DlPJozjZTAAWr7n\nvVyScglVq9lMHOYSqCiW1QKBgCHlV3paW+vsQnVtjgxhSHSwqWGxFmucQ5A4QWGd\neqjwwVJMb723Jr4a3imOOlJiWzw/DG9Ka1PtILSmlqYMcAffwx++zdgbkBPeIGEl\nKrqaMSHS10ngs9l4FTo+r+xFuT/ipeUpByZ6d/5K55jM697mLrBNU7amHUGJIY4n\nzXOFAoGAJw8yn3ithFmkha2xnV5pe1IXHhYsZFN8vtbMcZEEF31fhGGtkL7AnKXi\nsGqOQyY3TdDSMJ/+eCxJC4jFUJ6XmiBUUa6TFH62FIbVLouQgCLZbwzd8l7Aa1fu\nwvz6XHXI+pPc44Z/Z90HxBP93xU5KcqU/L9xSPC7qXAH2D5qwuc=\n-----END RSA PRIVATE KEY-----'
customer_key=RSA.import_key(customer_key)

# 使用私钥对数据进行签名
def sign_data(data):
    h = SHA256.new(data.encode('utf-8'))
    signature = pkcs1_15.new(customer_key).sign(h)
    return signature
# 使用公钥验证签名
def verify_signature(data, signature,public_key):
    h = SHA256.new(data.encode('utf-8'))
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except:
        return False


        
def H1(key,message):
    #key是整数，message为字符串类型
    x=message[0:2]
    key_str=hex(int(x,16)+key)[2:]
    key_mes=key_str+message[2:]
    return key_mes


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # 创建 socket 对象
host = socket.gethostname() # 获取本地主机名
port_Issuer = 50000
port_Alice = 12345   # 设置端口
port_Bob=10001
s.bind((host, port_Alice))        # 绑定端口

d0=22
#Alice监听消息
mes,addr=s.recvfrom(2048*8)
print(f'Received message from {addr}: {json.loads(mes.decode())}')
data=json.loads(mes.decode())
sig_c_str=data['sig_c']#提取出签名
seed=data['seed']
proof_p=H1(d0,seed)
public_key=data['public_key']
send_data={'p':proof_p,'sig_c':sig_c_str,'public_key':public_key}
json_data=json.dumps(send_data).encode()#对字典处理
s.sendto(json_data,(host, port_Bob))
s.close()

