#-------------------------------------- DECLARAÇÕES --------------------------------------------

from beautifultable import BeautifulTable

arq = open("linguagem.in", "r")
entrada = []
entrada = arq.readlines()

alfabeto = []
ignore = {'|','\\','%',' '} #lista de tokens para ignorar na gramatica - o % é o epsilon

afnd = {}

global count
count = 1                   #contador de estados criados
iniciais = []
finais = []

gramatica = []
newgram = 1

used = []



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

def tokens():                       #criação das regras para as palavras reservadas
	global count
	for a in entrada:
		if a == '':
			continue
		if(a[0] == '<' and len(a) >= 2 and a[2]== '>'):
			return
		iniciais.append(count)
		for b in range(0,len(a)+1):
			if(b == len(a)):
				for y in afnd:
					afnd[y].append('')
				finais.append(count)
				count += 1
				break
			if (a[b] in alfabeto):
				for y in afnd:
					afnd[y].append('')
				afnd[a[b]][count] = str(count+1)
				count += 1

def auxInicial():                   #colocando os estados iniciais no lugar certo
	for a in iniciais:
		if (a != 1):
			if(a in finais and 1 not in finais):
				finais.append(1)
			for y in afnd:
				if(afnd[y][1] != '' and afnd[y][a] != ''):
					aux1 = str(afnd[y][1]).split(',')
					aux2 = str(afnd[y][a]).split(',')
					res = list(set(aux1+aux2))
					ax = ''
					for g in res:
						if str(g) == str(a):
							g = 1
						if ax != '':
							ax += ',' + str(g)
						else:
							ax = str(g)
					afnd[y][1] = ax
				else:
					aux2 = str(afnd[y][a]).split(',')
					ax = ''
					for g in aux2:
						if str(g) == str(a):
							g = 1
						if ax != '':
							ax += ',' + str(g)
						else:
							ax = str(g)
					afnd[y][1] += ax
				afnd[y][a] = ''

def regras(gramatica):
	firsto = -1
	global count
	rotulo = {}
	lets = []
	f = 0
	for a in range(0,len(gramatica)):
		if(f == 0):
			f = 1
			iniciais.append(count)

		now = ''
		for b in range(0,len(gramatica[a])):
			if (gramatica[a][b] not in alfabeto) and (gramatica[a][b] not in ignore):
				now += gramatica[a][b]
			else:
				if(now != '' and now not in lets):
					lets.append(now)
				now = ''

	for a in range(0,len(lets)):
		if firsto == -1:
			firsto = count
		rotulo[lets[a]] = count
		count += 1
		for y in afnd:
			afnd[y].append('')

	for a in range(0,len(gramatica)):
		print(lets)
		ent = gramatica[a].split('::=')[1]
		line = rotulo[gramatica[a].split('::=')[0].replace('<','').replace('>','').replace(' ','')]
		a = spliterson(ent)
		for b in a:
			if(b[0] == '%'):
				finais.append(line)
				continue
			spl = b.replace(' ','').split('<')
			terminal = spl[0]
			if terminal == '':
				terminal = '%'
			if len(spl) == 1 and spl[0][0] != '<':
				for y in afnd:
					afnd[y].append('')
				if(afnd[terminal][line] != '' and set(str(afnd[terminal][line]).split(',')) != set(str(count).split(','))):
					prim = str(afnd[terminal][line]).split(',')
					sec = str(str(count)).split(',')
					res = list(set(prim+sec))
					ax = ''
					for g in res:
						if ax != '':
							ax += ',' + str(g)
						else:
							ax = str(g)
					afnd[terminal][line] = ax
				else:
					afnd[terminal][line] = count
				finais.append(count)
				count += 1
			else:
				naoterminal = b.split('<')[1]
				naoterminal = naoterminal.replace('>','')
				if(afnd[terminal][line] != '' and set(str(afnd[terminal][line]).split(',')) != set(str(rotulo[naoterminal]).split(','))): 
					prim = str(rotulo[naoterminal]).split(',')
					sec = str(str(afnd[terminal][line])).split(',')
					res = list(set(prim+sec))
					ax = ''
					for g in res:
						if ax != '':
							ax += ',' + str(g)
						else:
							ax = str(g)
					afnd[terminal][line] = ax
				else:
					afnd[terminal][line] = str(rotulo[naoterminal])
	if firsto != -1: 
		eliminaET(firsto)                         #eliminacao de epsilon transicao

def spliterson(ent):
	ent = ent.replace(' ','')
	aux = ent.split('|')
	return aux

def eliminaET(firsto):
	temer = []
	temet = []
	for x in range(firsto,count):
		if(afnd['%'][x] != ''):
			aux = str(afnd['%'][x]).split(',')
			aux1 = []
			aux1.append(x)
			aux1.append(aux)
			temer.append(aux1)
			temet.append(x)

	alter = 1
	while(alter == 1):
		alter = 0
		for a in temer:
			b = a[1]
			for c in b:
				if(int(c) in temet):
					i = 0
					for x in temer:
						if x[0] == int(c):
							break
						i += 1
					aux = temer[i][1]
					s = set(aux+a[1])
					s = list(s)
					if s != a[1]:
						alter = 1
					a[1] = s

	for y in afnd:
		for x in range(firsto, count):
			a = str(afnd[y][x]).split(',')
			for b in a:
				for c in temer:
					if(str(b) == str(c[0])):
						res = set(a+c[1])
						res = list(res)
						ax = ''
						for r in res:
							if(ax != ''):
								ax += ',' + r
							else:
								ax = r
						afnd[y][x] = ax

	for a in range(0,count):
		afnd['%'][a] = ''

	for a in temer:
		for b in a[1]:
			for y in afnd:
				x = str(afnd[y][a[0]]).split(',')
				z = str(afnd[y][int(b)]).split(',')
				res = set(x+z)
				res = list(res)
				ax = ''
				for r in res:
					if(ax != ''):
						if(r != ''):
							ax += ',' + r
					else:
						ax = r
				afnd[y][a[0]] = ax

	for a in temer:
		sim = 0
		for b in a[1]:
			if(int(b) in finais):
				sim = 1
		if(sim == 1):
			if(a[0] not in finais):
				finais.append(a[0])

def determiniza():
	global count
	i = 0
	while(i < count):
		for y in afnd:
			if isinstance(afnd[y][i], str) and len(afnd[y][i]) > 2: #indeterminismo
				b = afnd[y][i].split(',')
				p = 1
				for k in used:
					if (set(b) == set(k[0])):
						afnd[y][i] = k[1]
						p = 0
						break
				if p == 0:
					continue
				for z in afnd:
					afnd[z].append('')
				for z in b:
					if int(z) in finais:
						finais.append(count)
						break
				lc = count
				c = []
				c.append(b)
				c.append(count)
				count += 1
				used.append(c)
				for x in b:
					for l in afnd:
						if(afnd[l][count-1] != ''):
							if(afnd[l][int(x)] != '' and set(str(afnd[l][count-1]).split(',')) != set(str(afnd[l][int(x)]).split(','))): 
								prim = str(afnd[l][count-1]).split(',')
								sec = str(str(afnd[l][int(x)])).split(',')
								res = list(set(prim+sec))
								ax = ''
								for g in res:
									if ax != '':
										ax += ',' + str(g)
									else:
										ax = str(g)
								afnd[l][count-1] = ax
						else:
							afnd[l][count-1] = afnd[l][int(x)]
				afnd[y][i] = lc
		i += 1

def erro():
	for y in afnd:
		for x in range(count):
			if(afnd[y][x] == ''):
				afnd[y][x] = str(0)

def minimiza():
	global finais
	alc = []
	vivos = []
	alc.append(1)
	for y in afnd:
		if(int(afnd[y][1]) not in alc):
			alc.append(int(afnd[y][1]))
	for x in alc:
		for y in afnd:
			if(int(afnd[y][x]) not in alc):
				alc.append(int(afnd[y][x]))
	for x in range(count):
		if x in finais and x in alc:
			vivos.append(x)
	aux = 1
	while(aux):
		aux = 0
		for x in range(count):
			if x in vivos or x not in alc:
				continue
			for y in afnd:
				if(int(afnd[y][x]) in vivos):
					vivos.append(x)
					aux = 1
					break
	for y in afnd:
		for a in range(count):
			if(int(afnd[y][a]) not in alc or int(afnd[y][a]) not in vivos):
				afnd[y][a] = str(0)

	fica = list(set(vivos+alc))
	fica = sorted(fica)
	np = []
	rm = count-len(fica)
	for a in fica:
		if(a != 0):
			aux = []
			aux.append(a)
			aux.append(a - (fica[fica.index(a)] - fica[fica.index(a)-1] - 1))
			np.append(aux)
			fica[fica.index(a)] = a - (fica[fica.index(a)] - fica[fica.index(a)-1] - 1)

	for i in np:
		for y in afnd:
			afnd[y][i[1]] = afnd[y][i[0]]

	for y in afnd:
		afnd[y] = afnd[y][:-rm]

	for y in afnd:
		for a in range(1,count-rm):
			for i in np:
				if int(afnd[y][a]) == i[0]:
					afnd[y][a] = i[1]
	fn = []
	for a in finais:
		for i in np:
			if a == i[0]:
				fn.append(i[1])

	finais = fn

#------------------------------------------------ MAIN -------------------------------------------------

for a in range(0,len(entrada)):     #remoção do \n no final da string
	entrada[a] = entrada[a][0:len(entrada[a])-1]

for a in range(0,len(entrada)):     #criação do alfabeto
	for b in range(0,len(entrada[a])):
		if (entrada[a][b] not in alfabeto) and (entrada[a][b] not in ignore) and (not nterminal(entrada[a],b)):
			alfabeto.append(entrada[a][b])

print("ALFABETO em forma de lista")
print(alfabeto)

alfabeto.append('%')               #epsilon transição

for a in range(0,len(alfabeto)):   #criação do dicionario do alfabeto
	afnd[alfabeto[a]] = []

print("Alfabeto")
print(afnd)

for y in afnd:                     #estado final
	afnd[y].append(0)

tokens()                           #palavras resevadas
print(iniciais)
print(finais)
print(count)
auxInicial()

for a in range(0,len(entrada)):    #pegar gramaticas
	if(newgram == 1):
		if(len(gramatica) != 0):
			regras(gramatica)
			auxInicial()
		gramatica = []
		newgram = 0
	if(entrada[a] == '' or (entrada[a][0] != '<') or entrada[a] == '<'):
		newgram = 1
		continue
	gramatica.append(entrada[a])
if(len(gramatica) != 0):
	regras(gramatica)
	auxInicial()

determiniza()                      #determiniza
erro()
minimiza()
finais.append(0)

a = []
a.append('Regra')                  #tabela
for y in afnd:
	a.append(y)

table = BeautifulTable()
table.column_headers = a
for b in range(0,len(afnd[y[0]])):
	a = []
	if(b in finais):
		a.append(str(b)+'*')
	else:
		a.append(b)
	for y in afnd:
		a.append(afnd[y][b])
	table.append_row(a)
print(table)

arq.close()

saida = open("saidaAFD","w")

for y in afnd:
	lenstd = len(afnd[y])
	break

saida.write( str(lenstd)+'\n')
simbolos = ""
for y in afnd:
	simbolos += str(y) + ' '

simbolos = simbolos[:-1]
simbolos += '\n'

saida.write(simbolos)

for a in range(0,lenstd):
	estados = ""
	for y in afnd:
		estados += str(afnd[y][a]) + ' '
	estados = estados[:-1]
	estados += '\n'
	saida.write(estados)

fin = ""

for a in finais:
	fin += str(a) + ' '

saida.write(fin)

saida.close()

#---------------------------------- LEXICO ------------------------------------------

arq = open('saidaAFD', 'r')
AFD = arq.readlines()
alfabeto = []

afd = {}
entrada = open('exemploGramatica.txt', 'r')
code = []
code = entrada.readlines()

separadores = ['<', '>', '=', ',', '.', '|', '~', '+', '-', '*', '/', '!', ' ', '\n', ':', ';', '(', ')']

TS = open('TabelaDeSaida', 'w')

estados = int(AFD[0])
aux = AFD[1].split()
finais = AFD[estados+2].split()

#criação do alfabeto
for a in range(0,len(aux)):
	alfabeto.append(aux[a])

#criação do afnd (dicionario)
for a in range(0,len(alfabeto)):
	afd[alfabeto[a]] = []

for i in range(2, estados+2):
    slice = AFD[i].split()
    for j in range(0, len(alfabeto)):
        afd[alfabeto[j]].append(slice[j])

line = 1
for i in range(0, len(code)):
    words = []
    ini = 0
    fim = 0
    for j in range(0, len(code[i])):
        if code[i][j] not in alfabeto and code[i][j] not in separadores:
            print("Caracter não permitido pela gramatica da linguagem: '"+ code[i][j]+"'")
            exit()
        if(code[i][j] not in separadores):
            fim += 1
        else:
            words.append(code[i][ini:fim])
            if(code[i][j] != ' ' and code[i][j] != '\n'):
                words.append(code[i][fim])
            ini = fim = fim+1
    while '' in words:
        words.remove('')

    for word in words:
        est_atual = 1
        for a in range(0, len(word)):
            est_atual = int(afd[word[a]][est_atual])
        if est_atual == 0:
            print("Palavra não permitida pela linguagem!: '"+word+"'")
            exit()
        else:
            print(word+'$'+str(est_atual)+'$'+str(line))
            TS.write(word+'$'+str(est_atual)+'$'+str(line)+'\n')

    line += 1