from fonctions import *

#On calcule les 20 premières énergies à partir des fonctions hamiltonien et energies de fonctions.py
#On écris ces fonctions dans un fichier data.txt dans ce même dossier

#On ouvre le fichier
f = open("data.txt", "w")

#On itère de 2 à 20 inclusivement pour calculer l'énergie associée et on l'écris
for i in range(2,21):
    x = energie(hamiltonien(i,1))
    f.writelines(str(x[0]) + ' ' + str(x[1]) + "\n")

    #Comme le programme peut mettre plusieurs minutes à s'éxecuter, un indicateur de progression rudimentaire est imprimé.
    print(i,'/',20)

#On ferme le fichier
f.close()