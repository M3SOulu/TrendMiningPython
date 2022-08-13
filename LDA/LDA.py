import os
import spacy
import pyLDAvis
import pyLDAvis.sklearn
from ast import literal_eval
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer



class LDA():
    def __init__(self, data_frame):
        self.data_frame = data_frame 
        self.dirName = ""
        self.tokenized = ""
        self.lemmatized = ""
        self.vectorizer = ""
        self.vectorized = ""
        self.lda_model = ""
        self.best_lda_model = ""

    def createOutputDir(self, dirName):
        self.dirName = dirName
        does_folder_exist = os.path.exists(f'../Output/{dirName}')
        if (does_folder_exist):
            print("Output directory already exists.")         
        else:
            os.makedirs(f'../Output/{dirName}')
        print('Folder created for output storage') 

    def mergeTokenizedData(self):
        tokenized_rows = []
        for index, row in self.data_frame.iterrows(): 
            tokenized_rows.append(literal_eval(row["Tokenized_data"]))
        self.tokenized = tokenized_rows
    
    def lemmatization(self, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        # Run in terminal: python -m spacy download en
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        texts_out = []
        for sent in self.tokenized:
            doc = nlp(" ".join(sent)) 
            texts_out.append(" ".join([token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))
        self.lemmatized = texts_out

    def vectorization(self):
        self.vectorizer = CountVectorizer(analyzer='word',       
                             min_df=10,                        # minimum reqd occurences of a word 
                             stop_words='english',             # remove stop words
                             lowercase=True,                   # convert all words to lowercase
                             token_pattern='[a-zA-Z0-9]{3,}',  # num chars > 3
                             # max_features=50000,             # max number of uniq words
                            )
        self.vectorized = self.vectorizer.fit_transform(self.lemmatized)

    def computeSparsicity(self):
        data_dense = self.vectorized.todense()
        print("Sparsicity: ", ((data_dense > 0).sum()/data_dense.size)*100, "%")

    def buildLDAModel(self): 
        self.lda_model = LatentDirichletAllocation(
                                      n_components=20,               # Number of topics
                                      max_iter=10,               # Max learning iterations
                                      learning_method='online',   
                                      random_state=100,          # Random state
                                      batch_size=128,            # n docs in each learning iter
                                      evaluate_every = -1,       # compute perplexity every n iters, default: Don't
                                      n_jobs = -1,               # Use all available CPUs
                                      doc_topic_prior = None,
                                      learning_decay = 0.7,
                                      topic_word_prior = None,
                                     )
        lda_output = self.lda_model.fit_transform(self.vectorized)
        # See model parameters
        print('Model Parameters',self.lda_model.get_params())
        # Log Likelyhood: Higher the better
        print("Log Likelihood: ", self.lda_model.score(self.vectorized))
        # Perplexity: Lower the better. Perplexity = exp(-1. * log-likelihood per word)
        print("Perplexity: ", self.lda_model.perplexity(self.vectorized))
        
    def visualizeLDAvis(self):
        panel = pyLDAvis.sklearn.prepare(self.lda_model, self.vectorized, self.vectorizer, mds='tsne')
        pyLDAvis.save_html(panel, os.path.join("../Output/" + f'{self.dirName}/{self.dirName}_lda.html'))
        print('File saved')
         
    def buildImprovisedLDAModel(self): 
        print('Building improvised model')
        search_params = {'n_components': [10, 15, 20, 25, 30], 'learning_decay': [.5, .7, .9]}
        lda = LatentDirichletAllocation()
        model = GridSearchCV(lda, param_grid=search_params)
        model.fit(self.vectorized)
        self.best_lda_model = model.best_estimator_
        print("Best Models Params: ", model.best_params_)
        print("Best Log Likelihood Score: ", model.best_score_)
        print("Model Perplexity: ", self.best_lda_model.perplexity(self.vectorized))
        panel = pyLDAvis.sklearn.prepare(self.best_lda_model, self.vectorized, self.vectorizer, mds='tsne')
        pyLDAvis.save_html(panel, os.path.join("../Output/" + f'{self.dirName}/{self.dirName}_best_lda.html'))
        print('File saved')

        
