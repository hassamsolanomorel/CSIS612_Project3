from terminaltables import AsciiTable
table_data = [
    ['WAR', 'WAW'],
    ['S1 -> S2: R1', 'row1 column2'],
    ['row2 column1', 'row2 column2'],
    ['row3 column1', 'row3 column2']
]
table = AsciiTable(table_data)

# print(table.table)

stop = False


def getDependenceStr(ins1, ins2, reg):
    return f"{ins1} -> {ins2}: {reg}"


def getInstructionStr(ins, reg1, reg2, reg3):
    return f"{ins} {reg1} {reg2} {reg3}"


def getInstructionArr(ins):
    return ins.split(' ')


def validateInput(str):
    if str.strip() == '':
        return True

    return len(str.split()) == 4


def getInstructionFromUser(insNum):
    ins = input(f"S{insNum}: ")

    while not validateInput(ins):
        print("The value instruction you entered is invalid. Please try again")
        print("Remember the instruction must be in the format:ins Reg1 Reg2 Reg3 ")
        ins = input(f"S{insNum}: ")
    return ins


if __name__ == '__main__':
    maxNumIns = 5
    numIns = 0
    instructions = []
    print("Enter up to 5 MIPs instructions below. When you're done simply"
          "press enter without typing in any input")
    print("Instructions must be in the format: ins Reg1 Reg2 Reg3")
    print("i.e. add R1 R2 R3")
    while numIns < maxNumIns and not stop:
        ins = getInstructionFromUser(numIns+1)
        if ins != '':
            instructions.append(ins)
            numIns += 1
        else:
            stop = True

    print(instructions)
