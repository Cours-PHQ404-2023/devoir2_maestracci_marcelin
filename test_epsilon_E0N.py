from fonctions import *
import matplotlib.pyplot as plt
#On veut trouver la convergence de la série de valeurs E0/N d'après le fichier data.txt

#On initialise E0
Liste_E0 = []

#On crée une liste qui contient la première valeur de chaque colonne de data.txt, ce qui correspond à E0

for ligne in open('data.txt', 'r'):
    lignes = [i for i in ligne.split(" ")]
    Liste_E0.append(float(lignes[0]))

#On crée la liste que l'on veut tester en divisant le n ième E0 par n, 
Liste_test = []
Liste_epsilon = []
Liste_paire = []
Liste_impaire = []

for N in range(0,len(Liste_E0)): #On crée les listes pour le graphique

    Liste_test.append(Liste_E0[N]/(N+2)) #On décale N de 2 puisque l'on écrit les énergies à partir de N=2
    
    #Creation des listes paires et impaires
    if N%2 == 0:
    	if N >1:
        	Liste_paire.append(Liste_test[N]) #Enlever un nombre pour avoir un nombre paire d'élements
    else:
        Liste_impaire.append(Liste_test[N])

#On graphe les lignes horizontales qui correspondent aux limites de epsilon
plt.axhline(y=epsilon(Liste_test), linestyle='-',color='k',label='Liste Totale')
plt.axhline(y=epsilon(Liste_paire), linestyle='-',color='b',label='Liste Paire')
plt.axhline(y=epsilon(Liste_impaire), linestyle='-',color='r',label='Liste Impaire')

#On graphe les valeurs consécutives de E0/N
plt.plot([i for i in range(len(Liste_test))], Liste_test,color='k',marker='+',linestyle='dashed')
plt.plot([i for i in range(len(Liste_paire))], Liste_paire,color='b',marker='+',linestyle='dashed')
plt.plot([i for i in range(len(Liste_impaire))], Liste_impaire,color='r',marker='+',linestyle='dashed')

#On affiche le graph
plt.show()