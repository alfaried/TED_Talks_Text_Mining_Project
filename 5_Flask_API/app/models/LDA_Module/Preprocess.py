import gensim
import nltk
import re
import os

from app import app

# Declare global variables
dictionary_folder = app.config['SITE_ROOT'] + '/app/models/LDA_Module/models/dictionary/'
stop_list = nltk.corpus.stopwords.words("english")
stemmer = nltk.stem.porter.PorterStemmer()

class Dataset:
    # Initialize class method
    def __init__(self, file_path, type):
        print("Initializing " + type + " dataset")
        self.file_path = file_path

        # Initialize variables
        self.corpus = None
        self.docs = None
        self.dictionary = None
        self.vecs = None

        # Assign variables
        print("Loading corpus..")
        self.load_corpus()

        print("Loading docs..")
        self.convert_corpus_to_docs()

        print("Loading dictionary..")
        if type.lower() == "train":  
            self.convert_docs_to_dictionary()
        elif type.lower() == "test":
            self.load_dictionary()

        print("Loading vecs..")
        self.convert_docs_to_vecs()


    # SETTER Methods
    def set_corpus(self, corpus):
        if corpus == None:
            raise Exception("corpus required")

        self.corpus = corpus

    def set_docs(self, docs):
        if docs == None:
            raise Exception("docs required")

        self.docs = docs

    def set_vecs(self, vecs):
        if vecs == None:
            raise Exception("vecs required")

        self.vecs = vecs

    def set_dictionary(self, dictionary):
        if dictionary == None:
            raise Exception("dictionary required")

        self.dictionary = dictionary


    # GETTER Methods
    def get_file_path(self):
        return self.file_path

    def get_corpus(self):
        return self.corpus

    def get_fid(self):
        return self.corpus.fileids()[0]

    def get_fids(self):
        return self.corpus.fileids()

    def get_doc(self):
        return self.docs[0]

    def get_docs(self):
        return self.docs

    def get_vec(self):    
        return self.vecs[0]

    def get_vecs(self):    
        return self.vecs

    def get_dictionary(self):  
        return self.dictionary


    # MISC
    def load_corpus(self):
        file_path = self.get_file_path()  
        file_name = ".+\.txt"  

        if ".txt" in file_path:
            arr = file_path.split("/")
            file_path = "/".join(arr[:-1]) + "/"
            file_name = arr[-1]

        corpus = nltk.corpus.PlaintextCorpusReader(file_path, file_name)
        self.set_corpus(corpus)

    def convert_corpus_to_docs(self):
        corpus = self.get_corpus()
        fids = corpus.fileids()
        docs1 = []

        for fid in fids:
            doc_raw = corpus.raw(fid)
            doc = nltk.word_tokenize(doc_raw)
            docs1.append(doc)

        docs2 = [[w.lower() for w in doc] for doc in docs1]
        docs3 = [[w for w in doc if re.search('^[a-z]+$', w)] for doc in docs2]
        docs4 = [[w for w in doc if w not in stop_list] for doc in docs3]
        docs5 = [[stemmer.stem(w) for w in doc] for doc in docs4]
        self.set_docs(docs5)

    def convert_docs_to_vecs(self):        
        docs = self.get_docs()
        dictionary = self.get_dictionary()
        vecs1 = [dictionary.doc2bow(doc) for doc in docs]
        self.set_vecs(vecs1)

    def convert_docs_to_dictionary(self):
        docs = self.get_docs()
        dictionary = gensim.corpora.Dictionary(docs)
        dictionary.save(dictionary_folder + "dictionary_48")
        self.set_dictionary(dictionary)

    def load_dictionary(self):
        if len(os.listdir(dictionary_folder)) == 0:
            raise Exception("No prior dicitonary. Please load training dataset first")

        dictionary = gensim.corpora.Dictionary.load(dictionary_folder + "dictionary_48")
        self.set_dictionary(dictionary)