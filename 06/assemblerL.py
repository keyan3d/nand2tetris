## An Assembler for the Hack Machine, coded in Python 2.7.10
## Presented as a solution by keyan3d to the 6th
## chapter of "The Elements of Computing Systems"
## by Nisan and Schocken, MIT Press. A great read.
##
## ============= CAN'T HANDLE SYMBOLS ============= ##



def stitchLine(string):
    """ Takes in a string and returns a space-less version of it. """
    splitStr = string.split(' ')
    outputStr = ''
    for word in splitStr:
        outputStr += word
    return outputStr

def assemble(fileName):
    """ Takes in an asm file and creates its hack counterpart next to it.
        Example (assuming the Python file next to the folders):
            assemble('add\Add.asm') """
    
    compHash = {'0':  '0101010',
                '1':  '0111111',
                '-1': '0111010',
                'D':  '0001100',
                'A':  '0110000',    'M':  '1110000',
                '!D': '0001101',
                '!A': '0110001',    '!M': '1110001',
                '-D': '0001111',
                '-A': '0110001',    '-M': '1110001',
                'D+1':'0011111',
                'A+1':'0110111',    'M+1':'1110111',
                'D-1':'0001110',
                'A-1':'0110010',    'M-1':'1110010',
                'D+A':'0000010',    'D+M':'1000010',
                'D-A':'0010011',    'D-M':'1010011',
                'A-D':'0000111',    'M-D':'1000111',
                'D&A':'0000000',    'D&M':'1000000',
                'D|A':'0010101',    'D|M':'1010101'}

    destHash = {'':   '000',
                'M':  '001',
                'D':  '010',
                'MD': '011',
                'A':  '100',
                'AM': '101',
                'AD': '110',
                'AMD':'111'}

    jumpHash = {'':   '000',
                'JGT':'001',
                'JEQ':'010',
                'JGE':'011',
                'JLT':'100',
                'JNE':'101',
                'JLE':'110',
                'JMP':'111'}

    asmFile = open(fileName)
    hackFile = open(asmFile.name[:-4] + '.hack', 'w')
    
    for line in asmFile:
        dest = ''
        comp = ''
        jump = ''
        
        ## Removing white spaces:
        stitchedLine = stitchLine(line)

        ## Removing the comments following commands:
        if '//' in stitchedLine[2:]:
            commentIndex = stitchedLine.index('//')
            stitchedLine = stitchedLine[:commentIndex] + '\n'

        ## Ignoring comments or returns:
        if stitchedLine[:2] == '//' or stitchedLine[:2] == '\n':
            continue

        elif stitchedLine[0] == '@':
            intVal = int(stitchedLine[1:])
            binVal16 = format(intVal, '016b')
            hackFile.write(binVal16 + '\n')

        elif '=' in stitchedLine and ';' in stitchedLine:
            eqIndex = stitchedLine.index('=')
            scIndex = stitchedLine.index(';')
            for ind in range(eqIndex):
                dest += stitchedLine[ind]
            for ind in range(eqIndex+1, scIndex):
                comp += stitchedLine[ind]
            for ind in range(scIndex+1, scIndex+4):
                jump += stitchedLine[ind]
            hackFile.write('111' + compHash[comp] + destHash[dest] + jumpHash[jump] + '\n')

        elif '=' in stitchedLine:
            eqIndex = stitchedLine.index('=')
            for ind in range(eqIndex):
                dest += stitchedLine[ind]
            for ind in range(eqIndex+1, len(stitchedLine)-1):
                comp += stitchedLine[ind]
            hackFile.write('111' + compHash[comp] + destHash[dest] + jumpHash[jump] + '\n')

        elif ';' in stitchedLine:
            scIndex = stitchedLine.index(';')
            for ind in range(scIndex):
                comp += stitchedLine[ind]
            for ind in range(scIndex+1, len(stitchedLine)-1):
                jump += stitchedLine[ind]
            hackFile.write('111' + compHash[comp] + destHash[dest] + jumpHash[jump] + '\n')
        else:
            raise SyntaxError("Syntax Error in line: " + line)

    asmFile.close()
    hackFile.close()
