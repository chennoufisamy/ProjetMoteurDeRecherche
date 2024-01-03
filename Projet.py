import praw
import urllib
import urllib.request as libreq
import xmltodict
import pandas as pd
import datetime
import pickle
import re
from Document import Document
from Author import Author
from Corpus import Corpus
from Document import Document, RedditDocument, ArxivDocument

#connexion à l API
# r = praw.Reddit(client_id='zMgIHZUswL7lu-_SY_M3CA', client_secret='BILw8OIo0DCVBiKm62KCiaf2UnPTmA', user_agent='Chennoufi')

# #creation liste docs
# docs = []


# #recuperer et inserer les subreddit dans la liste docs
# astrophysics_reddit = r.subreddit('Astrophysics').hot(limit=50)
# for ligne in astrophysics_reddit:
#     document_info = {
#         'Titre': ligne.title.replace('\n', ''),
#         'Auteur': str(ligne.author),
#         'Date': datetime.datetime.fromtimestamp(ligne.created).strftime("%Y/%m/%d"),
#         'URL': "https://www.reddit.com/"+ligne.permalink,
#         'Texte': ligne.selftext.replace('\n',''),
#         'NCommentaires': str(ligne.num_comments)
#     }
#     docs.append(document_info)
    
# for d in docs:
#     print(d)

# # creation de l url
# method_name='search_query=all:astrophysics'

# #nombre max de resultats
# max_results = 'max_results=50'

# #concatenation URL
# url = f'http://export.arxiv.org/api/query?{method_name}&{max_results}'

# #effectuer la requete
# with libreq.urlopen(url) as url:
#     r = url.read()

# #convertir le resultat dans un dictionnaire 
# data = xmltodict.parse(r)

# print(docs)

# Affecter les donees dans deux champs
# astrophysics_arxiv = data['feed']['entry']

# Recuperer le title de chaque article et le mettre dans docs
# for entry in astrophysics_arxiv:
#     try:
#         authors = ", ".join([a["name"] for a in entry["author"]]) # On fait une liste d'auteurs, séparés par une virgule
#     except:
#         authors = entry["author"]["name"] # Si l'auteur est seul, pas besoin de liste
#     document_info = {
#     "Titre": entry['title'].replace('\n',''), # On enlève les retours à la ligne
#     "Auteur": authors,
#     "Date": datetime.datetime.strptime(entry['published'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y/%m/%d"), # Formatage de la date en année/mois/jour avec librairie datetime
#     "URL": entry['link'],
#     "Texte": entry['summary'].replace('\n', '')
#     }
#     docs.append(document_info) # Ajout du document a la liste

# Creation d'un dictionnaire pour stocker les ids
# ids = pd.Series([]) 

# Creation d'une liste pour contenir 50 chaines reddit et 50 chaines arxiv (origine du document)
# redditOrarxiv = []

# Creation d'un catalogue pour y mettre les donees
# catalogue =pd.DataFrame(docs,columns=['Titre', 'Auteur', 'Date', 'URL', 'Texte', 'NCommentaires'])
# print (df)

# Remplissage du dictionnaire ids avec un indice i 
# for i in range(len(docs)):
#     ids[i] = str(i)

# Ajout des ID dans le dataframe
# catalogue.insert(0,"ID",ids)

# #Remplissage de redditOrarxiv
# for i in range(50):
#     redditOrarxiv.append('reddit')
# for i in range(50):
#     redditOrarxiv.append('arxiv')

# print(redditOrarxiv)

# Insertion de redditOrarxiv dans la derniere colonne du cataloge
# catalogue.insert(6,"Origine",redditOrarxiv)      

# Creation du fichier csv contenant les donees du catalogue
# csv_file = 'donnees.csv'
# catalogue.to_csv(csv_file, sep=',', index=True)

#Ouverture du fichier
with open('donnees.csv', newline='',encoding="utf-8") as f:
    file = pd.read_csv(f,sep=',')

#Creation d'un dataframe
df_reddit_arxiv = pd.DataFrame(file)

# Creation d'un dictionnaire pour y contenir le nombre de mots et nombre de phrases des titres du catalogue
# taille_document = {'nb_mots' : [], 'nb_ph' : []}

# Remplissage du dictionnaire
# for document in df_reddit_arxiv['Titre']:
#     taille_document['nb_mots'].append(len(document.split(' '))) #On compte le nombre de mots (en comptant le nombre d'espaces)
#     taille_document['nb_ph'].append(len(document.split('.'))) #On compte le nombre de phrases (en comptant le nombre de points) 

# print(len(taille_document['nb_mots']))

# Creation de la liste des documents pertinents
# df_document_pertinent = []

# Remplissage de la liste
# for document in df_reddit_arxiv['Titre']:
#     if(len(df_reddit_arxiv['Titre'])) >= 20: #Si la longeur du titre est superieur a 20 on insere le titre dans la liste
#         df_document_pertinent.append(document)

# Concatenation des titree dans une chaine de caracteres
# chaine_documents =''.join(df_document_pertinent)

# Affichage de la chaine
# print(chaine_documents)

# Creation d'un dictionnaire documents
id2doc = {}

# Iteation du dataframe
for i,doc in df_reddit_arxiv.iterrows():
    
   #Recuperation des donees
    titre = doc['Titre']
    auteur = doc['Auteur']
    date = doc['Date']
    url = doc['URL']
    texte = doc['Texte']
    type = doc['Origine']
    id2doc[i] = Document(titre,auteur,date,url,texte,type) #Ajout d'un objet Document dans le dictionnaire indexe par un ID

# for  key  in  id2doc:
#   print(id2doc[key])

#Creation d'un dictionnaire auteurs
id2aut = {}
num_auteurs_vus = 0
authors = {}

# for key in id2doc:
#     if(id2doc[key].auteur not in id2aut): #On ajoute un auteur seulement si l'auteur n'y existe pas
#         id2aut[id2doc[key].auteur] = Author(id2doc[key].auteur) #Ajout d'un objet Author dans le dictionnaire indexe par le nom de l'auteur
#         id2aut[id2doc[key].auteur].add(id2doc) #Ajout de l'auteur dans le catalogue de l'objet Author

for _,doc in df_reddit_arxiv.iterrows():
    if doc['Auteur'] not in id2aut:
        num_auteurs_vus += 1
        authors[num_auteurs_vus] = Author(doc['Auteur'])
        id2aut[doc['Auteur']] = num_auteurs_vus

    authors[id2aut[doc['Auteur']]].add(doc['Texte'])


# Input emis par l'utilisateur
# auteur_recherche = input("Entrez le nom de l'auteur pour obtenir des statistiques : ")

# Si l'auteur emirs par l'utilisateur existe dans id2aut
# if auteur_recherche in id2aut:
#     auteur = id2aut[auteur_recherche]
#     print("Statistiques pour l'auteur : " + auteur.nom) #On affiche le nom
#     print("Nombre de documents produits : " + str(auteur.ndoc)) #On affiche le nombre de documents produits
#     total_taille_documents = sum(len(doc) for doc in auteur.production.values()) #On affiche le total de la longeur de ses documents
#     taille_moyenne = total_taille_documents / auteur.ndoc if auteur.ndoc > 0 else 0 #On cree la moyenne entre la taille totale des documents et les documents ecrits par l'auteur
#     print("Taille moyenne des documents : " + str(taille_moyenne) + " caractères")
# else:
#     print("L'auteur " + auteur_recherche + " n'est pas dans la base de données.")

#Creation du corpus
corpus = Corpus("Corpus1")
# corpus.tri_nom()
# corpus.tri_date()

# Preparation des donees a inserer dans le corupus
# for i,doc in df_reddit_arxiv.iterrows():
#     corpus.add(doc)
    
# Conversion du dataframe en une liste
docs = df_reddit_arxiv.to_dict(orient='records')

# Insertion donees avec la factory
for doc in docs:
    corpus.add(Corpus.factory(doc['Origine'],doc))

# Sauvegarde du corpus dans le disque dur
# corpus.save('corpus1.csv')

# Ouvrir le corpus
corpus_load = corpus.load('corpus1.csv')
print(corpus_load)