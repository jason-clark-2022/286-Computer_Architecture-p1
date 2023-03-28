# File main.py
# Name: Connor Stewart
# Date: 09/20/2020

import sys
import os
import struct


with open ( sys.argv[2], 'rb') as file:
    data = file.read()

fileOut = open("OUTPUTFILENAME_dis.txt", "w")
validBits = []
opBits = []
funcBits = []
rsBits = []
rtBits = []
rdBits = []
offBits = []
offBits18 = []
saBits = []
registers = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
line = []
cycleCount = 0


for i in range(0, len(data), 4):
    asInt = struct.unpack_from('>i', data, i)[0]
    asUInt = struct.unpack_from('>I', data, i)[0]
    asBin = format(asUInt, '0>32b')
    asBinSpace = asBin[0] + ' ' + asBin[1:6] + ' ' + asBin[6:11] + ' ' + asBin[11:16] + ' ' + asBin[16:21] + ' ' + asBin[21:26] + ' ' + asBin[26:]
    valid = asUInt >> 31
    opcode = asUInt >> 26
    fnCode = int(asBin[26:], 2)
    rsInt = int(asBin[6:11], 2)
    rtInt = int(asBin[11:16], 2)
    offset = int(asBin[16:], 2)
    offset18 = int(asBin[16:], 2) << 2
    shiftAmount = int(asBin[21:26], 2)
    jTarget = int(asBin[6:], 2) << 2
    rd = ((asUInt << 16) & 0x0FFFFFFFF) >> 27
    rs = ((asUInt << 6) & 0x0FFFFFFFF) >> 27
    rt = ((asUInt << 11) & 0x0FFFFFFFF) >> 27
    fn = ((asUInt) & 0x0FFFFFFFF) 
    text = ''
    if valid == 0: text = 'invalid instruction'
    elif opcode == 40: text = 'ADDI\tR' + str(rt) + ', R' + str(rs) + ', #' + str(offset)
    elif opcode == 43: text = 'SW\tR' + str(rt) + ', ' + str(offset) + '(R' + str(rs) + ')' 
    elif opcode == 35: text = 'LW\tR' + str(rt) + ', ' + str(offset) + '(R' + str(rs) + ')'
    elif opcode == 34: text = 'J\t#' + str(jTarget)
    elif opcode == 36: text = 'BEQ\tR' + str(rs) + ',R' + str(rt) + ' ' + str(offset)
    elif opcode == 33: text = 'BLTZ\tR' + str(rs) + ', #' + str(offset18)
    elif opcode == 60: text = 'MUL\tR' + str(rd) + ', R' + str(rs) + ', R' + str(rt)
    elif ( opcode == 32 and fnCode == 8 ): text = 'JR\tR' + str(rs)
    elif ( opcode == 32 and fnCode == 32 ): text = 'ADD\tR' + str(rd) + ', R' + str(rs) + ', R' + str(rt)
    elif ( opcode == 32 and fnCode == 0 ): text = 'SLL\tR' + str(rd) + ', R' + str(rt) + ', #' + str(shiftAmount)
    elif ( opcode == 32 and fnCode == 34 ): text = 'SUB\tR' + str(rd) + ', R' + str(rs) + ', R' + str(rt)
    elif ( opcode == 32 and fnCode == 2 ): text = 'SRL\tR' + str(rd) + ', R' + str(rt) + ', #' + str(shiftAmount)
    elif ( opcode == 32 and fnCode == 13 ): text = 'BREAK'
    elif ( opcode == 32 and fnCode == 36 ): text = 'AND\tR' + str(rd) + ', R' + str(rs) + ', R' + str(rt)
    elif ( opcode == 32 and fnCode == 10 ): text = 'MOVZ\tR' + str(rd) + ', R' + str(rs) + ', R' + str(rt)
    elif ( opcode == 32 and fnCode == 37 ): text = 'OR\tR' + str(rd) + ', R' + str(rs) + ', R' + str(rt)
    if ( opcode == 32 and fnCode == 0 and rsInt == 0 and rtInt == 0 ): text = 'NOP'

    item = {'addr':96+i, 'binspace':asBinSpace, 'text': text , 'rs':rs, 'rt':rt}
    
    output = ( item['binspace'] + ' ' + str(item['addr']) + '\t' + item['text'] + '\n')

    # Get Values
    validBits.append(valid)
    opBits.append(opcode)
    funcBits.append(fnCode)
    rsBits.append(rsInt)
    rtBits.append(rt)
    rdBits.append(rd)
    offBits.append(offset)
    offBits18.append(offset18)
    saBits.append(shiftAmount)
    line.append(96+i)


    fileOut.write(output)

lineCounter = 96
def printFunction(opcode,fnCode,rs,rt,rd,offset,offset18,shiftAmount,line,registers):

    if(opcode == 40): 
        print('====================\n')
        print('cycle: ' + str(cycleCount) + ' ' + str(line) + '\t' + 'ADDI\tR' + str(rt) + ', R' + str(rs) + ', #' + str(offset) + '\n')
        print('registers:\n')
        print('r00:\t' + str(registers[0]) + '\t' + str(registers[1]) + '\t' + str(registers[2]) + '\t' + str(registers[3]) + '\t' + str(registers[4]) + '\t' + str(registers[5]) + '\t' + str(registers[6]) + '\t' + str(registers[7]))
        print('r08:\t' + str(registers[8]) + '\t' + str(registers[9]) + '\t' + str(registers[10]) + '\t' + str(registers[11]) + '\t' + str(registers[12]) + '\t' + str(registers[13]) + '\t' + str(registers[14]) + '\t' + str(registers[15]))
        print('r16:\t' + str(registers[16]) + '\t' + str(registers[17]) + '\t' + str(registers[18]) + '\t' + str(registers[19]) + '\t' + str(registers[20]) + '\t' + str(registers[21]) + '\t' + str(registers[22]) + '\t' + str(registers[23]))
        print('r24:\t' + str(registers[24]) + '\t' + str(registers[25]) + '\t' + str(registers[26]) + '\t' + str(registers[27]) + '\t' + str(registers[28]) + '\t' + str(registers[29]) + '\t' + str(registers[30]) + '\t' + str(registers[31]))


counter = 0
while (opBits[counter] != 32 & funcBits[counter] != 13):
    
    if ( validBits[counter] == 1 ):
        #Print instruction
        
        if (opBits[counter] == 40):
            # print(rdBits[counter])
            registers[rd] = rsBits[counter] + rtBits[counter]
            printFunction(opBits[counter],funcBits[counter],rsBits[counter],rtBits[counter],rdBits[counter],offBits[counter],offBits18[counter],saBits[counter],line[counter], registers)

    counter += 1 
            


# Print loop
# for i in range(0, len(validBits)): 
#     print (validBits[i])



    