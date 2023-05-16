registers = {
    'R0': '000',
    'R1': '001',
    'R2': '010',
    'R3': '011',
    'R4': '100',
    'R5': '101',
    'R6': '110',
    'FLAGS': '111',
}

opcode = {
    'addf' : '10000',
    'subf' : '10001',
    'movf' : '00010',
    'add'  : '00000',
    'sub'  : '00001',
    'mov1' : '00010',
    'mov2' : '00011',
    'ld'   : '00100',
    'st'   : '00101',
    'mul'  : '00110',
    'div'  : '00111',
    'rs'   : '01000',
    'ls'   : '01001',
    'xor'  : '01010',
    'or'   : '01011',
    'and'  : '01100',
    'not'  : '01101',
    'cmp'  : '01110',
    'jmp'  : '01111',
    'jlt'  : '11100',
    'jgt'  : '11101',
    'je'   : '11111',
    'hlt'  : '11010'
}

variable_dict = {}
global label_dict 
label_dict = {}
var_temp_list = [0]
lst = []

typeA_list = ["add","sub","mul","xor","or","and","addf","subf"]
typeB_list = ["rs","ls","movf"]
typeC_list = ["cmp","not","div"]
typeABC_list = typeA_list + typeB_list + typeC_list
typeD_list = ["ld","st"]
typeE_list = ["jmp","jlt","jgt","je"]
typeF_list = ["hlt"]
type_total = typeA_list + typeB_list + typeC_list + typeD_list + typeE_list + typeF_list + ["mov", "var"]

def bitrep(num):
    st = ''
    while int(num) > 0:
        remainder = int(num) % 2
        st += str(remainder)
        num = int(num)//2
    return st[::-1]    

def unused_add(str1,size_req):
	return (size_req-len(str1))*"0"+str1

def whole2bin(num):
    st = ''
    while int(num) > 0:
        remainder = int(num) % 2
        st += str(remainder)
        num = int(num)//2    
    return st[::-1] 

def dec2bin(num,temp):
    num = '0.'+num
    str_out = ''
    float_num = float(num)
    loop_error_detector = 0
    while(float_num!=0 and loop_error_detector < 8):
        float_num*=2
        str_out += str(int(float_num))
        float_num = float_num - int(float_num)
        loop_error_detector+=1
    if (loop_error_detector == 8):
        print(f"Error at instruction line: {temp}")
        exit()
    return str_out

def bin_convert(n,temp):
    whole_num, dec_num = n.split(".")
    float_str = (whole2bin(whole_num) + '.' + dec2bin(dec_num,temp))
    float_num = float(float_str)
    float_len = len(float_str)
    if (float_len>8):
        print(f"Error at instruction line: {temp}")
        exit()
    exp_counter = 0
    while(float_num>2):
        float_num/=10
        exp_counter+=1
    final_str = str(float_num)[0:float_len]
    exp_str = n_bits(whole2bin(exp_counter),3)
    mantissa_str = n_bits_opp(final_str[2:float_len],5)
    ieee_final = exp_str + mantissa_str
    if len(ieee_final)>8:
        print(f"Error at instruction line: {temp}")
        exit()
    return ieee_final

def n_bits(bin,n):
    if len(bin)<n:
        while len(bin) != n:
            bin = '0' + bin    
    return bin 

def n_bits_opp(bin,n):
    if len(bin)<n:
        while len(bin) != n:
            bin = bin + '0' 
    return bin 

def typeA(instruction,r1,r2,r3):
    if (r1.upper() in registers) and (r2.upper() in registers) and (r3.upper() in registers):
        pass
    else:
        print("The register used is not of the declared type")
        exit()

    c1 = registers[r1.upper()]
    c2 = registers[r2.upper()]
    c3 = registers[r3.upper()]

    op = opcode[instruction]
    print(op + '0'*2 + c1 + c2 + c3)


def typeB(instruction, reg, imm_val, temp):

    op = opcode[instruction]
    c1 = registers[reg.upper()]
    imm_val = (imm_val.replace('$', '')).strip()

    if (op=='00010' or op=='01000' or op=='01001'):
        int_imm_val = int(imm_val)
        bin_imm_val = bitrep(int_imm_val)
        print(op + '0' + c1  + unused_add(bin_imm_val,7))
        return

    else:
        final_ieee_format = bin_convert(imm_val,temp)
        output_list.append(op+c1+final_ieee_format)


def typeC(instruction,r1,r2):
    if (r1.upper() in registers) and (r2.upper() in registers):
        pass
    else:
        print("The register used is not of the declared type")
 
    op = opcode[instruction]
    c1 = registers[r1.upper()]
    c2 = registers[r2.upper()]

    print(op  + '0' * 5 + c1  + c2)


def typeD(instruction, r1, variable_name):

    op = opcode[instruction]
    c1 = registers[r1.upper()]
    mem_addr = variable_dict[variable_name]
    
    print(op + '0' + c1  + mem_addr)
 
    
def typeE(instruction, mem_addr):

    label_instruction_num = label_dict[mem_addr]
    print(opcode[instruction] + '0'*4  + unused_add(bitrep(label_instruction_num),7))


def typeF(instruction):

    print(opcode[instruction] + '0'*11)

def instruction_init(input,temp):
    if (input[0] in typeA_list):
        typeA(input[0],input[1],input[2],input[3])
    elif (input[0] in typeB_list):
        typeB(input[0],input[1],input[2],temp)
    elif (input[0] in typeC_list):
        typeC(input[0],input[1],input[2])
    elif (input[0] in typeD_list):
        typeD(input[0],input[1],input[2])
    elif (input[0] in typeE_list):
        typeE(input[0],input[1])
    elif (input[0] in typeF_list):
        typeF(input[0])
    elif (input[0] == "mov"):
        if (input[2][0]=="$"):
            typeB("mov1",input[1],input[2],temp)
        else:
            typeC("mov2",input[1],input[2])
    else:
        pass

def var_define(input, var_counter):
    variable_dict[input[1]] = unused_add(bitrep(var_counter),7)
    return

def identify_input(input,temp):
    if (input == []):
        return
    elif (input[0] == "var"):
        global var_counter
        var_counter = var_temp_list[0]
        var_define(input, var_counter+input_count-var_count_final)
        var_temp_list[0] += 1
        return
    elif (input[0][-1] == ":"): 
        label_rest_input = input[1:]
        instruction_init(label_rest_input,temp)
        return
    else:
        instruction_init(input,temp)
        return

def line_check(line_input_count):
    if (line_input_count > 128):
        print("Total instruction lines exceeded count of 128")
        exit()

def var_error(inp,var_count):
        cnt = 0
        i = 0
        while (inp[i][0] == 'var'):
            cnt+=1
            i+=1
        if (cnt != var_count):
            while (inp[i][0] != 'var'):
                i+=1
            print(f"Error : var defined at {i} instruction, not at beginning of the file")
            exit()

def halt_error(inp):
    hlt_count = 0
    for i in inp:
        if (inp[i][-1] == 'hlt'):
            hlt_count += 1
    if (hlt_count == 0):
        print("Error: hlt instruction missing")
        exit()
    if (hlt_count==1 and inp[len(inp)-1][-1] != 'hlt'):
        print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: hlt not being used as the last instruction") 
        exit()
    if (hlt_count>1):
        print("Error: More than one hlt")
        exit()

def lbl_error(label_list):

    a = set(label_list)
    
    if len(a) != len(label_list):
        print ("Error: Defining label with same name multiple times!")
        exit()
    
def typo_error(instructions):
    for i in instructions:
        if instructions[i][0] not in type_total:
            with open("output","w")as f:
                f.write("")
            print(f'Error at instruction line {i+var_count_final+1}'+'\n'+f"Error: Instruction {instructions[i][0]} is not a valid instruction")   
            exit()

def reg_error(instructions, var_list, label_list):
    
    for i in instructions:
        if instructions[i][0] in ['add', 'sub', 'mul', 'xor', 'or', 'and','addf','subf']:   
            if len(instructions[i]) != 4:
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid instruction length")          
                exit()
            
            if (instructions[i][1] not in registers.keys()) or (instructions[i][2] not in registers.keys()) or (instructions[i][3] not in registers.keys()):
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Wrong register input")          
                exit()
                
            if (instructions[i][1] == 'FLAGS') or (instructions[i][2] == 'FLAGS') or (instructions[i][3] == 'FLAGS'):
                print(f'Error at instruction line {i+var_count_final}'+'\n'+'Error: Invalid use of FLAGS register')          
                exit()
                
        elif instructions[i][0] == 'mov':

            if instructions[i][2][0] == '$':
                imm = int(instructions[i][2][1:])
                if (imm > 127) or (imm < 0):
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid immediate value")          
                    exit()
                if len(instructions[i]) != 3:
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid instruction length")          
                    exit()
                if instructions[i][1] not in registers.keys():
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid register")          
                    exit()
                if instructions[i][1] == 'FLAGS':
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid use of FLAGS register")          
                    exit()
                
        elif instructions[i][0] == 'movf':

            if instructions[i][2][0] == '$':
                temp_imm, dec_imm = (instructions[i][2][1:]).split(".")
                imm = int(temp_imm)
                if (imm > 252) or (imm < 0):
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid immediate value")          
                    exit()
                if len(instructions[i]) != 3:
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid instruction length")          
                    exit()
                if instructions[i][1] not in registers.keys():
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid register")          
                    exit()
                if instructions[i][1] == 'FLAGS':
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid use of FLAGS register")          
                    exit()

            else:
                if len(instructions[i]) != 3:
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid instruction length")          
                    exit()
                
                if instructions[i][1] not in registers.keys() or instructions[i][2] not in registers.keys():
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid register")          
                    exit()

                if instructions[i][2] == 'FLAGS':
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid use of FLAGS register")          
                    exit()
                
        elif instructions[i][0] == 'ld' or instructions[i][0] == 'st':

            if len(instructions[i]) != 3:
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid instruction length")          
                exit()
            
            if instructions[i][1] not in registers.keys():
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid register used!!")          
                exit()
            if instructions[i][1] == 'FLAGS':
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid use of FLAGS register")                                 
                exit()
            
            if instructions[i][2] not in var_list:
                print(f'Error at instruction line {i+var_count_final+1}'+'\n'+f'Error: Undefined variable used : {instructions[i][2]} not defined')   
                exit()    
    
        elif instructions[i][0] in ['div', 'not','cmp']:
            if len(instructions[i]) != 3:
                print(f'Error at instruction line {i+var_count_final+2}'+'\n'+"Error: Invalid Instruction length : only 2 registers are accepted")   
                exit()
            
            if instructions[i][1] not in registers.keys() or instructions[i][2] not in registers.keys():
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid register used")          
                exit()
                
            if instructions[i][1] == 'FLAGS' or instructions[i][2] == 'FLAGS':
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Invalid use of FLAGS register")          
                exit()
            
        elif instructions[i][0] == 'rs' or instructions[i][0] == 'ls':
            if len(instructions[i]) != 3:
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid Instruction length")                 
                exit()
            
            if instructions[i][1] not in registers.keys():
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid register used")          
                exit()
            
            if instructions[i][1] == 'FLAGS':
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid use of FLAGS register")          
                exit()
            
            if instructions[i][2][0] != '$':
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid Syntax :Use '$' before the number")          
                exit()
            
            if instructions[i][2][0] == '$':                        
                imm = int(instructions[i][2][1:])
                if (imm > 127) or (imm < 0):
                    print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Illegal Immediate value entered")          
                    exit()
        
        elif instructions[i][0] in ['jmp', 'jlt', 'jgt', 'je']:
            
            if len(instructions[i]) != 2:
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid Instruction length")          
                exit()
            
            if (instructions[i][1]+":") not in label_list:
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Undefined label used!")          
                exit()
         
        elif instructions[i][0] == 'hlt':
            
            if len(instructions[i]) != 1:
                print(f'Error at instruction line {i+var_count_final}'+'\n'+"Error: Invalid instruction length (giving commans to hlt)")                  
                exit()
        
        else:
            print(f'Error at instruction line {i+var_count_final}'+'\n'+"General Syntax error")          
            exit()            
    return None                
    
global input_count
global inp
inp = {} 
instructions = {}
vars = {} 
labels = {}
input_count = 0 
lbl_count = 0 
inst_count = 0 
var_list = [] 
global var_count
var_count = 0
label_list=[] 
output_list=[] 

while True:
    try:
        l = input().split()
        if l != []:
            inp[input_count] = l
            input_count += 1
            if l[-1] == 'hlt':
                break

    except EOFError:
        break    

  
line_check(input_count)
global var_count_final
    

for i in inp:
    if inp[i][0] == 'var':
        vars[var_count] = inp[i]
        if len(inp[i])>0:
            var_list.append(inp[i][1])
            var_count += 1

    elif inp[i] == []:
        pass

    elif inp[i][0] in type_total:
        instructions[inst_count] = inp[i]
        inst_count += 1
        
    elif inp[i][0][-1] == ':' and inp[i][0][-2] != ' ':
        labels[lbl_count] = inp[i]
        label_dict[inp[i][0][:-1]] = i - var_count
        lbl_count += 1
        label_list.append(inp[i][0])

    elif inp[i][0] not in type_total and ":" not in inp[i][0]:
        instructions[inst_count] = inp[i]
        inst_count += 1
        break
    else:
        var_count_final = var_count
        reg_error(instructions, var_list, label_list)

var_count_final = var_count

typo_error(instructions)
reg_error(instructions, var_list, label_list)
halt_error(inp)
var_error(inp, var_count)
lbl_error(label_list)

for i in inp:
    temp = i
    identify_input(inp[i],temp)
