import matplotlib.pyplot as plt

opcodes = {
    	'add':["00000","A"],
    	'sub':["00001","A"],
    	'mov':["00010","B"],
    	'mov':["00011","C"],
    	'ld':["00100","D"],
    	'st':["00101","D"],
    	'mul':["00110","A"],
    	'div':["00111","C"],
    	'rs':["01000","B"],
    	'ls':["01001","B"],
    	'xor':["01010","A"],
    	'or':["01011","A"],
    	'and':["01100","A"],
    	'not':["01101","C"],
    	'cmp':["01110","C"],
    	'jmp':["01111","E"],
    	'jlt':["11100","E"],
    	'jgt':["11101","E"],
    	'je':["11111","E"],
    	'hlt':["11010","F"],
}

OpCode = {
    "00000":"A",
    "00001":"A",
    "00010":"B",
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

flag = 0
Registers = [0, 0, 0, 0, 0, 0, 0]

# mapping of program counter and memory address
pc_and_cycle = []

halted = False

# 8 bits required to represent memory address, one address contains a 16 bit binary
Memory_Heap = []
Binary_input = []
pc = 0
cycle = 1

def decimal_converter(num):
    while num > 1:
        num /= 10
    return num
manti=0
expi=0
def conversionFloat(n):
    k=str(n)
    if('.' not in k):
        k=k+".0"
    ki,kf=[int(i) for i in k.split(".")]
    mn1=bin(ki).replace("0b", "")
    i=0
    mn2=""
    dec=float("."+str(kf))
    while(dec!=0 and i<5):
        i+=1
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        mn2 += whole
    n1=len(mn1)
    n2=len(mn2)
    flag=0
    if(n1-1>7):
        flag=1
        return -1
    if(n1==7 and (mn1[6]=='1' or mn1[5]=='1') ):
        flag=1
        return -1
    if(n1==6 and mn1[5]=='1'):
        flag=1
        return -1
    if(n1+n2-1>8):
        flag=1
        return -1
    global manti
    manti=int(mn1)
    if(mn2==""):
        mn2="0"
    global expi
    expi=int(mn2)
    return 0
# print(manti,expi)

def checkOverflow(ind):
    global Registers, flag
    if (Registers[ind] > 2**16-1 or Registers[ind] < 0):
        flag = 8
        if (Registers[ind] > 2**16-1):
            Registers[ind] = int(ConvertToBinary16(Registers[ind]), 2)
        else:
            Registers[ind] = 0
    return


def flag_reset():  # resets flag do use this wherever necessary
    global flag
    flag = 0
    return


def ConvertToBinary16(dec_val):
    global expi,manti
    if(int(dec_val)!=dec_val):
        f=conversionFloat(dec_val)
        if(f==0):
            binval=bin(len(manti)-1)[2:]
            if(len(manti)<5):
                manti=manti+"0"*(5-len(manti))
            if(len(manti)>5-len(expi)):
                manti=manti[:5-len(expi)]
            binval+=manti+expi
            binval="0"*8+binval
            return binval
        else:
            return "0000000011111111"
        
    if (dec_val > 2**16-1):
        bin_rep = str(bin(dec_val))
        bin_rep = bin_rep[2::]
        l = len(bin_rep)
        bin_rep = bin_rep[l-16:l:]
        binval = int(bin_rep, 2)
        binval = ('{0:016b}'.format(binval))
    else:
        binval = ('{0:016b}'.format(dec_val))
    return binval


def ConvertToBinary8(dec_val):
    binval = ('{0:08b}'.format(dec_val))
    return binval


def ConvertToDecimal(bin_val):
    return int(bin_val, 2)


def outputOneLine():
    global pc, cycle, pc_and_cycle
    print(
        ConvertToBinary8(pc),
        ConvertToBinary16(Registers[0]),
        ConvertToBinary16(Registers[1]),
        ConvertToBinary16(Registers[2]),
        ConvertToBinary16(Registers[3]),
        ConvertToBinary16(Registers[4]),
        ConvertToBinary16(Registers[5]),
        ConvertToBinary16(Registers[6]),
        ConvertToBinary16(flag),
        sep=" "
    )
    pc_and_cycle.append((pc, cycle))
    cycle += 1


# 8 bit address and returns a 16 bit value as the data, 512 bytes stores 0 se initialized


def initializeMem():
    for j in range(256):
        Memory_Heap.append("0000000000000000")
    return


def UpdatePC():
    global pc
    pc += 1


# def program_counter:  # 8bit register that points to the current instruction


# operations
def add(instruction): #done
    to_store = instruction[6:9]
    reg1 = instruction[3:6]
    reg2 = instruction[0:3]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] + Registers[ConvertToDecimal(reg2)]
    checkOverflow(ConvertToDecimal(to_store))
    return


def addF(instruction):
    global Registers,flag
    to_store = instruction[6:9]
    reg1 = instruction[3:6]
    reg2 = instruction[0:3]
    n=ConvertToDecimal(ConvertToBinary16(Registers[ConvertToDecimal(reg1)])[:8]) + ConvertToDecimal(ConvertToBinary16(Registers[ConvertToDecimal(reg2)])[:8])
    f=conversionFloat(n)
    
    if(f==1):
        flag = 8
        Registers[ConvertToDecimal(to_store)] = 252
        # int(ConvertToBinary16(252), 2)
        return
    Registers[ConvertToDecimal(to_store)]=Registers[ConvertToDecimal(reg1)] + Registers[ConvertToDecimal(reg2)]
    return 


def sub(instruction): #done
    to_store = instruction[6:9]
    reg1 = instruction[0:3]
    reg2 = instruction[3:6]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] - Registers[ConvertToDecimal(reg2)]
    checkOverflow(ConvertToDecimal(to_store))
    return
def subF(instruction): #done
    global Registers,flag
    to_store = instruction[6:9]
    reg1 = instruction[0:3]
    reg2 = instruction[3:6]
    n=ConvertToDecimal(ConvertToBinary16(Registers[ConvertToDecimal(reg1)])[:8]) - ConvertToDecimal(ConvertToBinary16(Registers[ConvertToDecimal(reg2)])[:8])
    if(n<0):
        Registers[ConvertToDecimal(to_store)] = 0
        flag=8
        return
    f=conversionFloat(n)
    if(f==1):
        flag = 8
        Registers[ConvertToDecimal(to_store)] = 252
        # int(ConvertToBinary16(252), 2)
        return
    Registers[ConvertToDecimal(to_store)]=Registers[ConvertToDecimal(reg1)] - Registers[ConvertToDecimal(reg2)]
    return 


def mul(instruction): #done
    to_store = instruction[6:9]
    reg1 = instruction[3:6]
    reg2 = instruction[0:3]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] * Registers[ConvertToDecimal(reg2)]
    checkOverflow(ConvertToDecimal(to_store))
    return


def xor(instruction): #done
    to_store = instruction[6:9]
    reg1 = instruction[3:6]
    reg2 = instruction[0:3]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] ^ Registers[ConvertToDecimal(reg2)]
    return


def BITor(instruction): #done
    to_store = instruction[6:9]
    reg1 = instruction[3:6]
    reg2 = instruction[0:3]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(reg1)] | Registers[ConvertToDecimal(reg2)]
    return


def BITand(instruction): #done
    to_store = instruction[6:9]
    reg1 = instruction[3:6]
    reg2 = instruction[0:3]
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        reg1)] & Registers[ConvertToDecimal(reg2)]
    return


def rs(instruction): #no need
    to_store = instruction[0:3]
    value = ConvertToDecimal(instruction[3:])
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        to_store)] // (2 ** value)
    return


def ls(instruction): #no need
    to_store = instruction[0:3]
    value = ConvertToDecimal(instruction[3:])
    Registers[ConvertToDecimal(to_store)] = Registers[ConvertToDecimal(
        to_store)] * (2 ** value)
    if (Registers[ConvertToDecimal(to_store)] > 2**16-1):
        Registers[ConvertToDecimal(to_store)] = 0
    return


def movI(instruction): #no need
    to_store = instruction[0:3]
    value = ConvertToDecimal(instruction[3:])
    Registers[ConvertToDecimal(to_store)] = value
    return

def movF(instruction): #no need
    to_store = instruction[0:3]
    value = ConvertToDecimal(instruction[3:])
    Registers[ConvertToDecimal(to_store)] = value
    return


def movR(instruction): #done
    global flag
    to_store = instruction[3:]
    reg_aux = ConvertToDecimal(instruction[0:3])
    if (reg_aux == 7):
        Registers[ConvertToDecimal(to_store)] = flag
    else:
        Registers[ConvertToDecimal(to_store)] = Registers[reg_aux]
    return


def div(instruction): #no need
    rega = ConvertToDecimal(instruction[0:3])
    regb = ConvertToDecimal(instruction[3:])
    quotient = Registers[rega] // Registers[regb]
    remainder = Registers[rega] % Registers[regb]
    Registers[0] = quotient
    Registers[1] = remainder
    return


def inv(instruction): #done
    to_store = instruction[3:]
    regb = ConvertToDecimal(instruction[0:3])
    invert = 2 ** 16 - 1 - Registers[regb]
    Registers[ConvertToDecimal(to_store)] = invert
    return


def compare(instruction): #no need
    global flag
    a = Registers[ConvertToDecimal(instruction[0:3])]
    b = Registers[ConvertToDecimal(instruction[3:])]
    if (a < b):
        flag = 4
    elif (a > b):
        flag = 2
    else:
        flag = 1
    return


def ld(instruction): #no need
    to_store = ConvertToDecimal(instruction[:3])
    address = ConvertToDecimal(instruction[3:])
    Registers[to_store] = ConvertToDecimal(Memory_Heap[address])
    return


def st(instruction): #no need
    global Memory_Heap
    source_reg = ConvertToDecimal(instruction[:3])
    address = ConvertToDecimal(instruction[3:])
    Memory_Heap[address] = ConvertToBinary16(Registers[source_reg])
    return


def jmp(instruction): #no need
    global pc
    mem_add = ConvertToDecimal(instruction)
    pc = mem_add
    return


def jlt(instruction): #no need
    global pc, flag
    mem_add = ConvertToDecimal(instruction)
    if (flag == 4):
        pc = mem_add
    else:
        pc += 1
    return


def jgt(instruction): #no need
    global pc, flag
    mem_add = ConvertToDecimal(instruction)
    if (flag == 2):
        pc = mem_add
    else:
        pc += 1
    return


def je(instruction): #no need
    global pc, flag
    mem_add = ConvertToDecimal(instruction)
    if (flag == 1):
        pc = mem_add
    else:
        pc += 1
    return


def execution_engine():
    global flag, cycle, pc, Memory_Heap, halted
    instruction_bin = Memory_Heap[pc]
    opcode = instruction_bin[:5]
    op = OpCode[opcode]

    if (op!="movR" and op != "jlt" and op != "jgt" and op != "je"): #implementation based if condition
        flag_reset()
        
    if (op == "add"):
        rest_bin = instruction_bin[7:]
        add(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "addf"):
        rest_bin = instruction_bin[7:]
        addF(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "sub"):
        rest_bin = instruction_bin[7:]
        sub(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "subf"):
        rest_bin = instruction_bin[7:]
        subF(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "mul"):
        rest_bin = instruction_bin[7:]
        mul(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "xor"):
        rest_bin = instruction_bin[7:]
        xor(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "or"):
        rest_bin = instruction_bin[7:]
        BITor(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "and"):
        rest_bin = instruction_bin[7:]
        BITand(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "rs"):
        rest_bin = instruction_bin[5:]
        rs(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "ls"):
        rest_bin = instruction_bin[5:]
        ls(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "movI"):
        rest_bin = instruction_bin[5:]
        movI(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "movf"):
        rest_bin = instruction_bin[5:]
        movF(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "movR"):
        rest_bin = instruction_bin[10:]
        movR(rest_bin)
        flag_reset()
        outputOneLine()
        UpdatePC()
    elif (op == "div"):
        rest_bin = instruction_bin[10:]
        div(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "inv"):
        rest_bin = instruction_bin[10:]
        inv(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "cmp"):
        rest_bin = instruction_bin[10:]
        compare(rest_bin)
        outputOneLine() 
        UpdatePC()
    elif (op == "ld"):
        rest_bin = instruction_bin[5:]
        ld(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "st"):
        rest_bin = instruction_bin[5:]
        st(rest_bin)
        outputOneLine()
        UpdatePC()
    elif (op == "jmp"):
        rest_bin = instruction_bin[8:]
        outputOneLine()
        jmp(rest_bin)
    elif (op == "jlt"):
        rest_bin = instruction_bin[8:]
        temp=flag
        flag=0
        outputOneLine()
        flag=temp
        jlt(rest_bin)
        flag_reset()
    elif (op == "jgt"):
        rest_bin = instruction_bin[8:]
        temp=flag
        flag=0
        outputOneLine()
        flag=temp
        jgt(rest_bin)
        flag_reset()
    elif (op == "je"):
        rest_bin = instruction_bin[8:]
        #next 4 lines only for printing
        temp = flag
        flag = 0
        outputOneLine()
        flag = temp
        je(rest_bin)
        flag_reset()
    else:
        halted = True
        outputOneLine()


def TakeInput():
    global pc, Binary_input, halted
    initializeMem()
    bin_in = ""
    address = 0

    while (bin_in != "0101000000000000"):
        bin_in = input()
        Memory_Heap[address] = bin_in[::]
        address += 1

    while (not halted):
        execution_engine()


# bonus part
def scatterPlot():
    global pc_and_cycle  # (pc,cycle)
    x_axis = []
    y_axis = []
    for i in pc_and_cycle:
        x_axis.append(i[1])
        y_axis.append(i[0])
    plt.scatter(x_axis, y_axis, c="blue")
    plt.xlabel("Cycles")
    plt.ylabel("Program_Counter(Mem_Address)")
    plt.show()
    plt.savefig("graph.png")


if __name__ == "__main__":
    TakeInput()
    for i in Memory_Heap:
        print(i)
    scatterPlot()
