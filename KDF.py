import hashlib
import hmac


class KDF(object):
    def __init__(self,  **locker_args):
        self.BCH_POLYNOMIAL = 1051  # 有效位



    def Key_Derive(self, key_material, output_length):
        # 定义哈希算法和密钥长度
        hash_algo = hashlib.sha256
        key_length = hash_algo().digest_size

        # 计算所需的迭代次数
        iterations = (output_length + key_length - 1) // key_length

        # 初始化派生密钥结果
        derived_key = b""

        for i in range(1, iterations + 1):
            # 使用HMAC-SHA256计算伪随机函数（PRF）
            prf = hmac.new(key_material, digestmod=hash_algo)
            prf.update(bytes([i]))  # 添加迭代计数器

            # 添加PRF结果到派生密钥
            derived_key += prf.digest()

        # 返回指定长度的派生密钥
        return derived_key[:output_length]
    def BinaryToStr(self, binary_string):
        fixed_length = 8
        binary_list = [binary_string[i:i + fixed_length] for i in range(0, len(binary_string), fixed_length)]
        ascii_string = ""
        for binary in binary_list:
            decimal_value = int(binary, 2)  # 将二进制子字符串转换为对应的整数值
            character = chr(decimal_value)  # 将整数值转换为对应的 ASCII 字符
            ascii_string += character

        #print(ascii_string)  # 输出: "hello"
        return ascii_string

    def BinaryToByteArray(self, binary_str):
        n = int(binary_str, 2)

        # 将整数转换为字节序列
        byte_seq = n.to_bytes((n.bit_length() + 7) // 8, 'big')

        # 将字节序列转换为bytearray类型
        byte_array = bytearray(byte_seq)
        return byte_array

