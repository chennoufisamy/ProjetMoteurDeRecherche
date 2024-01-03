# Classe Author

class Author:
    
    # Initialiser objet Author
    def __init__(self,nom):

        self.nom =str(nom)
        self.ndoc = 0
        self.production = []

    # Incrémenter le nombre de documents et les documents écrits par l'auteur
    def add(self, production):
        
        self.ndoc += 1
        self.production.append(production)
    
    # Affichage des informations de l'auteur
    def __str__(self):

        return "Le nom de l'auteur est " + self.nom + " Il a crée " + str(self.ndoc) + " documents " + "\n" + "leur titire est : " + str(self.production) + "\n"