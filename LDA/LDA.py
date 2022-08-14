import os
import spacy
import pyLDAvis
import numpy as np
import pandas as pd
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
        self.df_document_topic = ""
        self.df_topic_distribution = ""
        self.df_topic_keywords = ""

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

    # Hot and cold topic
    def wordsInTopics(self):
        print('First 10 words in each topic:')
        featureNames = self.vectorizer.get_feature_names()
        for idx, topic in enumerate(self.best_lda_model.components_):
            print ("Topic ", idx, " ".join(featureNames[i] for i in topic.argsort()[:-10 - 1:-1]))       
    
    def calculateDominantTopic(self):
        # Create Document - Topic Matrix
        lda_output = self.best_lda_model.transform(self.vectorized)
        topicnames = ["Topic" + str(i) for i in range(self.best_lda_model.n_components)]
        docnames = ["Doc" + str(i) for i in range(len(self.data_frame))]
        self.df_document_topic = pd.DataFrame(np.round(lda_output, 2), columns=topicnames, index=docnames)
        dominant_topic = np.argmax( self.df_document_topic.values, axis=1)
        self.df_document_topic['dominant_topic'] = dominant_topic
        self.data_frame['dominant_topic'] = dominant_topic
        print('Dataframe')
        print(self.data_frame.head(4))

    def getTopicDistribution(self):
        self.df_topic_distribution = self.df_document_topic['dominant_topic'].value_counts().reset_index(name="Num Documents")
        self.df_topic_distribution.columns = ['Topic Num', 'Num Documents']
        print('Topic distribution')
        print(self.df_topic_distribution.sort_values(by=['Topic Num']))

    def topKeywordsInEachTopic(self, n_words=20):
        # Show top n keywords for each topic
        keywords = np.array(self.vectorizer.get_feature_names())
        topic_keywords = []
        for topic_weights in self.best_lda_model.components_:
            top_keyword_locs = (-topic_weights).argsort()[:n_words]
            topic_keywords.append(keywords.take(top_keyword_locs))
        self.df_topic_keywords = pd.DataFrame(topic_keywords)
        self.df_topic_keywords.columns = ['Word '+str(i) for i in range(self.df_topic_keywords.shape[1])] 
        self.df_topic_keywords['Topic'] = ['Topic '+str(i) for i in range(self.df_topic_keywords.shape[0])]
        self.df_topic_keywords.set_index('Topic')
        print(f'Top {n_words} words in each topic')
        print(self.df_topic_keywords)

    def printAbstractForTopic(self, topic=0):
        abstract = self.data_frame[self.data_frame.dominant_topic == topic].Abstract
        print(f'Abstract belonging to topic number {topic}')
        print(abstract)

    def topCitedTopics(self):
        cite_sum = []
        topic_age = []

        for i in range(self.best_lda_model.n_components):
            group_rows = self.data_frame[self.data_frame.dominant_topic == i]
            cite_sum.append(group_rows.Cites.sum())
            topic_age.append((2023 - group_rows.Date.astype('datetime64[ns]').dt.year).sum())
            
        self.df_topic_distribution['Cite Sum'] = cite_sum
        self.df_topic_distribution['Topic Age'] = topic_age
        self.df_topic_distribution['Paper Count'] = self.df_topic_distribution['Num Documents']
        self.df_topic_distribution['Cite Per Year'] = self.df_topic_distribution['Cite Sum'] / self.df_topic_distribution['Topic Age']
        self.df_topic_distribution['Cite Per Topic'] = self.df_topic_distribution['Cite Sum'] / self.df_topic_distribution['Paper Count']

        # Top cited per year
        top_cited_per_year = self.df_topic_distribution[self.df_topic_distribution['Cite Per Year'] == self.df_topic_distribution['Cite Per Year'].max()]
        print('Top cited per year')
        print(self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(top_cited_per_year['Topic Num'].values[0])])

        # Most cited
        most_cited = self.df_topic_distribution[self.df_topic_distribution['Cite Sum'] == self.df_topic_distribution['Cite Sum'].max()]
        print('Most cited')
        print(self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(most_cited['Topic Num'].values[0])])

        # Oldest topic
        oldest_topic = self.df_topic_distribution[self.df_topic_distribution['Topic Age'] == self.df_topic_distribution['Topic Age'].max()]
        print('Oldest topic')
        print(self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(oldest_topic['Topic Num'].values[0])])

        # Most popular topic
        most_popular = self.df_topic_distribution[self.df_topic_distribution['Paper Count'] == self.df_topic_distribution['Paper Count'].max()]
        self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(most_popular['Topic Num'].values[0])]

    def getTopFive(self):
        # Top 5 cited per year
        sorted_cite_per_year = self.df_topic_distribution.sort_values(by='Cite Per Year', ascending=False)
        top_five_topic_numbers = sorted_cite_per_year[:5]
        print('Top 5 cited topics per year')
        for index, row in top_five_topic_numbers.iterrows():
            words = self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(int(row['Topic Num']))]
            print(words)

        # Top 5 most cited 
        sorted_cited = self.df_topic_distribution.sort_values(by='Cite Sum', ascending=False)
        top_five_topic_numbers = sorted_cited[:5]
        print('Top 5 Most cited topics')
        for index, row in top_five_topic_numbers.iterrows():
            words = self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(int(row['Topic Num']))]
            print(words)

        # Top 5 oldest topic
        sorted_topic_age = self.df_topic_distribution.sort_values(by='Topic Age', ascending=False)
        top_five_topic_numbers = sorted_topic_age[:5]
        print('Top 5 Oldest topics')
        for index, row in top_five_topic_numbers.iterrows():
            words = self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(int(row['Topic Num']))]
            print(words)

        # Top 5 most popular
        sorted_paper_count = self.df_topic_distribution.sort_values(by='Paper Count', ascending=False)
        top_five_topic_numbers = sorted_paper_count[:5]
        print('Top 5 most cited topics')
        for index, row in top_five_topic_numbers.iterrows():
            words = self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(int(row['Topic Num']))]
            print(words)
    
