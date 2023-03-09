from fonctions import *

#On veut voir la limite de la série de Gregory d'après l'algorithme epsilon pour n termes, allant de 1 à 6

#On peut imprimer le dixième terme de la série de Gregory pour comparer
print('Millième terme de la série de gregory : ')
print(serie_de_gregory(1000)[999])


#On utilise la fonction epsilon avec une valeur impaire de i pour avoir des résultats intéréssants. Pour imprimer
#également les lignes paires il suffit de remplacer '2*i' par 'i'

print("cinq premiers termes de l'algorithme epsilon : ")

for i in range(0,5):
	print(epsilon(serie_de_gregory(2*i+1)))

