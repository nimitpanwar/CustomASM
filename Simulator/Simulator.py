def aand(a,b):
    s=""
    for i in range(min(len(a), len(b))):
        s+='1'if int(a[i])==int(b[i])==1 else '0'
    return s

def oor(a,b):
    s=""
    for i in range(min(len(a), len(b))):
        s+='0' if int(a[i])==int(b[i])==0 else '1'
    return s

def xor(a,b):
    s=""
    for i in range(min(len(a), len(b))):
        s+='0' if int(a[i])!=int(b[i]) else '1'
    return s

def invert(a):
    s=""
    for i in range(len(a)):
        if int(a[i])==1:
            s+='0' 
        else:
            s+='1'
    return s


def DecToBin7(decimal_num):
    binary_num = bin(decimal_num)[2:]
    binary_num = '0' * (7 - len(binary_num)) + binary_num
    return binary_num


def DecToBin16(decimal_num):
    binary_num = bin(decimal_num)[2:]
    binary_num = '0' * (16 - len(binary_num)) + binary_num
    return binary_num


def BinToDec(binary):
    decimal_num = 0 
    x = 0
    while(binary != 0):
        dec = int(binary) % 10
        decimal_num += dec * pow(2, x)
        binary= int(binary)//10
        x+= 1
    return decimal_num


opcodes = {
    'add':["00000","A"],
    'sub':["00001","A"],
    'mov':["00010","B"],
    'ld':["00011","D"],
    'st':["10101","D"],
    'mul':["10110","A"],
    'div':["10111","C"],
    'rs':["11000","B"],
    'ls':["11001","B"],
    'xor':["11010","A"],
    'or':["11011","A"],
    'and':["11100","A"],
    'not':["11101","C"],
    'cmp':["11110","C"],
    'jmp':["11111","E"],
    'jlt':["01100","E"],
    'jgt':["01101","E"],
    'je':["01111","E"],
    'hlt':["01010","F"],
}

opcodeType = {
    "00000":"A",
    "00001":"A",
    "00010":"B",
    "00011":"B",
    "00011":"C",
    "00100":"D",
    "00101":"D",
    "00110":"A",
    "00111":"C",
    "01000":"B",
    "01001":"B",
    "01010":"A",
    "01011":"A",
    "01100":"A",
    "01101":"C",
    "01110":"C",
    "01111":"E",
    "11100":"E",
    "11101":"E",
    "11111":"E",
    "11010":"F",
}

registers = {
	'R0':'000',
	'R1':'001',
	'R2':'010',
	'R3':'011',
	'R4':'100',
	'R5':'101',
	'R6':'110',
	'FLAGS':'111' 
}

with open("sample.txt","r") as f:
    contents=f.readlines()

def iType(a):
    return opcodeType[a[:5]]

i=0
while(iType(contents[i])!="F"):
    type=iType(contents[i])
    print(type)
    i=i+1

