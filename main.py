from os.path import exists
import struct

# the byte size of the buffer to read in
SIZE = 4

# a list of the full instructions and the binary correlating to them
binary_list = []
instructions = []

# a dictionary of the special registers and how to translate to them
spec_registers = {
    28: "SP",
    29: "FP",
    30: "LR",
    31: "XZR"
}

# a dictionary for all of the conditions for b.cond instruction
b_cond = {
    0: "EQ",
    1: "NE",
    2: "HS",
    3: "LO",
    4: "MI",
    5: "PL",
    6: "VS",
    7: "VC",
    8: "HI",
    9: "LS",
    10: "GE",
    11: "LT",
    12: "GT",
    13: "LE"
}


# gets the integer negative number of a value in twos compliment form
def twos_compliment(br_address, length):
    inverse = br_address ^ (2 ** (length + 1) - 1)
    temp_address = bin(inverse + 1)[3:]
    br_address = -1 * int(temp_address, 2)
    return br_address


'''
The beginning of the "type" functions.

Each of these is mapped to a specific type of legv8 instruction and will translate its binary into a human readable
legv8 instruction.

@:param
    opcode: the opcode of the instruction being decoded
    binary: the binary for the instruction
    i: used to determine the position of a label in the instruction set (B and CB type instructions only)
@:returns 
    inst: the completed instruction
'''


# function to get r-type instructions
def r_type(opcode, binary, i):
    rm = int(binary[0: 5], 2)
    shamt = int(binary[5: 11], 2)
    rn = int(binary[11: 16], 2)
    rd = int(binary[16: 21], 2)

    shamt = "#" + str(shamt) if shamt != 0 else ""
    rd = "X" + str(rd) + ", " if rd not in spec_registers.keys() else spec_registers[rd] + ", "
    rn = "X" + str(rn) + ", " if rn not in spec_registers.keys() else spec_registers[rn] + ", "
    rm = "X" + str(rm) if rm not in spec_registers.keys() else spec_registers[rm]

    rd = rd if opcode != "PRNL" and opcode != "DUMP" and opcode != "HALT" else ""
    rn = rn if opcode != "PRNT" and opcode != "PRNL" and opcode != "DUMP" and opcode != "HALT" else ""
    rm = rm if opcode != "LSL" and opcode != "LSR" and opcode != "PRNT" and opcode != "PRNL" and opcode != "DUMP" and opcode != "HALT" else ""

    rd = rd if opcode != "PRNT" else rd[0: len(rd) - 2]

    inst = opcode + " " + rd + rn + rm + shamt
    return inst


# function to get i-type instructions
def i_type(opcode, binary, i):
    alu_immediate = int(binary[0: 12], 2)
    rn = int(binary[12: 17], 2)
    rd = int(binary[17: 22], 2)

    alu_immediate = "#" + str(alu_immediate)
    rn = "X" + str(rn) + ", " if rn not in spec_registers.keys() else spec_registers[rn] + ", "
    rd = "X" + str(rd) + ", " if rd not in spec_registers.keys() else spec_registers[rd] + ", "

    inst = opcode + " " + rd + rn + alu_immediate
    return inst


# function to get d-type instructions
def d_type(opcode, binary, i):
    dt_address = int(binary[0: 9], 2)
    # op = int(binary[9: 11], 2) // not needed
    rn = int(binary[11: 16], 2)
    rt = int(binary[16: 21], 2)

    dt_address = "#" + str(dt_address) + "]"
    rn = "[X" + str(rn) + ", " if rn not in spec_registers.keys() else "[" + spec_registers[rn] + ", "
    rt = "X" + str(rt) + ", " if rt not in spec_registers.keys() else spec_registers[rt] + ", "

    inst = opcode + " " + rt + rn + dt_address
    return inst


label_num = 1
label_dict = {}


# function to get b-type instructions
def b_type(opcode, binary, i):
    global label_num
    label = None

    br_address = int(binary, 2)

    if br_address > len(instructions):
        br_address = twos_compliment(br_address, len(binary))

    if br_address > len(instructions) or br_address < -len(instructions):
        label = "LR"

    if not label:
        if (i + br_address) in label_dict.keys():
            label = label_dict[i + br_address]
        else:
            label = "label" + str(label_num)
            label_num += 1
            label_dict[i + br_address] = label

    inst = opcode + " " + label
    return inst


# function to get cb-type instructions
def cb_type(opcode, binary, i):
    global label_num
    cond_br_address = int(binary[0: 19], 2)
    rt = int(binary[19: 24], 2)

    if cond_br_address > len(instructions):
        cond_br_address = twos_compliment(cond_br_address, 19)

    if (i + cond_br_address) in label_dict.keys():
        label = label_dict[i + cond_br_address]
    else:
        label = "label" + str(label_num)
        label_num += 1
        label_dict[i + cond_br_address] = label

    if opcode == "B.cond":
        inst = "B." + b_cond[rt] + " " + label
    else:
        inst = opcode + " X" + str(rt) + ", " + label

    return inst


# the full dictionary of all of the opcodes and what instruction and function they map to
ops_dict = {
    '0b10001011000': ["ADD", r_type],
    '0b10001010000': ["AND", r_type],
    '0b11010110000': ["BR", b_type],
    '0b11111111110': ["DUMP", r_type],
    '0b11001010000': ["EOR", r_type],
    '0b11111111111': ["HALT", r_type],
    '0b11111000010': ["LDUR", d_type],
    '0b11010011011': ["LSL", r_type],
    '0b11010011010': ["LSR", r_type],
    '0b10011011000': ["MUL", r_type],
    '0b10101010000': ["ORR", r_type],
    '0b11111111100': ["PRNL", r_type],
    '0b11111111101': ["PRNT", r_type],
    '0b11111000000': ["STUR", d_type],
    '0b11001011000': ["SUB", r_type],
    '0b11101011000': ["SUBS", r_type],
    '0b1101001000': ["EORI", i_type],
    '0b1001000100': ["ADDI", i_type],
    '0b1001001000': ["ANDI", i_type],
    '0b1011001000': ["ORRI", i_type],
    '0b1101000100': ["SUBI", i_type],
    '0b1111000100': ["SUBIS", i_type],
    '0b10110101': ["CBNZ", cb_type],
    '0b10110100': ["CBZ", cb_type],
    '0b1010100': ["B.cond", cb_type],
    '0b100101': ["BL", b_type],
    '0b101': ["B", b_type]
}


# reads in the contents of the machine file in 4 byte (32 bit) chunks and appends them to a list of binaries
def file_read(file_name):
    if ".machine" not in file_name:
        print("File must be a \'.machine\' file")
        exit(1)
    if not exists(file_name):
        print("\"" + file_name + "\" does not exist")
        exit(1)

    with open(file_name, mode='rb') as file:
        while True:
            buffer = file.read(SIZE)
            if buffer:
                value = struct.unpack('>I', buffer)[0]
                binary_list.append(bin(value))
            else:
                break
    file.close()


# gets the opcodes of the instructions
def get_opcodes():
    for i, binary in enumerate(binary_list):
        for key in ops_dict.keys():
            if str(key) in binary:
                instructions.append(ops_dict[key])
                binary_list[i] = binary_list[i].replace(str(key), "")
                break


# calls the type function for the specific instruction
def set_instructions():
    global label_num
    for i, instruction in enumerate(instructions):
        opcode = instruction[0]
        instructions[i] = instruction[1](opcode, binary_list[i], i)


# prints the instruction list
def print_instructions():
    for i, instruction in enumerate(instructions):
        if i in label_dict.keys():
            print(label_dict[i] + ":")
        print(instruction)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str, help="The name of the legv8 binary file to be disassembled")

    args = parser.parse_args()
    file_read(file_name=args.file_name)

    get_opcodes()
    set_instructions()
    print_instructions()
