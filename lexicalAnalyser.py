from afd import *
automato = AFD("entradas/in")


def processToken(token, afd):
    currentState = "S"
    #print("\nCurrent token: " + token)
    for i in range(len(token)):
        #print("currentState = " + currentState + " currentChar = " + token[i])
        if token[i] not in afd.symbols:
            return False
        currentState = afd.goesTo(currentState, token[i])
        if currentState == False:
            return False
        #print("nextState: " + currentState)
        #print(afd.findState(currentState).final)
        if i == len(token)-1 and afd.findState(currentState).final == True: 
            return currentState
    return False

def read_tokens_and_get_line(file_name):
    tokens_with_lines = []
    with open(file_name, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()
            if line:
                tokens = line.split()
                for token in tokens:
                    tokens_with_lines.append((token, line_number))
    # returns tuples: ('token', 1)
    return tokens_with_lines 

def printSymbolTable(symbolTable):
    for t in symbolTable:
        print("\nLINE: ",t["line"]," IDENTIFIER: "+ t["identifier"]+" LABEL: ",t["label"])

def processTokens(afd, path):
    symbolTable = []
    tape = []
    tokens = read_tokens_and_get_line(path)
    for token, line in tokens:
        label = processToken(token, afd)
        if not label:
            label = "REJECTED"
        symbolTable.append({"line": line, "identifier": token, "label": label})
        tape.append(label)
    printSymbolTable(symbolTable)
    print("\n-----------------------------------------\nOUTPUT STREAM: ", tape)
    
    
PATH = "entradas/tokens/t1.txt"

processTokens(automato, PATH)