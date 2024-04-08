from afnd import *
from afd import *
#OBS <S> deve ser sempre o estado inicial

#a = AFND("entradas/in3")
automato = AFD("entradas/in")

#a.printAttributes()
automato.printWithErrorState()
#automato.printAttributes()