from afd import *
from SymbolTable import *

automato = AFD("entradas/in")

class Lexer:
    def __init__(self, afd):
        #self.tape = self.processTokens(afd, path)
        self.afd = afd

    def processTokens(self, path):
        symbolTable = SymbolTable()
        tape = []
        tokens = self.read_tokens_and_get_line(path)
        #print(afd.tokens)
        for token, line in tokens:
            label = self.processToken(token, self.afd)
            if not label:
                label = "REJECTED"
            elif token in self.afd.tokens:
                label = token

            symbolTable.add_symbol({"line": line, "identifier": token, "label": label})
            tape.append(label)
        symbolTable.add_symbol({"line": line, "identifier": '$', "label": '$'})
        #printSymbolTable(symbolTable.table)
        #print("\n-----------------------------------------\nOUTPUT STREAM: ")
        #print(symbolTable.table)
        return symbolTable.table

    def processToken(self, token, afd):
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

    def read_tokens_and_get_line(self, file_name):
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

    def printSymbolTable(self, symbolTable):
        #print(symbolTable)
        for t in symbolTable:
            print("\nLINE: ",t["line"]," IDENTIFIER: ", t["identifier"]," LABEL: ",t["label"])


    
    
""" PATH = "entradas/tokens/t1.txt"
symbolTable = SymbolTable();
processTokens(automato, PATH, symbolTable) """