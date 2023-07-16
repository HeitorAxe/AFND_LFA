from afnd import *

class AFD(AFND):
    def __init__(self, path) -> None:
        super().__init__(path)
        self.__makeAFD()

    #determinização
    def __makeAFD(self):
        #não sei se é bom deletar agora
        #ou deixar pra deletar na minização
        #os estados determinizadoss
        #assignDel = list()
        for i in self.table:
            for j in i.nextStates:
                if len(j) > 2: #Caso o mesmo simbolo leve a mais de um estado
                    newState=""
                    newNextStates = list()
                    final = False
                    for k in range(1, len(j)):
                        newState+=j[k]+" "
                        aux = self.findState(j[k])
                        newNextStates.extend(aux.nextStates)
                        if(aux.final):
                            final = True
                        #ver isso aqui
                        #self.table.remove(aux)
                    del j[1:]
                    newState = newState.strip()
                    j.append(newState)
                    state = STATE(newState)
                    state.setFinal(True)
                    state.addNextStateArray(newNextStates)
                    self.table.append(state)
                    print("New State Created")
                    state.printStates()
