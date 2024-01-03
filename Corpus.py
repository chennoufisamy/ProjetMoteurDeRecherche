import io
import pandas as pd
import pickle
import re
import numpy as np
from datetime import datetime
from Author import Author
from Document import Document,RedditDocument,ArxivDocument
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Le singleton :

# def singleton(cls):
#     instance = [None]
#     def wrapper(*args, **kwargs):
#         if instance[0] is None:
#             instance[0] = cls(*args, **kwargs)
#         return instance[0]
#     return wrapper
# @singleton


# Classe corpus

class Corpus:

    # Initialiser objet Corpus

    def __init__(self, nom):

        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
    
    # Factory
    @staticmethod
    def factory(type,doc):

        if type == 'reddit':
            return RedditDocument(doc['Titre'],doc['Auteur'],doc['Date'],doc['URL'],doc['Texte'],doc['Origine'],doc['NCommentaires'])
        
        if type == 'arxiv':
            return ArxivDocument(doc['Titre'],doc['Auteur'],doc['Date'],doc['URL'],doc['Texte'],doc['Origine'],doc['Auteur'])
         
    # Ajouter dans le corpus (auteurs et documents)
    def add(self, doc):
        
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = Author(doc.auteur)
            self.aut2id[doc.auteur] = self.naut

        self.authors[self.aut2id[doc.auteur]].add(doc.texte)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        
    # Afficher les titres des documents tries par la date de publication
    def tri_date(self):

        sorted_docs = sorted(self.id2doc.values(), key=lambda x: (x.date))
        for doc in sorted_docs:
            print(doc.date + " : " + doc.titre)

    # Afficher les titres documents tries par le nom de l'auteur
    def tri_nom(self):

        sorted_docs = sorted(self.id2doc.values(), key=lambda x: (x.titre))
        for doc in sorted_docs:
            print(doc.titre)
    
    # Sauvegarde du corpus dans un fichier        
    def save(self,filename):

        with open(filename, "wb") as f:
            pickle.dump(self, f)

    # Charger un corpus à partir d'un fichier CSV
    def load(self, filename):

        with open(filename, "rb") as f:
            donnees = pickle.load(f)
        return donnees

    # Affichage des informations du corpus
    def __repr__(self):

        return "Corpus: " + self.nom + " Nombre de documents: " + str(self.ndoc) + " Nombre d'auteurs: " + str(self.naut)  