from binascii import unhexlify
seven_segment_combinations = {
    '1111110': '0',
    '0110000': '1',
    '1101101': '2',
    '1111001': '3',
    '0110011': '4',
    '1011011': '5',
    '1011111': '6',
    '1110000': '7',
    '1111111': '8',
    '1111011': '9',
    '1110111': 'A',
    '0011111': 'B',
    '1001110': 'C',
    '0111101': 'D',
    '1001111': 'E',
    '1000111': 'F',
}

def convert(s):
    n = [s[2],s[5],s[4],s[0],s[6],s[7],s[3]]
    return ''.join(n)

data = [x.replace(",","").strip() for x in open("digital.csv").readlines()]
flag = ""
for x in data:
    x = convert(x)
    if seven_segment_combinations.get(x):
        flag+=seven_segment_combinations[x]
flag = [flag[i:i+2] for i in range(0, len(flag), 2)]

clean = ""
for x in range(0, len(flag), 1):
    if len(set(flag[x]))==1:
        clean+=flag[x]
flag = ""
for x in range(0, len(clean)-1,2):
    flag+=clean[x]
print(len(flag),unhexlify(flag))
