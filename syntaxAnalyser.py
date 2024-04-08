from afd import *
automato = AFD("entradas/in")

def processToken(token, afd):
    currentState = "S"
    print("\nCurrent token: " + token)
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
            return True
    return False

print(processToken("se", automato))
print(processToken("senao", automato))
print(processToken("entao", automato))
print(processToken("si", automato))
print(processToken("aeiosu", automato))
#automato.printAttributes()

