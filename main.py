#-------------------------------------- DECLARAÇÕES --------------------------------------------

from beautifultable import BeautifulTable

arq = open("linguagem.in", "r")
entrada = []
entrada = arq.readlines()

alfabeto = []
ignore = {'|','\\','%',' '} #lista de tokens para ignorar na gramatica


#-------------------------------------- FUNÇÕES ------------------------------------------------

def nterminal(a,i):         #função que verifica se o token é um terminal ou um não-terminal
	p = 0
	for b in range(i,-1,-1):
		if(a[b] == '<'):
			p = 1
			break
		if(a[b] == '>'):
			break

	if(p == 0):
		return False

	p = 0
	for b in range(i,len(a)):
		if(a[b] == '>'):
			p = 1
		if(a[b] == '<'):
			break

	if(p == 0):
		return False

	return True

#------------------------------------------------ MAIN -------------------------------------------------

#remoção do \n no final da string
for a in range(0,len(entrada)):
	entrada[a] = entrada[a][0:len(entrada[a])-1]

#criação do alfabeto
for a in range(0,len(entrada)):
	for b in range(0,len(entrada[a])):
		if (entrada[a][b] not in alfabeto) and (entrada[a][b] not in ignore) and (not nterminal(entrada[a],b)):
			alfabeto.append(entrada[a][b])

print("ALFABETO")
print(alfabeto)