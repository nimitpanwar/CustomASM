reg_Val_Dict = {
    '000': 0,
    '001': 0,
    '010': 0,
    '011': 0,
    '100': 0,
    '101': 0,
    '110': 0,
}

flags = "0000000000000000"

# Opening file
with open("sample_sim.txt") as f:
    input_len = len(f.readlines())
input_list = []

with open("sample_sim.txt") as g:
    for i in range(input_len):
        input_list.append(g.readline())

def convert_binary(number):
    bin_int_num=str(bin(int(float(number))))[2:]
    if len(str(bin_int_num))>3:
        return 0
    decimal_num=number-int(float(number))
    count=0
    bin_dec_num=''
    while count<5:
        count+=1
        bit=int(decimal_num*2)
        bin_dec_num+=str(bit)
        decimal_num=decimal_num*2- bit
    k=3
    bias=2**(k-1) -1
    power=len(bin_int_num)-1+bias
    power=str(bin(power))[2:]
    if len(power)<3:
        power=(3-len(power))*"0" + power
    mantissa=(str(bin_int_num)[1:]+bin_dec_num)[:5]
    return (power+mantissa)

# Helper functions
def decToBin(val, bits):
    if type(val) == float:
        a = convert_binary(val)
        if len(a) < bits:
            a = a + ("0" * (bits - len(a)))
        return a
    else:
        b = str(bin(val)[2:])
        if len(b) < bits:
            b = "0" * (bits - len(b)) + b
        return b

def binToDec(bin_num):
    a = int(bin_num, 2)
    return a


def getRegVal(reg):
    return reg_Val_Dict.get(reg)


def print_reg():
    for i in reg_Val_Dict:
        print(decToBin(reg_Val_Dict.get(i), 16), end=" ")

def float_to_decimal(binary):
    exponent = int(binary[0:3], 2) - 3
    mantissa = binary[3:]
    decimal = 0
    for i, bit in enumerate(mantissa):
        if bit == "1":
            decimal += 1 / (2 ** (i + 1))
    result = (1 + decimal) * 2 ** exponent
    return result


# Instruction functions
def add(current, flags):
    dest_reg = getRegVal(current[7:10])
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg = reg1 + reg2
    if (len(bin(dest_reg)) <= 9):
        reg_Val_Dict[current[7:10]] = dest_reg
        return flags
    else:
        return flags[0:12] + "1" + flags[13:16]

def addf(current, flags):
    dest_reg = getRegVal(current[7:10])
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    dest_reg = reg1 + reg2
    if (len(convert_binary(dest_reg)) <= 8):
        reg_Val_Dict[current[7:10]] = dest_reg
        return flags
    else:
        return flags[0:12] + "1" + flags[13:16]



def sub(current, flag):
    dest_reg = getRegVal(current[7:10])
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    if (reg1 >= reg2):
        dest_reg = reg1 - reg2
        reg_Val_Dict[current[7:10]] = dest_reg
        return flag
    else:
        return flag[0:12] + "1" + flag[13:16]

def subf(current, flag):
    dest_reg = getRegVal(current[7:10])
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    if (reg1 >= reg2):
        dest_reg = reg1 - reg2
        reg_Val_Dict[current[7:10]] = dest_reg
        return flag
    else:
        return flag[0:12] + "1" + flag[13:16]

def mul(current):
    dest_reg = getRegVal(current[7:10])
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg = reg1 * reg2
    if (len(bin(dest_reg)) <= 9):
        reg_Val_Dict[current[7:10]] = dest_reg
        return flags
    else:
        return flags[0:12] + "1" + flags[13:16]

def mulf(current):
    dest_reg = getRegVal(current[7:10])
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    dest_reg = reg1 * reg2
    if (len(convert_binary(dest_reg)) <= 8):
        reg_Val_Dict[current[7:10]] = dest_reg
        return flags
    else:
        return flags[0:12] + "1" + flags[13:16]


def XOR(current):
    dest_reg = getRegVal(current[7:10])
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg = reg1 ^ reg2
    reg_Val_Dict[current[7:10]] = dest_reg
    # print(dest_reg)


def OR(current):
    dest_reg = getRegVal(current[7:10])
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg = reg1 | reg2
    reg_Val_Dict[current[7:10]] = dest_reg
    # print(dest_reg)


def AND(current):
    dest_reg = getRegVal(current[7:10])
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg = reg1 & reg2
    reg_Val_Dict[current[7:10]] = dest_reg
    print(dest_reg)


def mov_imm(current):
    dest_reg = binToDec(current[9:16])
    reg_Val_Dict[current[6:9]] = dest_reg

def movf_imm(current):
    dest_reg = float_to_decimal(current[9:16])
    reg_Val_Dict[current[6:9]] = dest_reg


def r_shift(current):
    dest_reg = getRegVal(current[6:9])
    dest_reg = dest_reg >> binToDec(current[9:16])
    reg_Val_Dict[current[6:9]] = dest_reg


def l_shift(current):
    dest_reg = getRegVal(current[6:9])
    dest_reg = dest_reg << binToDec(current[9:16])
    reg_Val_Dict[current[6:9]] = dest_reg


def mov_reg(current):
    if(current[13:16]!="111"):
        reg1=getRegVal(current[13:16])
        dest_reg=reg1
        reg_Val_Dict[current[10:13]]=dest_reg
    else:
        reg1=binToDec(flags)
        dest_reg=reg1
        reg_Val_Dict[current[10:13]]=dest_reg


def div(current, flag):
    reg3 = getRegVal(current[10:13])
    reg4 = getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    if (reg4 != 0):
        quotient = reg3 // reg4
        remainder = reg3 % reg4
        reg_Val_Dict['000'] = quotient
        reg_Val_Dict['001'] = remainder
        return flag
    else:
        return flag[0:12] + "1" + flag[13:16]


def cmp(current, flag):
    reg1 = getRegVal(current[10:13])
    reg2 = getRegVal(current[13:16])
    if (reg1 < reg2):
        flag = flag[0:13] + "1" + flag[14:16]
    elif (reg1 > reg2):
        flag = flag[0:14] + "1" + flag[15:16]
    elif (reg1 == reg2):
        flag = flag[0:15] + "1" + flag[16:16]
    return flag


# def inv(current):
#     reg2 = getRegVal(current[13:16])
#     not_val = ~reg2
#     reg_Val_Dict[current[10:13]] = not_val

def inv(current):
    reg2=getRegVal(current[13:16])
    not_val=""
    for i in decToBin(reg2,7):
        if i=="0":
            not_val="".join([not_val,"1"])
        elif i=="1":
            not_val="".join([not_val,"0"])
    reg_Val_Dict[current[10:13]]=binToDec(not_val)
    # print(not_val)


def jmp(current):
    pc = binToDec(current[9:16])
    return pc


def jlt(pc, current):
    if flags[13] == "1":
        pc = binToDec(current[9:16])
    else:
        pc += 1
    return pc


def jgt(pc, current):
    if flags[14] == "1":
        pc = binToDec(current[9:16])
    else:
        pc += 1
    return pc


def je(pc, current):
    if flags[15] == "1":
        pc = binToDec(current[9:16])
    else:
        pc = pc + 1
    return pc


def ld(current):
    mem_add = current[9:16]
    dest_reg = current[6:9]
    if mem_add not in varDict.keys():
        varDict[mem_add] = 0
    reg_Val_Dict[dest_reg] = varDict[mem_add]
    


def st(current):
    mem_add = current[9:16]
    dest_reg = current[6:9]
    varDict[mem_add] = reg_Val_Dict[dest_reg]


# Program variables
pc = 0
output_list = []
halted = False
i = 0

# Main execution
while (halted != True):
    # variables
    bin_pc = decToBin(pc, 7)
    curr = input_list[pc]
    curr_inst = (curr[0:5])
    jump_inst = False
    newFlags = flags

    # Identifying opcode and executing instructions
    if (curr_inst == "00000"):
        newFlags = add(curr, flags)
    elif (curr_inst == "00001"):
        newFlags = sub(curr, flags)
    elif (curr_inst == "00110"):
        newFlags = mul(curr)

    elif (curr_inst == "01010"):
        XOR(curr)
    elif (curr_inst == "01011"):
        OR(curr)
    elif (curr_inst == "01100"):
        AND(curr)
    elif (curr_inst == "00010"):
        mov_imm(curr)
    elif (curr_inst == "01000"):
        r_shift(curr)
    elif (curr_inst == "01001"):
        l_shift(curr)
    elif (curr_inst == "00011"):
        mov_reg(curr)
    elif (curr_inst == "00111"):
        newFlags = div(curr, flags)
    elif (curr_inst == "01101"):
        inv(curr)
    elif (curr_inst == "01110"):
        newFlags = cmp(curr, flags)
    elif (curr_inst == "01111"):
        pc = jmp(curr)
        jump_inst = True
    elif (curr_inst == "11100"):
        pc = jlt(pc, curr)
        jump_inst = True
    elif (curr_inst == "11101"):
        pc = jgt(pc, curr)
        jump_inst = True
    elif (curr_inst == "11111"):
        pc = je(pc, curr)
        jump_inst = True
    elif (curr_inst == "11010"):
        halted = True
    elif (curr_inst == "10000"):
        newFlags = addf(curr, flags)
    elif (curr_inst == "10001"):
        newFlags = subf(curr, flags)
    elif (curr_inst == "10110"):
        newFlags = mulf(curr)
    elif (curr_inst == "10010"):
        movf_imm(curr)

    # Setting/Resetting flags reg
    if (newFlags == flags):
        flags = "0000000000000000"
    else:
        flags = newFlags

    print(bin_pc, end="        ")
    print_reg()
    print(flags)
    # print("")

    if (jump_inst == False):
        pc += 1


n_nl=0
for i in input_list:
    if i=="\n":
        n_nl+=1

for i in range(n_nl):
    input_list.remove("\n")

for i in input_list:
    if "\n" in i:
        print(i,end="")
    else:
        print(i)

while(pc<128):
    print("0000000000000000")
    pc += 1
