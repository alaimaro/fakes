import bchlib
import random
import numpy as np
import torch
import os
import hashlib
import math


class BCH(object):
    def __init__(self,  **locker_args):
        # 码字长度=BCH_POLYNOMIAL+BCH_BITS
        self.BCH_POLYNOMIAL = 253 # 多项式
        self.BCH_BITS = 6  # 纠错能力
        #self.key_file = 'database_key.csv'   #秘钥文件名
        self.bch=bchlib.BCH(self.BCH_POLYNOMIAL, self.BCH_BITS)

    #msg 为bytearray型
    def do_encode(self, msg):
        #data = bytearray(msg.encode('utf-8'))
        data =msg

        #data = bytes(bin(int(msg, 2)), encoding='utf-8')
        print("data:%s"%data)
        # encode and make a "packet"
        ecc = self.bch.encode(data)

        print("ecc:%s"%ecc)


        packet = data + ecc

        return packet

    def do_decode(self, packet):
        # print hash of packet
        #packet = bytes(int(msg, 2))
        #packet = self.str2bits(msg)

        print(packet)
        print(len(packet))


        print(self.bch.ecc_bytes)
        # de-packetize
        data, ecc = packet[:-self.bch.ecc_bytes], packet[-self.bch.ecc_bytes:]
        print(data)
        print(ecc)

        # correct
        bitflips = self.bch.decode_inplace(data, ecc)

        # packetize
        packet = data + ecc



        return data








