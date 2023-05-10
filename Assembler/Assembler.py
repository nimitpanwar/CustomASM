opcodes = {
    'add': '00000',
    'sub': '00001',
    'mov': '00010',
    # 'mov': '00011',
    'ld': '00100',
    'st': '00101',
    'mul': '00110',
    'div': '00111',
    'rs': '01000',
    'ls': '01001',
    'xor': '01010',
    'or': '01011',
    'and': '01100',
    'not': '01101',
    'cmp': '01110',
    'jmp': '01111',
    'jlt': '11100',
    'jgt': '11101',
    'je': '11111',
    'hlt': '11010',
}

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

type_A = ['add', 'sub', 'mul', 'xor', 'or', 'and']
type_B = ['mov', 'rs', 'ls']
type_C = ['mov', 'not', 'cmp', 'div']
type_D = ['ld', 'st']
type_E = ['jmp', 'jlt', 'jgt', 'je']
type_F = ['hlt']


def encode_type_B(opcode, operands):
    reg, imm = operands.split()
    imm = int(imm[1:])  
    encoded = opcodes[opcode] + '0' + registers[reg] + format(imm, '07b')
    return encoded

def encode_type_C(opcode, operands):
reg1, reg2 = operands.split()
encoded = opcodes[opcode] + '00000' + registers[reg1] + registers[reg2]
return encoded

def encode_type_D(opcode, operands):
reg1, mem_addr = operands.split()
encoded = opcodes[opcode] + registers[reg1] + format(mem_addr, '07b')
return encoded

def encode_type_E(opcode, operands):
mem_addr = operands
endcoded = opcodes[opcode] + '0000' + format(mem_addr, '07b')
return encoded

while True:
    line = input().strip()
    if line == 'hlt':
        break
    
    parts = line.split(' ', 1)
    opcode = parts[0]
    operands = parts[1] if len(parts) > 1 else ''
    if opcode in type_A:  
        reg1, reg2, reg3 = operands.split()
        encoded = opcodes[opcode] + '00' + registers[reg1] + registers[reg2] + registers[reg3]
        print(encoded)
    
    if opcode in type_B and operands[3] == '$':
        encoded = encode_type_B(opcode, operands)
        print(encoded)
        
    elif opcode == 'mov' and operands[3] != '$':
        reg1, reg2 = operands.split()
        encoded = '00011' + '00000' + registers[reg1] + registers[reg2]
        print(encoded)
    
    elif opcode in type_C and opcode != 'mov':
    encoded = encode_type_C(opcode, operands)
    print(encoded)
    
    elif opcode in type_D:
    encoded = encode_type_D(opcode, operands)
    print(encoded)

    elif opcode in type_E:
    encoded = encode_type_D(opcode, operands)
    print(encoded)

    elif opcode in type_E:
    encoded = opcodes[opcode] + '00000000000'
    print(encoded)
        
