import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import Toplevel, Text, Scrollbar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from Document import RedditDocument,ArxivDocument
from Corpus import Corpus
from matplotlib.figure import Figure
from ttkthemes import ThemedTk
import sv_ttk


# import tkinter as tk
# from tkinter import ttk
# # Create a style
# style = ttk.Style(root)

# # Import the tcl file
# root.tk.call("source", "forest-dark.tcl")

# # Set the theme with the theme_use method
# style.theme_use("forest-dark")



class VisualInterface:
    def __init__(self, corpus):
        self.corpus = corpus
        self.root = ThemedTk(theme="scidgrey")
        self.root.title("Interface pour l'Analyse de Documents")
        self.notebook = ttk.Notebook(self.root)

        self.tab_search = ttk.Frame(self.notebook)
        self.tab_compare = ttk.Frame(self.notebook)
        self.tab_temporal = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_search, text='Rechercher un Document')
        self.notebook.add(self.tab_compare, text='Comparer deux Documents')
        self.notebook.add(self.tab_temporal, text='Évolution temporelle des Mots')

        self.notebook.pack(expand=1, fill="both")

        # Search Documents Tab
        self.create_search_tab()
        
        # Compare Documents Tab
        self.create_compare_tab()

        # Temporal Evolution Tab
        self.create_temporal_tab()

        # Make the window resizable
        self.root.resizable(True, True)

                # Increase font size
        self.increase_font_size()

    def increase_font_size(self):
        style = ttk.Style()
        style.configure('TLabel', font=('TkDefaultFont', 14))
        style.configure('TButton', font=('TkDefaultFont', 12))
        style.configure('TEntry', font=('TkDefaultFont', 12))
        style.configure('TCombobox', font=('TkDefaultFont', 12))

    # def create_compare_tab(self):
    #     label_reddit = ttk.Label(self.tab_compare, text="Sélectionner un document Reddit:")
    #     label_reddit.grid(row=0, column=0, pady=5, padx=(10, 0), sticky='w')

    #     self.reddit_var = tk.StringVar()
    #     self.reddit_dropdown = ttk.Combobox(self.tab_compare, textvariable=self.reddit_var)
    #     self.reddit_dropdown['values'] = [doc.titre for doc in self.corpus.id2doc.values() if isinstance(doc, RedditDocument)]
    #     self.reddit_dropdown.grid(row=0, column=1, pady=5, padx=(10, 0), sticky='w')

    #     label_arxiv = ttk.Label(self.tab_compare, text="Sélectionner un document Arxiv:")
    #     label_arxiv.grid(row=1, column=0, pady=5, padx=(10, 0), sticky='w')

    #     self.arxiv_var = tk.StringVar()
    #     self.arxiv_dropdown = ttk.Combobox(self.tab_compare, textvariable=self.arxiv_var)
    #     self.arxiv_dropdown['values'] = [doc.titre for doc in self.corpus.id2doc.values() if isinstance(doc, ArxivDocument)]
    #     self.arxiv_dropdown.grid(row=1, column=1, pady=5, padx=(10, 0), sticky='w')

    #     compare_button = ttk.Button(self.tab_compare, text="Comparer", command=self.compare_documents)
    #     compare_button.grid(row=2, column=0, columnspan=2, pady=10, padx=(10, 0), sticky='w')
        
    def create_compare_tab(self):
        label_reddit = ttk.Label(self.tab_compare, text="Sélectionner un document Reddit:")
        label_reddit.grid(row=0, column=0, pady=5, padx=(10, 0), sticky='w')

        self.reddit_var = tk.StringVar()
        self.reddit_dropdown = ttk.Combobox(self.tab_compare, textvariable=self.reddit_var)
        self.reddit_dropdown['values'] = [doc.titre for doc in self.corpus.id2doc.values() if isinstance(doc, RedditDocument)]
        self.reddit_dropdown.grid(row=0, column=1, pady=5, padx=(10, 0), sticky='w')

        label_arxiv = ttk.Label(self.tab_compare, text="Sélectionner un document Arxiv:")
        label_arxiv.grid(row=1, column=0, pady=5, padx=(10, 0), sticky='w')

        self.arxiv_var = tk.StringVar()
        self.arxiv_dropdown = ttk.Combobox(self.tab_compare, textvariable=self.arxiv_var)
        self.arxiv_dropdown['values'] = [doc.titre for doc in self.corpus.id2doc.values() if isinstance(doc, ArxivDocument)]
        self.arxiv_dropdown.grid(row=1, column=1, pady=5, padx=(10, 0), sticky='w')

        compare_tfidf_button = ttk.Button(self.tab_compare, text="Comparer TF-IDF", command=self.compare_tfidf)
        compare_tfidf_button.grid(row=2, column=0, pady=10, padx=(10, 0), sticky='w')

        compare_wordcloud_button = ttk.Button(self.tab_compare, text="Comparer Word Clouds", command=self.compare_wordclouds)
        compare_wordcloud_button.grid(row=2, column=1, pady=10, padx=(10, 0), sticky='w')



    def create_search_tab(self):
        # Tab for searching by title
        label_title = ttk.Label(self.tab_search, text="Entrer le titre:")
        label_title.grid(row=0, column=0, pady=2, padx=(10, 0), sticky='w')

        self.title_entry = ttk.Entry(self.tab_search)
        self.title_entry.grid(row=0, column=1, pady=10, padx=(10, 0), sticky='w')

        title_search_button = ttk.Button(self.tab_search, text="Rechercher par Titre", command=lambda: self.search_documents("title"))
        title_search_button.grid(row=1, column=0, columnspan=2, pady=10, padx=(10, 0), sticky='w')

        # Tab for searching by author
        label_author = ttk.Label(self.tab_search, text="Entrer le nom de l'auteur:")
        label_author.grid(row=2, column=0, pady=2, padx=(10, 0), sticky='w')

        self.author_entry = ttk.Entry(self.tab_search)
        self.author_entry.grid(row=2, column=1, pady=10, padx=(10, 0), sticky='w')

        author_search_button = ttk.Button(self.tab_search, text="Rechercher par Auteur", command=lambda: self.search_documents("author"))
        author_search_button.grid(row=3, column=0, columnspan=2, pady=10, padx=(10, 0), sticky='w')

        # Tab for searching by year
        label_year = ttk.Label(self.tab_search, text="Entrer l'année:")
        label_year.grid(row=4, column=0, pady=2, padx=(10, 0), sticky='w')

        self.year_entry = ttk.Entry(self.tab_search)
        self.year_entry.grid(row=4, column=1, pady=10, padx=(10, 0), sticky='w')

        year_search_button = ttk.Button(self.tab_search, text="Rechercher par Année", command=lambda: self.search_documents("year"))
        year_search_button.grid(row=5, column=0, columnspan=2, pady=10, padx=(10, 0), sticky='w')

        # Tab for searching by source
        label_source = ttk.Label(self.tab_search, text="Entrer la source (URL):")
        label_source.grid(row=6, column=0, pady=2, padx=(10, 0), sticky='w')

        self.source_entry = ttk.Entry(self.tab_search)
        self.source_entry.grid(row=6, column=1, pady=10, padx=(10, 0), sticky='w')

        source_search_button = ttk.Button(self.tab_search, text="Rechercher par Source", command=lambda: self.search_documents("source"))
        source_search_button.grid(row=7, column=0, columnspan=2, pady=10, padx=(10, 0), sticky='w')


    def create_temporal_tab(self):
            label_temporal = ttk.Label(self.tab_temporal, text="Entrer le(s) mot(s) pour étudier l'Évolution Temporelle (séparés par un espace):")
            label_temporal.grid(row=0, column=0, pady=5, padx=(10, 0), sticky='w')

            self.temporal_entry = ttk.Entry(self.tab_temporal)
            self.temporal_entry.grid(row=0, column=1, pady=10, padx=(10, 0), sticky='w')

            temporal_button = ttk.Button(self.tab_temporal, text="Générer le Graphique", command=self.generate_temporal_graph)
            temporal_button.grid(row=5, column=0, columnspan=2, pady=10, padx=(10, 0), sticky='w')


    def compare_documents(self):
        reddit_doc_title = self.reddit_var.get()
        arxiv_doc_title = self.arxiv_var.get()

        # Check if either reddit_var or arxiv_var is empty
        if not reddit_doc_title or not arxiv_doc_title:
            # Display a message or take any other action
            print("Please select both Reddit and Arxiv documents.")
            return

        reddit_doc = next(doc for doc in self.corpus.id2doc.values() if isinstance(doc, RedditDocument) and doc.titre == reddit_doc_title)
        arxiv_doc = next(doc for doc in self.corpus.id2doc.values() if isinstance(doc, ArxivDocument) and doc.titre == arxiv_doc_title)

        comparison_result = self.corpus.comparer_reddit_arxiv()

        filtered_result = comparison_result[
            (comparison_result['Document Reddit'] == reddit_doc.titre) & 
            (comparison_result['Document Arxiv'] == arxiv_doc.titre)
        ]

        result_window = tk.Toplevel(self.root)
        result_window.title("Comparison Result")

        text_widget = scrolledtext.ScrolledText(result_window, wrap='none', height=20, width=100)
        text_widget.grid(row=0, column=0, padx=10, pady=10)

        scrollbar_x = tk.Scrollbar(result_window, orient=tk.HORIZONTAL, command=text_widget.xview)
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        text_widget.configure(xscrollcommand=scrollbar_x.set)

        result_string = pd.DataFrame.to_string(filtered_result, index=False)
        text_widget.insert('1.0', result_string)

    def compare_tfidf(self):
        # Use the existing compare_documents logic
        self.compare_documents()

    def compare_wordclouds(self):
        reddit_doc_title = self.reddit_var.get()
        arxiv_doc_title = self.arxiv_var.get()

        # Check if either reddit_var or arxiv_var is empty
        if not reddit_doc_title or not arxiv_doc_title:
            # Display a message or take any other action
            print("Please select both Reddit and Arxiv documents.")
            return

        reddit_doc = next(doc for doc in self.corpus.id2doc.values() if isinstance(doc, RedditDocument) and doc.titre == reddit_doc_title)
        arxiv_doc = next(doc for doc in self.corpus.id2doc.values() if isinstance(doc, ArxivDocument) and doc.titre == arxiv_doc_title)

        # Call the analyse_vocabulaire function to generate word clouds
        self.corpus.analyse_vocabulaire(reddit_doc.titre, arxiv_doc.titre)



    def search_documents(self, search_type, afficher_texte=True):
        query = ""

        if search_type == "title":
            query = self.title_entry.get()
        elif search_type == "author":
            query = self.author_entry.get()
        elif search_type == "year":
            query = self.year_entry.get()
        elif search_type == "source":
            query = self.source_entry.get()

        if not query:
            print("Veuillez entrer une requête.")
            return

        # Utilize the rechercher_documents function of the corpus to get the results
        results = self.corpus.rechercher_documents(query, afficher_texte)

        if results:
            result_window = tk.Toplevel(self.root)
            result_window.title("Résultats de la Recherche")

            text_widget = scrolledtext.ScrolledText(result_window, wrap='none', height=20, width=100)
            text_widget.grid(row=0, column=0, padx=10, pady=10)

            scrollbar_x = tk.Scrollbar(result_window, orient=tk.HORIZONTAL, command=text_widget.xview)
            scrollbar_x.grid(row=1, column=0, sticky='ew')
            text_widget.configure(xscrollcommand=scrollbar_x.set)

            for result in results:
                # Display the text of the document
                if afficher_texte:
                    text_widget.insert('1.0', f"Texte : {result.texte}\n")

                # Display the URL of the document
                text_widget.insert('1.0', f"URL : {result.url}\n")

                # Display the date of the document
                text_widget.insert('1.0', f"Date : {result.date}\n")

                # Display the author of the document
                text_widget.insert('1.0', f"Auteur : {result.auteur}\n")

                # Display the title of the document
                text_widget.insert('1.0', f"Titre : {result.titre}\n")

                # Add an empty line between documents
                text_widget.insert('1.0', "\n")

            # Add a callback to clear the widgets when the results window is closed
            result_window.protocol("WM_DELETE_WINDOW", lambda: self.clear_results(result_window, afficher_texte))
        else:
            print(f"Aucun document trouvé dans le corpus pour la requête : {query}")

    def clear_results(self, result_window, afficher_texte=True):
        # Clear the text widget and reset the entry fields
        result_window.destroy()
        if afficher_texte:
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
            self.year_entry.delete(0, tk.END)
            self.source_entry.delete(0, tk.END)


    def generate_temporal_graph(self):
        words = [word.strip() for word in self.temporal_entry.get().split()]

        # Check if there is input in the temporal_entry
        if not words:
            # Display a message or take any other action
            print("Please enter word(s) before generating the graph.")
            return

        self.corpus.observer_evolution_temporelle(words)

    def run(self):
        self.root.mainloop()


