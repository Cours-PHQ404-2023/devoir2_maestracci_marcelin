#-------------------------------------------------------------#
#                                                             #
# Ce document contient toutes les fonctions pour le Devoir 2: #
#                                                             #
# - hamiltonien                                               #
# - energie                                                   #
# - serie_de_gregory                                          #
# - epsilon                                                   #
#                                                             #
#-------------------------------------------------------------#


# Dépendances nécéssaires

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

#Fonction pour construire l'Hamiltonien
def hamiltonien(N, J=1):
    """
    Cette fonction calcule l'Hamiltonien H d'un système de spins N couplés avec une constante J selon le modèle de spin 
    d'Heisenberg. Elle retourne une matrice creuse H de type coo_matrix.

    Arguments:
    - N (int): le nombre de spins dans le système
    - J (float): la constante de couplage entre les spins
    
    Retourne:
    - H (coo_matrix): une matrice creuse coo_matrix représentant l'Hamiltonien du système de spins
    """

    #On initilalise H2 le hamiltonien d'ordre 2
    H2 = sp.coo_matrix([[0.25, 0, 0, 0], [0, -0.25, 0.5, 0], [0, 0.5, -0.25, 0], [0, 0, 0, 0.25]], dtype=np.float32)

    # Définition des matrices de Pauli Sx Sy Sz, en bsr pour faciliter le produit de kronecker
    Sx = sp.bsr_matrix([[0, 0.5], [0.5, 0]], dtype=np.float32, blocksize=(1, 1))
    Sy = sp.bsr_matrix([[0, -0.5j], [0.5j, 0]], dtype=np.complex64, blocksize=(1, 1))
    Sz = sp.bsr_matrix([[0.5, 0], [0, -0.5]], dtype=np.float32, blocksize=(1, 1))
    S = [Sx, Sy, Sz]  # Liste contenant les trois matrices de Pauli pour boucler les produits S@I@S

    if N == 2:
        H = H2
    if N > 2:
        #On trouve H_k a partir de H_(k-1), jusqu'a H_n
        for k in range(3, N+1):
            # Calcul de la somme pour H_(k+1): On généralise la formule donnée dans l'énoncé en calculant tous les sites de H. Toutes les combinaisons I@I@I...I@H@I@...@I sont dans ces trois lignes:

            H = sp.coo_matrix(sp.kron(H2, sp.eye(2**(k-2))))

            for j in range(1,k-2):
                H += sp.coo_matrix(sp.kron(sp.eye(2**j),sp.kron(H2, sp.eye(2**(k-j-2)))))
            
            H += sp.coo_matrix(sp.kron(sp.eye(2**(k-2)),H2))            

            # On ajoute à H la somme Sx*I*Sx + Sy*I*Sy + Sz*I*Sz
            for i in range(0, 3):
                H += sp.coo_matrix(sp.kron(S[i], sp.kron(sp.eye(2**(k-2)), S[i])),dtype=np.float32)
    #Normalement H est déja réel mais pour simplifier les +0j on cast en réel
    return J * H.real



def energie(H):
    """
    Calcul l'énergie des deux premiers états propres de l'hamiltonien H

    Arguments:
    H (sparse matrix): une matrice creuse de l'hamiltonien de Heisenberg

    Retourne:
    valeurs_propres : une liste contenant les deux premières énergies propres triées en ordre croissant

    """

    # Initialisation du nombre d'états propres à chercher
    valeurs_a_calculer = 2

    # On cherche les valeurs propres les plus petites
    valeurs_propres = spla.eigsh(H, k=valeurs_a_calculer, which='SA', return_eigenvectors=False)

    # On arrondit les valeurs propres et on les trie en ordre croissant
    valeurs_propres = sorted(valeurs_propres)

    # On retire les doublons de valp
    valeurs_propres = list(set(np.round(valeurs_propres,decimals=5)))

    # Tant que l'on a moins de deux valeurs propres, on continue à chercher
    while len(valeurs_propres) < 2:
        # On augmente le nombre d'états propres à chercher
        valeurs_a_calculer += 1

        # On cherche les valeurs propres
        valeurs_propres = spla.eigsh(H, k=valeurs_a_calculer, which='SA', return_eigenvectors=False)

        #On les trie en ordre croissant
        valeurs_propres = list(set(np.round(valeurs_propres,decimals=5)))
    
    # On retourne les deux premières valeurs propres triées en ordre croissant
    return valeurs_propres[:2]



#On peut programmer directement la série de Grégory jusqu'au terme 'termes' en paramètre

def serie_de_gregory(n):
    """
    Calcule les n premiers termes de la série de Gregory qui converge vers pi/4.

    Arguments :
    - n (int) : le nombre de termes de la série de Gregory à calculer

    Retourne :
    - Liste (list) : une liste contenant les 'n' premiers termes de la série de Gregory
    """

    Liste = [4]  # Initialisation de la liste avec le premier terme de la série

    # Boucle pour calculer les termes suivants de la série
    for i in range(1, n):
        terme_i = Liste[i-1] + ((-1)**i) * 4 / (2*i+1)  # Formule de calcul du terme i
        Liste.append(terme_i)

    return Liste


#Algorithme Epsilon en lui même

def epsilon(Serie):
    """
    Calcule la limite de la suite définie par récurrence par la méthode de Steffensen.

    Arguments :
    - S (list) : une liste contenant les termes initiaux de la suite

    Retourne :
    - epsilon (float) : la limite de la suite

    """

    #On copie Serie
    S = Serie.copy()

    # Initialisation d'une liste S_Old de même taille que Serie, mais avec des zéros
    S_Old = [0 for i in range(len(S)+1)]

    # Boucles pour réduire la liste S jusqu'à un seul élément
    for i in range(len(S)-1):

        # Boucle pour calculer les éléments récursifs de la suite
        for j in range(len(S)-1):

            # Stockage temporaire de l'élément j de S avant la mise à jour
            tmp = S[j]

            # Application de l'algorithme de Steffensen si il ne diverge pas : sinon on garde la valeur actuelle
            if S[j+1] != S[j]:
            	S[j] = S_Old[j+1] + 1 / (S[j+1] - S[j])

            # Mise à jour de la liste S_Old
            S_Old[j] = tmp

        # Suppression du dernier élément de S, qui ne sera plus utilisé
        S.pop()

    return S[0]  # Renvoi de la limite de la suite