from pwn import *
from string import printable as ascii
from pprint import pprint
import sys
r = remote("178.62.9.10", 31350)
context.log_level = "critical"

# flag = "HTB{hmm_w1th_s0m3_ana1ys15_y0u_c4n_3x7ract_7h3_h4mmin9_7_4_3nc_fl49}"
flag = ""

def hamming_decoder(encoded_bits):
    p0 = encoded_bits[0] ^ encoded_bits[2] ^ encoded_bits[4] ^ encoded_bits[6]
    p1 = encoded_bits[1] ^ encoded_bits[2] ^ encoded_bits[5] ^ encoded_bits[6]
    p2 = encoded_bits[3] ^ encoded_bits[4] ^ encoded_bits[5] ^ encoded_bits[6]
    syndrome = p2 * 4 + p1 * 2 + p0
    if syndrome == 0:
        return encoded_bits[2], encoded_bits[4], encoded_bits[5], encoded_bits[6]
    corrected_bit = (encoded_bits[syndrome-1] + 1) % 2
    corrected_bits = encoded_bits[:]
    corrected_bits[syndrome-1] = corrected_bit
    return corrected_bits[2], corrected_bits[4], corrected_bits[5], corrected_bits[6]

while len(flag) <= 68:
    status = True
    clean_flag = {}
    while status:
        encoded_str = r.recvline().decode().split(": ")[-1].strip()
        encoded_bits = [int(x) for x in encoded_str]
        decoded_bits = []
        for i in range(0, len(encoded_bits), 7):
            decoded_bits.extend(hamming_decoder(encoded_bits[i:i+7]))
        decoded_str = ''.join(str(bit) for bit in decoded_bits)
        ascii_string = ''.join(chr(int(decoded_str[i:i+8], 2)) for i in range(0, len(decoded_str), 8))
        if len(ascii_string) == 68:
            char = ascii_string[len(flag)]
            if char not in clean_flag.get(0, {}):
                clean_flag.setdefault(char, 0)
            clean_flag[char] += 1
        clean_flag = dict(sorted(clean_flag.items(), key=lambda x: x[1], reverse=True))
        tmp = list(clean_flag.keys())[0]
        if clean_flag[tmp] == 5:
            flag += tmp
            status = False
        print(f"found: {flag+tmp}", end="\r")
