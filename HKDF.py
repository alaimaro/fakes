#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import hashlib
import hmac
from math import ceil
import chardet,sys
from BCH import BCH


class HKDF(object):
    def __init__(self,  **locker_args):
        # 码字长度=BCH_POLYNOMIAL+BCH_BITS
        self.hash_len = 32 #

    def hmac_sha256(self,key, data):
        return hmac.new(key, data, hashlib.sha256).digest()


    def hkdf(self,length, ikm, salt=b"", info=b""):
        prk = self.hmac_sha256(salt, ikm)
        t = b""
        okm = b""
        for i in range(ceil(length / self.hash_len)):
            t = self.hmac_sha256(prk, t + info + bytes([1 + i]))
            okm += t
        return okm[:length]



hkdf_instancee=HKDF()

msg='10101000011110100010000010011111001010011010100001111010001000001001111100101001101010000111101000100000100111110010100101010111'
print(len(msg))
ikm=bytearray(bin(int(msg,2)), encoding='utf-8')
print('ikm',ikm[2:])
R0=hkdf_instancee.hkdf(121,ikm)
print(R0)
print(len(R0))
print('R0',R0[2:])
bch=BCH()
R0_1=bch.do_encode(R0)
print(R0_1)
print(len(R0_1))
k_r = int.from_bytes(bytes(ikm), sys.byteorder)
r_r = int.from_bytes(R0_1, sys.byteorder)
print(bin(k_r)[2:])
print(bin(r_r)[2:])
p = k_r ^ r_r
print(p)
print(bin(p)[2:])
msg1='10101001111110100010000010011111001010011010100001111010001000001001111100101001101010000111101000100000100111110010100101010111'


