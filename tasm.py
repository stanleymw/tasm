'''
test asm interpreter

'''

import sys
# HANDLE INPUTS
num_args = len(sys.argv) - 1

#print(num_args, sys.argv)

if num_args < 1:
    print("Fatal error: no input files")



DEBUG = False
LIST_INSTRUCTIONS = False
TARGET_FILE = None
if num_args >= 1:
    TARGET_FILE = sys.argv[1]


if "-d" in sys.argv:
    DEBUG = True
if "-i" in sys.argv:
    LIST_INSTRUCTIONS = True


def runProgram(target_file):
    output_code = 0
    program = open(target_file,"r")
    import math
    #inputs = [int(i) for i in program.readline().split()]
    #current_input = 0

    ACC = 0
    REG = {"SP": 0, "BP": 0, "FRT": 0, "IP":0} #Program registers
    FLAGS = {"ZF": 0, "SF": 0}
    STACK = [] #stack

    #SP = stack pointer
    #BP = base pointer
    #FRT = function return register
    #IP = instruction pointer
    LABELS = {}

    # CREATE LABELS FIRST




    PROGRAM_LINES = program.read().split("\n")
    for i,line in enumerate(PROGRAM_LINES):
        if len(line.strip()) > 0 and line.strip()[-1] == ":":
            LABELS[line.strip()[:-1]] = i+1

    if DEBUG:
        print("DISCOVERED LABELS: (LABEL: VALUE)",LABELS)

    
    while True:

        instruction = PROGRAM_LINES[REG["IP"]]
        #print(instruction)
        if instruction.strip()=="":
            REG["IP"]+=1
            continue
        elif instruction[0] == "#":
            REG["IP"]+=1
            continue

        a = instruction.split() 
        if "END" in a:
            break
        if LIST_INSTRUCTIONS:
            print(a)
        #if len(a) < 3:
        #    a = [""] + a
        
        opcode = a[0]

        # islit = None
        # literalval = None
        # if loc[0] == "=":
        #     # value at loc is a literal
        #     islit = True
        #     literalval = int(loc[1:])
        for val in a:
            if str(val).strip()[0] == "=":
                #check if its a literal
                REG[str(val).strip()] = int(str(val).strip()[1:])

        
        if opcode == "ADD":
            REG[a[1]] = REG[a[1]] + REG[a[2]]
        elif opcode == "SUB":
            REG[a[1]] = REG[a[1]] - REG[a[2]]
        elif opcode == "MULT":
            REG[a[1]] = REG[a[1]] * REG[a[2]]
        elif opcode == "IDIV":
            REG[a[1]] = REG[a[1]] // REG[a[2]]
        elif opcode == "MOD":
            REG[a[1]] = REG[a[1]] % REG[a[2]]
        elif opcode == "NROOT":
            REG[a[1]] = REG[a[1]]**(1/REG[a[2]])
        elif opcode == "RETC":
            output_code = REG[a[1]]
        elif opcode == "BG":
            if ACC>0:
                REG["IP"]=LABELS[a[1]]-1
        elif opcode == "BE":
            if ACC==0:
                REG["IP"]=LABELS[a[1]]-1
        elif opcode == "BL":
            if ACC<0:
                REG["IP"]=LABELS[a[1]]-1
        elif opcode == "JMP":
            REG["IP"]=LABELS[a[1]]-1

        elif opcode == "READ":
            REG[a[1]] = int(input())

        elif opcode == "PRINT":
            print(REG[a[1]])


        elif opcode == "PUSH":
            STACK.append(REG[a[1]])
            REG["ESP"] += 1
        elif opcode == "POP":
            REG[a[1]] = STACK.pop(REG["ESP"])
            REG["ESP"] -= 1
        elif opcode == "MOV":
            REG[a[1]] = REG[a[2]]
        elif opcode == "CMP":
            tmp = REG[a[1]] - REG[a[2]]
            if tmp == 0:
                FLAGS["ZF"] = 1
            elif tmp < 0:
                # Positive SF flag (sign flag) indicates that last result was positive
                FLAGS["SF"] = 0
            elif tmp > 0:
                FLAGS["SF"] = 1
        elif opcode == "JE":
            if FLAGS["ZF"]:
                REG["IP"]=LABELS[a[1]]-1
        elif opcode == "JNE":
            if not FLAGS["ZF"]:
                REG["IP"]=LABELS[a[1]]-1
        elif DEBUG:
            print("UNKNOWN INSTRUCTION:",a)


        REG["IP"]+=1
        if LIST_INSTRUCTIONS:
            print("RAN INSTRUCTION",a,"IP:",REG["IP"], "ACC:",ACC, "REGISTRY:",REG, "LBLS:",LABELS, "STACK:", STACK, "FLAGS:",FLAGS)


    if DEBUG:
        print("Program exited with output code {}. Debug information:".format(output_code), "ACC=",ACC,"REGISTRY=",REG,"LABELS=",LABELS)


if TARGET_FILE:
    runProgram(TARGET_FILE)
