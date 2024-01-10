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
from rank_bm25 import BM25Okapi
from collections import defaultdict
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk

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
            self = pickle.load(f)

    # Affichage des informations du corpus
    def __repr__(self):

        return "Corpus: " + self.nom + " Nombre de documents: " + str(self.ndoc) + " Nombre d'auteurs: " + str(self.naut)  
    
    # Recherche une clef dans le fichier
    def search(self,clef):

        trouver = []
        for _, reddit_doc in self.id2doc.items():
            contenu = reddit_doc.texte
            trouver.append(re.findall(clef,contenu,flags=re.IGNORECASE))
        return trouver 
    
    # Creation de la concorde
    def concorde(self,clef,taille=20):

        #Creation d'un tableau afin de stocker le contexte gauche le motif et le contexte droit a chaque fois que le motif apparait
        results = []

        #longeur du dataframe à retourner à ne pas dépasser
        longeur_df = 0
        
        #On boucle sur le dictionnaire id2doc et on récupére le contenu du texte des documents
        for _, reddit_doc in self.id2doc.items():

            contenu = reddit_doc.texte
            
            #On cherche si le motif existe dans le document qui on est en train de traiter
            trouver = str(re.search(clef,contenu,flags=re.IGNORECASE))
            
            #Si le motif existe et que la longueur du dataframe est inférieur à la taille
            if (trouver != 'None') and (longeur_df < taille) :

                #On recupere la positoin du motif dans le texte
                position = reddit_doc.texte.find(clef)
                
                #On extrait dans contexte_g : le début du texte jusqu'à le motif
                contexte_g = reddit_doc.texte[:position]
                
                #On extrait dans contexte_d : du motif jusqu'à la fin du texte
                contexte_d = reddit_doc.texte[position+ len(clef):]
                
                #On ajoute dans results un dictionnaire contenant les champs contexte_gauche, motif_trouve et contexte_droit
                results.append({'contexte_gauche' : contexte_g, 'motif_trouve' : clef, 'contexte_droit' : contexte_d})
                
                #Incrémentation longeur dataframe
                longeur_df += 1
                
        #On return le dataframe crée à partir de la liste results
        return pd.DataFrame(results)
    
    # Nettoyage du contenu des documents 

    def nettoyer_texte(self):

        contenu = ''
        for _, doc in self.id2doc.items():
            contenu = contenu + doc.texte

        contenu = contenu.replace('\n',' ')
        contenu = re.sub(r'[^a-zA-Z\s]', '', contenu)
        contenu = contenu.lower()
        return contenu
    
    # Creation d'un vocabulaire

    def creation_vocabulaire(self,texte):

        vocabulaire = set()
        mots = re.split(r'\s+', texte)

        for mot in mots:
            vocabulaire.add(mot)
            
        return vocabulaire
    
    # Savoir le nombre d'occurences de chaque mot dans le vocabulaire
    def occurences(self, texte):

        occurence = {}
        freq_doc = {}
        mots = texte.split()
        mots = sorted(set(mots))

        for mot in mots:
            if mot in occurence:
                occurence[mot] += 1
            else:
                occurence[mot] = 1
            if mot not in freq_doc:
                freq_doc[mot] = 1
                
        for _, doc in self.id2doc.items():
            for mot in occurence.keys():
                if mot in doc.texte:
                    freq_doc[mot] += 1

        occurence_liste = [
            {
                'mots': mot,
                'nb_occurence_mot': occurence[mot],
                'freq_doc': freq_doc[mot]
            } for mot in occurence
        ]

        return occurence_liste
    
    # Convertir les documents en une liste
    def docs_in_list(self):

        documents_list = []

        for _, reddit_doc in self.id2doc.items():
            contenu = reddit_doc.texte
            if contenu != 'nan' :
                contenu = contenu.replace('\n',' ')
                contenu = re.sub(r'[^a-zA-Z\s]', '', contenu)
                contenu = contenu.lower()
                documents_list.append(contenu)

        return documents_list 
    
    # Savoir le nombre de mots dans le vocabulaire
    def stats(self):

        freq = []
        texte_nettoye = self.nettoyer_texte()
        vocabulaire = self.creation_vocabulaire(texte_nettoye)
        print('Le nombre de mots different dans le texte est ' + str(len(vocabulaire)))
        freq = self.occurences(texte_nettoye)
        return pd.DataFrame(freq)
    
    # Construction d'un vocabulaire avec un id unique pour chaque mot et le nombre d'occurences du mot
    def construire_vocabulaire(self):

        texte_nettoye = self.nettoyer_texte()
        mots = texte_nettoye.split()
        mots = sorted(set(mots))
        vocabulaire = {}
        identifiant = 1

        for mot in mots:
            nb_occurences = mots.count(mot)
            info_mot = {
            'identifiant_unique': identifiant,
            'nb_occurrences': nb_occurences,
        }

            vocabulaire[mot] = info_mot
            identifiant += 1
        
        return vocabulaire

    # Le moteur de recherche
    def moteur_de_recherche(self,recherche):
        
        # Convertir les documents en une liste
        docs_list = self.docs_in_list()

        # Creation d'un objet TfidfVectorizer en passant le stop_words (mots vides) en langue anglaise 
        tfv = TfidfVectorizer(stop_words='english')

        # Applique le TF-IDF sur les documents
        matrice = tfv.fit_transform(docs_list)
        
        # Transformation de la recherche en vecteur
        recherche_vectorized = tfv.transform([recherche])
        
        # Calcul de la similarité cosinus
        similarite = cosine_similarity(matrice, recherche_vectorized).flatten()
        
        # Recuperer des documents similaires
        similarite_index = np.argsort(similarite)
        similarite_index = np.flip(similarite_index)
        
        # Affichage des documents similaires
        for _,index in enumerate(similarite_index):
            if similarite[index] > 0 :
                document = self.id2doc[index+1].texte 
                print(document)
        
        # Trier les documents par ordre de similarité
        similarite = sorted(similarite,reverse=True)

        return similarite 

    # Analyse comparative sans sortie CSV
    def comparer_reddit_arxiv(self):
        # Filtrer les documents Reddit et Arxiv
        docs_reddit = [doc for _, doc in self.id2doc.items() if isinstance(doc, RedditDocument)]
        docs_arxiv = [doc for _, doc in self.id2doc.items() if isinstance(doc, ArxivDocument)]

        # Extraire les textes des documents Reddit et Arxiv
        textes_reddit = [doc.texte for doc in docs_reddit]
        textes_arxiv = [doc.texte for doc in docs_arxiv]

        # Vectorisation TF-IDF
        vectoriseur_tfidf = TfidfVectorizer(stop_words='english')
        matrice_tfidf_reddit = vectoriseur_tfidf.fit_transform(textes_reddit)
        matrice_tfidf_arxiv = vectoriseur_tfidf.transform(textes_arxiv)

        # BM25 Okapi
        bm25_reddit = BM25Okapi([texte.split() for texte in textes_reddit])
        matrice_bm25_arxiv = np.array([bm25_reddit.get_scores(requete.split()) for requete in textes_arxiv])

        # Liste pour stocker les données du DataFrame
        donnees_df = []

        # Remplir donnees_df avec les données de comparaison
        for i, doc_reddit in enumerate(docs_reddit):
            for j, doc_arxiv in enumerate(docs_arxiv):
                similarite_tfidf = cosine_similarity(matrice_tfidf_reddit[i].reshape(1, -1), matrice_tfidf_arxiv[j].reshape(1, -1))[0, 0]
                similarite_bm25 = matrice_bm25_arxiv[j, i]

                donnees_df.append({
                    'Document Reddit': doc_reddit.titre,
                    'Document Arxiv': doc_arxiv.titre,
                    'TF-IDF Reddit': matrice_tfidf_reddit[i].toarray(),
                    'TF-IDF Arxiv': matrice_tfidf_arxiv[j].toarray(),
                    'Similarité BM25 Okapi': similarite_bm25,
                    'Similarité Cosinus': similarite_tfidf
                })

        # Créer un DataFrame à partir de donnees_df
        df = pd.DataFrame(donnees_df)
        df.sort_values(by='Similarité Cosinus', ascending=False, inplace=True)
        df = df[df['Similarité Cosinus'] != 0]
        df.reset_index(drop=True, inplace=True)
        print(df)

        return df
    
    #Vérifie si des dates valides sont présentes dans les documents avec le format spécifié.
    # def has_valid_dates(self, date_format='%Y-%m-%d'):
    #     for _, doc in self.id2doc.items():
    #         if isinstance(doc, Document):
    #             try:
    #                 datetime.strptime(doc.date, date_format)
    #                 return True  
    #             except ValueError:
    #                 continue  
    #     return False  


    # # Récupère les documents avec des dates dans les formats spécifiés.
    # def get_documents_with_dates(self, date_formats=['%Y-%m-%d']):
    #     documents_with_dates = []

    #     for _, doc in self.id2doc.items():
    #         if isinstance(doc, Document):
    #             for date_format in date_formats:
    #                 try:
    #                     datetime_object = datetime.strptime(doc.date, date_format)
    #                     documents_with_dates.append((doc, datetime_object))
    #                     break  
    #                 except ValueError:
    #                     continue 

    #     documents_with_dates.sort(key=lambda x: x[1], reverse=True)

    #     return documents_with_dates

    # Evolution temporelle d'un mot (ou d'un groupe de mots) par année
    def observer_evolution_temporelle(self, mots):
        # Créer un dictionnaire pour stocker les fréquences de mots par année
        freq_mot_par_annee = defaultdict(int)

        # Identifier automatiquement le format de date en vérifiant le premier document avec une date valide
        format_date = None
        for _, doc in self.id2doc.items():
            if isinstance(doc, Document):
                try:
                    datetime.strptime(doc.date, '%Y-%m-%d')  # Essayer le format par défaut
                    format_date = '%Y-%m-%d'
                    break
                except ValueError:
                    continue

        # Si le format par défaut ne fonctionne pas, essayer d'identifier un format différent
        if format_date is None:
            for _, doc in self.id2doc.items():
                if isinstance(doc, Document):
                    try:
                        datetime.strptime(doc.date, '%Y/%m/%d')  # Ajuster le format si nécessaire
                        format_date = '%Y/%m/%d'
                        break
                    except ValueError:
                        continue

        # Si aucun format de date valide n'est identifié, afficher un avertissement
        if format_date is None:
            print("Avertissement : Impossible d'identifier automatiquement le format de date. Utilisation du format par défaut '%Y-%m-%d'.")

        # Itérer à travers les documents et extraire la date et l'information de fréquence de mots
        for _, doc in self.id2doc.items():
            if isinstance(doc, Document):
                try:
                    date_objet = datetime.strptime(doc.date, format_date)
                    annee = date_objet.year
                except ValueError:
                    
                    continue

                for mot in mots:
                    freq_mot = doc.texte.lower().count(mot.lower())  # Compter les occurrences du mot, insensible à la casse
                    freq_mot_par_annee[(mot, annee)] += freq_mot

        # Tracé de l'évolution temporelle pour chaque mot
        plt.figure(figsize=(12, 6))
        for mot in mots:
            freq_mot_par_mot = {cle[1]: valeur for cle, valeur in freq_mot_par_annee.items() if cle[0] == mot}
            annees, frequences = zip(*sorted(freq_mot_par_mot.items()))

            plt.plot(annees, frequences, marker='o', linestyle='-', label=mot)

        plt.title('Évolution Temporelle des Mots')
        plt.xlabel('Année')
        plt.ylabel('Fréquence du Mot')
        plt.legend()
        plt.show()

    def analyse_vocabulaire(self, reddit_doc_name, arxiv_doc_name):
        # Get Reddit and Arxiv documents by name
        reddit_doc = next((doc for _, doc in self.id2doc.items() if isinstance(doc, RedditDocument) and doc.titre == reddit_doc_name), None)
        arxiv_doc = next((doc for _, doc in self.id2doc.items() if isinstance(doc, ArxivDocument) and doc.titre == arxiv_doc_name), None)

        if reddit_doc is None or arxiv_doc is None:
            print("One or both documents not found.")
            return

        # Tokenize for WordCloud
        reddit_tokens = nltk.word_tokenize(reddit_doc.texte)
        arxiv_tokens = nltk.word_tokenize(arxiv_doc.texte)

        # Generate WordCloud for Reddit document
        wordcloud_reddit = WordCloud(width=400, height=200, background_color='white').generate(' '.join(reddit_tokens))

        # Generate WordCloud for Arxiv document
        wordcloud_arxiv = WordCloud(width=400, height=200, background_color='white').generate(' '.join(arxiv_tokens))

        # Plot both WordClouds side by side
        plt.figure(figsize=(15, 5))

        plt.subplot(1, 2, 1)
        plt.imshow(wordcloud_reddit, interpolation='bilinear')
        plt.title(f'WordCloud - {reddit_doc_name}')
        plt.axis('off')

        plt.subplot(1, 2, 2)
        plt.imshow(wordcloud_arxiv, interpolation='bilinear')
        plt.title(f'WordCloud - {arxiv_doc_name}')
        plt.axis('off')

        plt.show()

        

    
    def rechercher_documents(self, requete, afficher_texte=True):
        # Vérifier si la requête correspond à un titre, un auteur, une date ou une URL de document
        correspondances = []
        requete_minuscule = requete.lower()

        for _, doc in self.id2doc.items():
            if (
                requete_minuscule in doc.titre.lower() or
                requete_minuscule in doc.auteur.lower() or
                requete_minuscule in doc.date.lower() or
                requete_minuscule in doc.url.lower()
            ):
                correspondances.append(doc)

        if not correspondances:
            print(f"Aucun document trouvé dans le corpus pour la requête : {requete}")
            return None
        else:
            for correspondance in correspondances:
                print(f"Titre : {correspondance.titre}, Auteur : {correspondance.auteur}, Date : {correspondance.date}, URL : {correspondance.url}")
                if afficher_texte:
                    print(f"Texte : {correspondance.texte}")

            return correspondances