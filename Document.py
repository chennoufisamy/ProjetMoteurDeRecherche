# Classe Document

class Document:

    # Initialiser objet Document
    def __init__(self,titre,auteur,date,url,texte,type):

        self.titre =str(titre)
        self.auteur = str(auteur)
        self.date = str(date)
        self.url = str(url)
        self.texte = str(texte)
        self.type = str(type)
    
    # Afficher les informations d'un objet Document
    def afficher(self):

        print ("Le titre du document est " + self.titre + "\n" +
               "L'auteur du document est " + self.auteur + "\n" +
               "La date de publication du document est " + self.date + "\n" +
               "L'url du document est " + self.url + "\n" +
               "Le contenu du document est " + self.texte)

    # Recuperer le type du document 
    def getType(self):
        
        pass
    
    # Affichage du document
    def __str__(self):

        return "Le document est " + self.titre + " Son auteur est: " + self.auteur + " Sa publication est " + self.date  
    
# Classe RedditDocument qui hérite de la classe Document
class RedditDocument(Document):
    
    # Initialiser objet RedditDocument
    def __init__(self, titre,auteur,date,url,texte,type, ncom):
            
            super().__init__(titre,auteur,date,url,texte,type)
            self.ncom = ncom
    
    # Recuperer le type du document
    def getType(self):
        
        return "Reddit"
    
    # Recuperer le nombre de commentaires
    def get_ncom(self):

        return self.ncom

    # Définir le nombre de commentaires
    def set_ncom(self, ncom):

        self.ncom = ncom

    # Affichage du document
    def __str__(self):

        return super().__str__() + " Le nombre de commentaires est: " + str(self.ncom)

# Classe ArxivDocument qui hérite de la classe Document   
class ArxivDocument(Document):

    # Initialiser objet ArxivDocument
    def __init__(self, titre,auteur,date,url,texte,type, coauteurs):

        super().__init__(titre,auteur,date,url,texte,type)
        self.coauteurs = coauteurs
    
    # Recuperer le type du document
    def getType(self):

        return "Arxiv"
    
    # Recuperer les co-auteurs du document
    def get_coauteurs(self):

        return self.coauteurs
    
    # Denifinr les co-auteurs du document
    def set_coauteurs(self, coauteurs):

        self.coauteurs = coauteurs

    # Affichage du document
    def __str__(self):

        return super().__str__() + " Le nom des co-auteurs est: " + self.coauteurs
    
