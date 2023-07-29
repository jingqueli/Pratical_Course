#verify the above pitfalls
import ECDSA_myself as ecdsa
import sm2_myself as sm2
import Schnorr_myself as schnorr
from gmpy2 import invert
import gmpy2
#1  ECDSA:leaking k lead to leaking of d
def ECDSA_leak_k(mes):
    q=ecdsa.q
    d,Q=ecdsa.key_gen()
    print('真正的d是',d)
    k=61052478844650362117101898807367092637533363199480174276305957447633440843510
    (r,s)=ecdsa.signature(mes,d)
    print('r',r)
    e=ecdsa.sm3_hash(mes.encode())
    e=int(e,16)
    print('e',e)
    d_re=((s*k-e)*invert(r,q))%q
    print('根据k还原出d是',d_re)
    if(d==d_re):
        print('leaking k lead to leaking of d')
    return d_re
#2 ECDSA:reusing k lead to leaking of d
def ECDSA_reuse_k(mes1,mes2):
    q=ecdsa.q
    d,Q=ecdsa.key_gen()
    print('真正的d是',d)
    (r1,s1)=ecdsa.signature(mes1,d)
    (r2,s2)=ecdsa.signature(mes2,d)
    e1=ecdsa.sm3_hash(mes1.encode())
    e1=int(e1,16)
    #print('e1',e1)
    e2=ecdsa.sm3_hash(mes2.encode())
    e2=int(e2,16)
    #print('e2',e2)
    s1e2_s2e1=(s1*e2-s2*e1)%ecdsa.q
    s2r1_s1r2=(s2*r1-s1*r2)%ecdsa.q
    d_re=(invert(s2r1_s1r2,ecdsa.q)*(s1e2_s2e1))%ecdsa.q
    print('还原出d是',d_re)
    if(d==d_re):
        print('resuing k lead to leaking of d')
    return None
#3:ECDSA Two users,using k leads to leaking of d,that they can deduce each other's d    
def ECDSA_deduce_other_d(mes1,mes2):
    q=ecdsa.q
    k=61052478844650362117101898807367092637533363199480174276305957447633440843510
    d,Q=ecdsa.key_gen()
    print('真正的d',d)
    #用户一使用k与用户二的消息推断用户二的密钥d
    (r2,s2)=ecdsa.signature(mes2,d)#(r2,s2)是用户一可以获知的用户二的签名
    e=ecdsa.sm3_hash(mes2.encode())
    e=int(e,16)
    d_re_1=((s2*k-e)*invert(r2,q))%q
    print('d_re_1',d_re_1)
    if(d_re_1==d):
        print('user 1 can deduce k of user 2')
    #用户二也可推测用户一的d
    (r1,s1)=ecdsa.signature(mes1,d)
    e=ecdsa.sm3_hash(mes1.encode())
    e=int(e,16)
    d_re_2=((s1*k-e)*invert(r1,q))%q
    print('d_re_2',d_re_2)
    if(d_re_2==d):
        print('user 2 can deduce k of user1')
    return None
#ECDSA (r,s),(r,-s)are both valid signature
def ECDSA_both_vaild(mes):
    q=ecdsa.q
    d,Q=ecdsa.key_gen()
    (r,s)=ecdsa.signature(mes,d)
    #try to verify (r,s) signature
    ecdsa.verify_sig(mes,Q,(r,s))
    #make a fake sig
    (r1,s1)=ecdsa.point_neg((r,s))
    #try to verify (r1,s1) signature
    ecdsa.verify_sig(mes,Q,(r1,s1))
    return None

#ECDSA forge_signature_donot_check_m
def ECDSA_forge_sig(mes):
    #if without hash and donot check m,we can forge a fake sig as following:
    q=ecdsa.q
    d,Q=ecdsa.key_gen()
    e=ecdsa.sm3_hash(mes1.encode())
    e=int(e,16)
    
    (r,s)=ecdsa.signature(mes,d)
    print('s的逆',invert(s,q))
    print('r',r)
    #ecdsa.verify_sig_fake(e,Q,(r,s))
    #try to forge a sig
    #e_fake=(e*invert(r,q)*invert(s,q))%q
    #print('e_fake',e_fake)
    (r1,s1)=(invert(s,q),invert(r,q))
    #sig=(r1,s1)
    ecdsa.verify_sig_fake(e,Q,(r1,s1))
    return None

def ECDSA_same_dk(mes1,mes2):
    q=ecdsa.q
    d,Q=ecdsa.key_gen()
    print('真正的d是',d)
    (r1,s1)=ecdsa.signature(mes1,d)
    (r2,s2)=ecdsa.signature(mes2,d)
    e1=ecdsa.sm3_hash(mes1.encode())
    e1=int(e1,16)
    #print('e1',e1)
    e2=ecdsa.sm3_hash(mes2.encode())
    e2=int(e2,16)
    #print('e2',e2)
    s1e2_s2e1=(s1*e2-s2*e1)%ecdsa.q
    s2r1_s1r2=(s2*r1-s1*r2)%ecdsa.q
    d_re=(invert(s2r1_s1r2,ecdsa.q)*(s1e2_s2e1))%ecdsa.q
    print('还原出d是',d_re)
    if(d==d_re):
        print('using same d and k leads to leaking of d ')
    return None
    




mes1='RuoYan'
mes2='Flore'
#ECDSA_leak_k(mes1)
#ECDSA_reuse_k(mes1,mes2)
#ECDSA_deduce_other_d(mes1,mes2)
#ECDSA_both_vaild(mes1)
#ECDSA_forge_sig(mes1)
ECDSA_same_dk(mes1,mes2)
