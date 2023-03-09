from fonctions import hamiltonien

#On imprime le hamiltonien de rang 3, de couplage J=4 en format sparse et numpy

print('Le hamiltonien en format sparse COO : ')
print(hamiltonien(3,4))

print('Le hamiltonien en tableau numpy : ')
print(hamiltonien(3,4).toarray())