from afnd import *
from time import sleep
import queue

class AFD(AFND):
    def __init__(self, path) -> None:
        self.afnd = AFND(path)
        super().__init__(path)
        self.table.clear()
        self.__makeAFD()
        self.delNonTerminal()

    def __makeAFD(self):
        afnd = self.afnd
        #fila que vai tratar os estados a serem adicionados
        #no afd, que são os estados acessíveis do estado inicial.
        q = queue.Queue()
        #adicionando estado inicial
        start = afnd.findState("S")
        q.put(start)
        while(not q.empty()):
            state=q.get()
            #estado a ser adicionado no afd
            currentNewState = STATE(state.index) 

            if(self.findState(state.index)):
                continue

            if state.final:
                currentNewState.setFinal(True)

            done = list()
            #print(state.index)
            for transac in state.nextStates:
                if len(transac)>2:
                    #dados necessários para criação do novo estado
                    #q vai ser adicionado a fila (não existe no afnd original)
                    newStateIndex=""
                    newNextStates = list()
                    final = False
                    for i in transac[1:]:
                        newStateIndex+=i+" "
                        aux = afnd.findState(i)
                        for j in aux.nextStates:
                            if j not in newNextStates:
                                newNextStates.append(j)
                        #print(newNextStates)
                        if aux.final:
                            final = True
                    newStateIndex = newStateIndex.strip()
                    currentNewState.nextStates.append([transac[0], *[newStateIndex]])
                    #done registra estados ja criados
                    if(newStateIndex not in done):
                        done.append(newStateIndex)
                        newState=STATE(newStateIndex)
                        newState.addNextStateArray(newNextStates)
                        if final:
                            newState.setFinal(True)
                        #adicionando como proximo a ser criado
                        q.put(newState)

                else:
                    aux = afnd.findState(transac[1])
                    currentNewState.nextStates.append([transac[0], transac[1]])
                    #adicionando a fila
                    q.put(aux)

            self.table.append(currentNewState)

            #debug
            #sleep(1)
            #self.printAttributes()

    #deve ser usado apenas depois da determinzação
    #retorna o primeiro proximo estado de um estado
    #ao receber um simbolo
    def goesTo(self, stateIndex, symbol):
        state = self.findState(stateIndex)
        for nextState in state.nextStates:
            if nextState[0] == symbol:
                return nextState[1]
        return False
    
    #deletes a state and all the paths leading to it
    def deleteState(self, stateIndex):
        for state in self.table:
            if state.index == stateIndex:
                self.table.remove(state)
            else:
                for nextState in state.nextStates:
                    if stateIndex in nextState:
                        nextState.remove(stateIndex)
                        if len(nextState) < 2:
                            state.nextStates.remove(nextState)

    #determina se um estado chega ao fim
    def isNonTerminal(self, start):
        visited = [] # List for visited nodes.
        queue = []     #Initialize a queue
        visited.append(start)
        queue.append(start)
        final = False
        #print("STATE", start)

        while queue:          # Creating loop to visit each node
            m = queue.pop(0) 
            #print (m, end = " ") 
            if self.findState(m).final:
                final = True
            for nextState in self.findState(m).nextStates:
                for neighbour in nextState[1:]:
                    if neighbour not in visited:
                        visited.append(neighbour)
                        queue.append(neighbour)

            #for neighbour in graph[m]:
            #    if neighbour not in visited:
            #        visited.append(neighbour)
            #        queue.append(neighbour)

        return final
    

    def delNonTerminal(self):
        #testa se os estados proximos aos iniciais são finais
        for state in self.table:
            finalizes = self.isNonTerminal(state.index)
            if finalizes:
                #print(state.index,"Is final")
                continue
            else:
                #print(state.index,"Is Not final")
                self.deleteState(state.index)




                