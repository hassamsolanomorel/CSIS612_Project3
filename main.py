from terminaltables import AsciiTable
import copy

table_data = [
    ['WAR', 'WAW'],
    ['S1 -> S2: R1', 'row1 column2'],
    ['row2 column1', 'row2 column2'],
    ['row3 column1', 'row3 column2']
]
table = AsciiTable(table_data)


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
        print("Remember the instruction must be in the format:"
              "ins Reg1 Reg2 Reg3 ")
        ins = input(f"S{insNum}: ")
    return ins


def findDependencies(instructions):
    dependencies = {'waw': findWAWs(instructions),
                    'war': findWARs(instructions),
                    'trueDeps': findTrueDependencies(instructions)}
    return dependencies


def findWAWs(instructions):
    waws = {}
    insDict = {}
    i = 1

    for ins in instructions:
        insDict[f'S{i}'] = ins
        i += 1

    workingIns = copy.deepcopy(insDict)

    for (key, value) in insDict.items():
        insParts = value.split()

        del workingIns[key]

        for (key2, otherIns) in workingIns.items():
            if insParts[1] == otherIns.split()[1]:
                waws[f'{key} -> {key2}'] = insParts[1]
                break  # Find only the first occurance of a waw
    return waws


def findWARs(ins):
    wars = {}
    insDict = {}
    i = 1

    for ins in instructions:
        insDict[f'S{i}'] = ins
        i += 1

    workingIns = copy.deepcopy(insDict)

    for (key, value) in insDict.items():
        insParts = value.split()

        del workingIns[key]

        for (key2, otherIns) in workingIns.items():
            if insParts[2] == otherIns.split()[1]:
                wars[f'{key} -> {key2}'] = insParts[2]
            if insParts[3] == otherIns.split()[1]:
                wars[f'{key} -> {key2}'] = insParts[3]
    return wars


def findTrueDependencies(ins):
    trueDeps = {}
    for i in range(len(ins)-1, -1, -1):
        ins1 = ins[i].split()
        for k in range(2, len(ins1), 1):
            checkReg = ins1[k]
            for s in range(i-1, -1, -1):
                ins2 = ins[s].split()
                if checkReg == ins2[1]:
                    trueDeps[f'S{s+1} -> S{i+1}'] = checkReg
                    break
    return trueDeps


def resolveDependencies(instructions, dependencies):
    waws = dependencies['waw']
    wars = dependencies['war']
    trueDeps = dependencies['trueDeps']
    insDict = {}
    i = 1

    for ins in instructions:
        insDict[f'S{i}'] = ins
        i += 1

    tNum = 0

    # Resolve WAWs
    for (dependence, reg) in waws.items():
        depParts = dependence.split()
        insParts = insDict[depParts[0]].split()

        try:
            # Check true dependence
            trueDepsExist, trueDep = checkTrueDep(dependence, trueDeps, reg)
            if trueDepsExist:
                trueDepParts = trueDep.split()
                ins1 = insDict[trueDepParts[0]].split()
                ins2 = insDict[trueDepParts[2]].split()

                ins1ChangeIndex = ins1.index(reg)
                ins2ChangeIndex = [i for i, x in enumerate(ins2) if x == reg]

                ins1[ins1ChangeIndex] = f'T{tNum}'
                for index in ins2ChangeIndex:
                    if index != 1:
                        ins2[index] = f'T{tNum}'

                insDict[trueDepParts[0]] = ' '.join(ins1)
                insDict[trueDepParts[2]] = ' '.join(ins2)
            else:
                changeIndex = insParts.index(reg)
                insParts[changeIndex] = f'T{tNum}'

                insDict[depParts[0]] = ' '.join(insParts)
            tNum += 1
        except ValueError:
            pass

    # Resolve WARs
    for (dependence, reg) in wars.items():
        depParts = dependence.split()
        insParts = insDict[depParts[0]].split()

        try:
            changeIndex = insParts.index(reg)
            insParts[changeIndex] = f'T{tNum}'

            insDict[depParts[0]] = ' '.join(insParts)
            tNum += 1
        except ValueError:
            pass

    return insDict


def checkTrueDep(falseDep, trueDeps, reg):
    # for waws
    depArr = falseDep.split()
    for (trueDep, reg2) in trueDeps.items():
        trueDepArr = trueDep.split()
        if depArr[0] == trueDepArr[0] and reg == reg2:
            return (True, trueDep)
    return (None, None)


def parseDepDictToTableData(dependenciesDict):
    tableData = [
        ['WAW', 'WAR', 'True']
    ]
    waws = dependenciesDict['waw']
    wars = dependenciesDict['war']
    trueDeps = dependenciesDict['trueDeps']

    wawKeys = list(waws.keys())
    warKeys = list(wars.keys())
    trueDepKeys = list(trueDeps.keys())

    maxLength = max([len(waws), len(wars), len(trueDeps)])
    for i in range(0, maxLength):
        data = [f'{wawKeys[i]} -> {waws[wawKeys[i]]}'
                if i < len(wawKeys) else '',  # Add WAW Dependencies

                f'{warKeys[i]} -> {wars[warKeys[i]]}'
                if i < len(warKeys) else '',  # Add WAR Dependencies

                f'{trueDepKeys[i]} -> {trueDeps[trueDepKeys[i]]}'
                if i < len(trueDepKeys) else '']  # Add True Dependencies

        tableData.append(data)
    return tableData


if __name__ == '__main__':
    numIns = 0
    maxNumIns = 5
    stop = False
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

    # Genarate the table data need to show instructions given
    table_data = [
        ['Given Instructions'],
    ]

    i = 1
    for ins in instructions:
        table_data.append([f'S{i} - ' + ins])
        i += 1

    table = AsciiTable(table_data)
    print("Here are the instructions provided:")
    print('\n' + table.table + '\n')
    input("Press Enter find any existing false dependencies\n")
    dependenciesDict = findDependencies(instructions)
    table = AsciiTable(parseDepDictToTableData(dependenciesDict))
    print('\n' + table.table + '\n')
    input("\nPress Enter to begin renaming registers")
    resolvedInstructions = resolveDependencies(instructions, dependenciesDict)
    resolvedInstructionsArr = []
    for (key, value) in resolvedInstructions.items():
        resolvedInstructionsArr.append(f'{key} - {value}')
    resolvedTableData = [
        ['Resolved Instructions']
    ]

    for ins in resolvedInstructionsArr:
        resolvedTableData.append([ins])
        table = AsciiTable(resolvedTableData)
        print(table.table + '\n')
        input('Press Enter to continue')
    print('DONE!\n')
