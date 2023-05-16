reg_Val_Dict= {
    '000': 0,
    '001': 0,
    '010': 0,
    '011': 0,
    '100': 0,
    '101': 0,
    '110': 0,
}

flags="0000000000000000"

# Opening file
with open("sample_sim.txt") as f:
    input_len=len(f.readlines())
input_list=[]

with open("sample_sim.txt") as g:
    for i in range(input_len):
        input_list.append(g.readline())

# Helper functions
def decToBin(val,bits):
    a=str(bin(val)[2:])
    if len(a)<bits:
        a="0"*(bits-len(a))+a
    return a

def binToDec(bin_num):
    a=int(bin_num,2)
    return a

def getRegVal(reg):
    return reg_Val_Dict.get(reg)

def print_reg():
    for i in reg_Val_Dict:
        print(decToBin(reg_Val_Dict.get(i),16),end=" ")

# Instruction functions
def add(current,flags):
    dest_reg=getRegVal(current[7:10])
    reg1=getRegVal(current[10:13])
    reg2=getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg=reg1+reg2
    if(len(bin(dest_reg))<=7):
        reg_Val_Dict[current[7:10]]=dest_reg
        return flags
    else:
        return flags[0:12]+"1"+flags[13:16]


def sub(current,flag):
    dest_reg=getRegVal(current[7:10])
    reg1=getRegVal(current[10:13])
    reg2=getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    if(reg1>=reg2):
        dest_reg=reg1-reg2
        reg_Val_Dict[current[7:10]]=dest_reg
        return flag
    else:
        return flag[0:12]+"1"+flag[13:16]

def mul(current):
    dest_reg=getRegVal(current[7:10])
    reg1=getRegVal(current[10:13])
    reg2=getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg=reg1*reg2
    if(len(bin(dest_reg))<=7):
        reg_Val_Dict[current[7:10]]=dest_reg
        return flags
    else:
        return flags[0:12]+"1"+flags[13:16]

def XOR(current):
    dest_reg=getRegVal(current[7:10])
    reg1=getRegVal(current[10:13])
    reg2=getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg=reg1^reg2
    reg_Val_Dict[current[7:10]]=dest_reg
    # print(dest_reg)

def OR(current):
    dest_reg=getRegVal(current[7:10])
    reg1=getRegVal(current[10:13])
    reg2=getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg=reg1|reg2
    reg_Val_Dict[current[7:10]]=dest_reg
    # print(dest_reg)

def AND(current):
    dest_reg=getRegVal(current[7:10])
    reg1=getRegVal(current[10:13])
    reg2=getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    dest_reg=reg1 & reg2
    reg_Val_Dict[current[7:10]]=dest_reg
    print(dest_reg)
    
def mov_imm(current):
    dest_reg=binToDec(current[9:16])
    reg_Val_Dict[current[6:9]]=dest_reg

def r_shift(current):
    dest_reg=getRegVal(current[6:9])
    dest_reg=dest_reg>>binToDec(current[9:16])
    reg_Val_Dict[current[6:9]]=dest_reg

def l_shift(current):
    dest_reg=getRegVal(current[6:9])
    dest_reg=dest_reg<<binToDec(current[9:16])
    reg_Val_Dict[current[6:9]]=dest_reg

def mov_reg(current):
    reg1=getRegVal(current[13:16])
    dest_reg=reg1
    reg_Val_Dict[current[10:13]]=dest_reg

def div(current,flag):
    reg3=getRegVal(current[10:13])
    reg4=getRegVal(current[13:16])
    # print(dest_reg,reg1,reg2)
    if(reg4!=0):
        quotient=reg3//reg4
        remainder=reg3%reg4
        reg_Val_Dict['000']=quotient
        reg_Val_Dict['001']=remainder
        return flag
    else:
        return flag[0:12]+"1"+flag[13:16]
    
def cmp(current,flag):
    reg1=getRegVal(current[10:13])
    reg2=getRegVal(current[13:16])
    if(reg1<reg2):
        flag=flag[0:13]+"1"+flag[14:16]
    elif(reg1>reg2):
        flag=flag[0:14]+"1"+flag[15:16]
    elif(reg1==reg2):
        flag=flag[0:15]+"1"+flag[16:16]
    return flag

def inv(current):
    reg2=getRegVal(current[13:16])
    not_val=~reg2
    reg_Val_Dict[current[10:13]]=not_val

def jmp(current):
    pc=binToDec(current[9:16])
    return pc

def jlt(pc,current):
    if flags[13]=="1":
        pc=binToDec(current[9:16])
    else:
        pc+=1
    return pc

def jgt(pc,current):
    if flags[14]=="1":
        pc=binToDec(current[9:16])
    else:
        pc+=1
    return pc

def je(pc,current):
    if flags[15]=="1":
        pc=binToDec(current[9:16])
    else:
        pc=pc+1
    return pc

def ld(current):
    pass

def st(current):
    pass 

# Program variables
pc=0
output_list=[]
halted=False
i=0

# Main execution
while(halted!=True):
    # variables
    bin_pc=decToBin(pc,7)
    curr=input_list[pc]
    curr_inst=(curr[0:5])
    jump_inst=False
    newFlags=flags
    
    # Identifying opcode and executing instructions 
    if(curr_inst=="00000"):
        newFlags=add(curr,flags)    
    elif(curr_inst=="00001"):
        newFlags=sub(curr,flags)
    elif(curr_inst=="00110"):
        newFlags=mul(curr)
    elif(curr_inst=="01010"):
        XOR(curr)
    elif(curr_inst=="01011"):
        OR(curr)
    elif(curr_inst=="01100"):
        AND(curr)
    elif(curr_inst=="00010"):
        mov_imm(curr)
    elif(curr_inst=="01000"):
        r_shift(curr)
    elif(curr_inst=="01001"):
        l_shift(curr)
    elif(curr_inst=="00011"):
        mov_reg(curr)
    elif(curr_inst=="00111"):
        newFlags=div(curr,flags)
    elif(curr_inst=="01101"):
        inv(curr)
    elif(curr_inst=="01110"):
        newFlags=cmp(curr,flags)
    elif(curr_inst=="01111"):
        pc=jmp(curr)
        jump_inst=True
    elif(curr_inst=="11100"):
        pc=jlt(pc,curr)
        jump_inst=True
    elif(curr_inst=="11101"):
        pc=jgt(pc,curr)
        jump_inst=True
    elif(curr_inst=="11111"):
        pc=je(pc,curr)
        jump_inst=True
    elif(curr_inst=="11010"):
        halted=True

    # Setting/Resetting flags reg
    if(newFlags==flags):
        flags="0000000000000000"
    else:
        flags=newFlags

    print(bin_pc,end=" ")
    print_reg()
    print(flags)
    print("") 

    # If no jump is encountered increment pc by 1 
    if(jump_inst==False):
        pc+=1
    
