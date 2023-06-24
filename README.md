# pa2
A binary disassembler made in python for Com S 321. <br><br>

For this assignment, you will be implementing a disassembler for the binaries that run on our LEGv8 emulator in binary mode.  Your disassembler will handle input files containing any number of contiguous, binary LEGv8 instructions encoded in big-endian byte order.  The input file name will be given as the first command line parameter.  Your output, printed to the terminal, should be--modulo some caveats discussed below--the original LEGv8 assembly code that generated the binary. <br><br>

Except that it ignores the PC and flow control, a disassembler essentially implements the first two stages (fetch and decode) of the five-stage pipeline described in lecture and the textbook.  A working disassembler requires perhaps half of the total work of building a binary emulator. <br><br>

Your disassembler should fully support the following set of LEGv8 instructions: <br><br>

ADD <br>
ADDI <br>
AND <br>
ANDI <br>
B <br>
B.cond: This is a CB instruction in which the Rt field is not a register, but a code that indicates the condition extension. These have the values (base 16): <br>
&nbsp;&nbsp;&nbsp;&nbsp;0: EQ. <br>
&nbsp;&nbsp;&nbsp;&nbsp;1: NE. <br>
&nbsp;&nbsp;&nbsp;&nbsp;2: HS. <br>
&nbsp;&nbsp;&nbsp;&nbsp;3: LO. <br>
&nbsp;&nbsp;&nbsp;&nbsp;4: MI. <br>
&nbsp;&nbsp;&nbsp;&nbsp;5: PL. <br>
&nbsp;&nbsp;&nbsp;&nbsp;6: VS. <br>
&nbsp;&nbsp;&nbsp;&nbsp;7: VC. <br>
&nbsp;&nbsp;&nbsp;&nbsp;8: HI. <br>
&nbsp;&nbsp;&nbsp;&nbsp;9: LS. <br>
&nbsp;&nbsp;&nbsp;&nbsp;a: GE. <br>
&nbsp;&nbsp;&nbsp;&nbsp;b: LT. <br>
&nbsp;&nbsp;&nbsp;&nbsp;c: GT. <br>
&nbsp;&nbsp;&nbsp;&nbsp;d: LE. <br>
BL <br> 
BR: The branch target is encoded in the Rn field. <br>
CBNZ <br>
CBZ <br>
EOR <br>
EORI <br>
LDUR <br>
LSL: This instruction uses the shamt field to encode the shift amount, while Rm is unused. <br>
LSR: Same as LSL. <br>
ORR <br>
ORRI <br>
STUR <br>
SUB <br>
SUBI <br>
SUBIS <br>
SUBS <br>
MUL <br>
PRNT: This is an added instruction (part of our emulator, but not part of LEG or ARM) that prints a register name and its contents in hex and decimal.  This is an R instruction.   The opcode is 11111111101.  The register is given in the Rd field. <br>
PRNL: This is an added instruction that prints a blank line.  This is an R instruction.  The opcode is 11111111100. <br>
DUMP: This is an added instruction that displays the contents of all registers and memory, as well as the disassembled program.  This is an R instruction.  The opcode is 11111111110. <br>
HALT: This is an added instruction that triggers a DUMP and terminates the emulator.  This is an R instruction.  The opcode is 11111111111 <br><br>
You may implement your disassembler in any language you like so long is it builds (if a compiled language) and runs on pyrite.  This restriction is necessary in order to give the TAs a common platform to test and evaluate your solution.  Most important, popular, or trendy languages are already installed on pyrite, including C, C++, Java, and Python.  If your language of choice is not installed, you are welcome to contact the system administrators <coms-ssg@iastate.edu> to request its installation; however, I can make no guarantees about whether or not they will do the installation for you, and--if they do--how timely their service will be. <br><br>

In order to minimize the burden on the TAs, your solution should include two bourne shell scripts in the top level directory: build.sh and run.sh.  build.sh should include the executable command(s) necessary to build your program; if your program is in an interpreted language, this final may be empty.  run.sh should take one parameter, the name of a LEGv8 binary file, and pass it to your disassembler.  For instance, if I were implementing my disassembler in C and had the program in a source file named disasm.c, my build.sh would contain exactly: <br><br>

gcc disasm.c -o disasm <br><br>

And my run.sh would contain exactly: <br><br>

./disasm $1 <br><br>

Bourne shell script are simply text files, and $1 is interpreted as the first positional parameter passed to the script on the command line.  To run your scripts, execute sh build.sh or sh run.sh <legv8 assembly file>. <br><br>

The data lost in converting from assembly to machine code are comments and label names.  Both of these are completely irretrievable, but new label names can be generated, even if these are devoid of the semantic meanings imparted by the original program author.  For example, you can simply number the labels: "label1", "label2", etc.  Your disassembled output should generate new label names such that our emulator can execute or assemble your generated code.  Your "reassembled disassembly" should be byte-for-byte identical to the input. <br><br>

To use the emulator as an assembler (the output file will have the same name is the input with ".machine" concatenated onto the end): ./legv8emul <legv8 assembly file> -a <br><br>

To run the emulator in binary emulation mode: ./legv8emul <legv8 binary file> -b
