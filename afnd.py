import re
import itertools
import tabulate
#parece q ta tudo em ordem
#afnd funcionando

class STATE:
    id_iter = itertools.count()
    def __init__(self, index) -> None:
        self.index = index
        #não sei se vai ser necessário
        self.id = next(self.id_iter)
        self.nextStates = list()
        self.final = False
    def addNextState(self, symbol, nextState):
        for i in range(len(self.nextStates)):
            if self.nextStates[i][0] == symbol:
                self.nextStates[i].append(nextState)
                #wont be using this
                return
        #wont be using this either

        self.nextStates.append([symbol, nextState])

    def addNextStateArray(self, arr):
        for i in arr:
            for j in range(1, len(i)):
                self.addNextState(i[0], i[j])

    def setFinal(self, bool):
        self.final = bool

    def printStates(self):
        for i in self.nextStates:
            print(i)

class AFND:
    #path to file
    def __init__(self, path) -> None:
        self.tokens = list()
        self.gr = list()
        self.symbols = list()
        self.states = list()
        #list of States
        self.table = list()
        self.__getDataFromFile(path)

    def __getDataFromFile(self, path):
        f = open(path, "r")
        for x in f:
            #print(x)
            #in case it is a rule from gr
            if x[0] == "<":
                self.gr.append(x)
                #trimming rule from gr
                x=x.replace(" ", "")
                x=x.replace("::=", "|")#Atenção! isso aqui vai servir só pra n ter q lidar com esse simbolo
                #turning into list of states
                rules=re.split('\|', x)
                
                #For tracking states and next states
                matches = re.findall(r'<(.*?)>', x);
                newState = STATE(matches[0])
                #resulta em erro se der append agora e dps modificar o objeto?
                self.table.append(newState)
                #get states and symbols from the rule
                for r in rules:
                    #lembrar que com exceto pelo primeiro elemento de rules, o primeiro é um simbolo antes do "<"
                    state = r.replace("\n", "")[r.find("<")+1:r.find(">")]
                    symbol = r.split("<")[0].strip()
                    if state and state not in self.states:
                        #print("ADDING "+state+" to states")
                        self.states.append(state)
                    if symbol and symbol not in self.symbols and symbol != "ε":
                        self.symbols.append(symbol)

                    #adding nextState to state object
                    if symbol:
                        if symbol == "ε":
                            newState.setFinal(True)
                        else:
                            if state:
                                newState.addNextState(symbol, state)
                            else:
                                #in this case we need to create an ending state for the symbol
                                newFinalStateIndex = int(repr(STATE.id_iter)[6:-1])
                                #parsing as string cuz i think there would be some problems if i dont
                                #relating to printing and stuff
                                newFinalState = STATE(str(newFinalStateIndex))
                                newFinalState.setFinal(True)
                                self.table.append(newFinalState)
                                newState.addNextState(symbol, str(newFinalStateIndex))

                
            #ADICIONANDO AS REGRAS DE ACORDO COM OS TOKENS
            #Pressupõe que os estados da GR já foram cirados 
            #Mas se n tiver GR no input funciona de boas
            else:
                self.tokens.append(x)
                for i in range(len(x)-1):
                    nextStateIndex = repr(STATE.id_iter)[6:-1]
                    if x[i] not in self.symbols:
                        self.symbols.append(x[i])

                    for j in range(len(self.table)):
                        if i == 0 and len(self.table)!=0:
                            if self.table[j].index == "S" or self.table[j].id == 0:
                                self.table[j].addNextState(x[i], nextStateIndex)
                        else:
                            if self.table[j].id == int(nextStateIndex)-1:
                                self.table[j].addNextState(x[i], nextStateIndex)
                                self.table[j].setFinal(False)
                        
                    nextState = STATE(nextStateIndex)
                    nextState.setFinal(True)
                    self.table.append(nextState)
        f.close()

    def printAttributes(self):
            print("TABLE")
            table = list()
            table.append(["State", *self.symbols])
            for i in range(len(self.table)):
                aux = list()
                if self.table[i].final:
                    aux.append("*"+self.table[i].index)
                else:
                    aux.append(self.table[i].index)

                for j in range(len(self.symbols)):
                    found = False
                    for k in self.table[i].nextStates:
                        if k[0] == self.symbols[j]:
                            aux.append(k[1:])
                            found = True
                    if not found:
                        aux.append("")
                table.append(aux)
        
            print(tabulate.tabulate(table, headers="firstrow", tablefmt="heavy_grid"))
            """ for i in self.table:
                print(i.index+": ", i.nextStates) """

    def findState(self, index):
        for i in self.table:
            if i.index == index:
                return i
        return False
    
    
    def printWithErrorState(self):
            table = list()
            table.append(["State", *self.symbols])
            temp = ["-1" for i in range(len(self.symbols))]
            temp.insert(0, "-1")
            table.append(temp)
            for i in range(len(self.table)):
                aux = list()
                if self.table[i].final:
                    aux.append("*"+self.table[i].index)
                else:
                    aux.append(self.table[i].index)

                for j in range(len(self.symbols)):
                    found = False
                    for k in self.table[i].nextStates:
                        if k[0] == self.symbols[j]:
                            aux.append(k[1:])
                            found = True
                    if not found:
                        aux.append("-1")
                table.append(aux)
        
            print(tabulate.tabulate(table, headers="firstrow", tablefmt="heavy_grid"))