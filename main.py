from beautifultable import BeautifulTable

arq = open("linguagem", "r")
entrada = []
entrada = arq.readlines()

#remoção do \n no final da string
for a in range(0,len(entrada)):
	entrada[a] = entrada[a][0:len(entrada[a])-1]