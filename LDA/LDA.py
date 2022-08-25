import os
import spacy
import pyLDAvis
import numpy as np
import pandas as pd
import pyLDAvis.sklearn
from ast import literal_eval
import statsmodels.api as sma
from collections import Counter
from sklearn.model_selection import GridSearchCV
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
 

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


class LDA():
    """This is the class implementation for calculating LDA
    """
    def __init__(self, data_frame):
        self.data_frame = data_frame 
        self.dirName = ""
        self.tokenized = ""
        self.lemmatized = ""
        self.vectorizer = ""
        self.vectorized = ""
        self.lda_model = ""
        self.best_lda_model = ""
        self.best_model_output = ""
        self.df_document_topic = ""
        self.df_topic_distribution = ""
        self.df_topic_keywords = ""
        self.hot = ""
        self.cold =""

    def createOutputDir(self, dirName):
        """This function creates output directory for file storage

        Args:
            dirName (str): Name of the directory you want to create
        """
        self.dirName = dirName
        does_folder_exist = os.path.exists(f'../Output/{dirName}')
        if (does_folder_exist):
            print("Output directory already exists.")         
        else:
            os.makedirs(f'../Output/{dirName}')
        print('Folder created for output storage') 

    def mergeTokenizedData(self):
        """This function converts the string representation of tokenized data into list
        """
        tokenized_rows = []
        for index, row in self.data_frame.iterrows(): 
            tokenized_rows.append(literal_eval(row["Tokenized_data"]))
        self.tokenized = tokenized_rows
    
    def lemmatization(self, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
        """This function is used to lemmitize the tokenized data

        Args:
            allowed_postags (list, optional): Allowed postags for lemmitization. Defaults to ['NOUN', 'ADJ', 'VERB', 'ADV'].
        """
        # Run in terminal: python -m spacy download en
        nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])
        texts_out = []
        for sent in self.tokenized:
            doc = nlp(" ".join(sent)) 
            texts_out.append(" ".join([token.lemma_ if token.lemma_ not in ['-PRON-'] else '' for token in doc if token.pos_ in allowed_postags]))
        self.lemmatized = texts_out

    def vectorization(self):
        """This function is used to vectorize the lemmitized data
        """
        self.vectorizer = CountVectorizer(analyzer='word',       
                             min_df=10,                        # minimum reqd occurences of a word 
                             stop_words='english',             # remove stop words
                             lowercase=True,                   # convert all words to lowercase
                             token_pattern='[a-zA-Z0-9]{3,}',  # num chars > 3
                             # max_features=50000,             # max number of uniq words
                            )
        self.vectorized = self.vectorizer.fit_transform(self.lemmatized)

    def computeSparsicity(self):
        """This function computes the sparsicity
        """
        data_dense = self.vectorized.todense()
        print("Sparsicity: ", ((data_dense > 0).sum()/data_dense.size)*100, "%")

    def buildLDAModel(self): 
        """This function builds LDA model and calculates its log-likelihood and Perplexity
        """
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
        """This function generates the pyLDAvis report and saves it to the output folder
        """
        panel = pyLDAvis.sklearn.prepare(self.lda_model, self.vectorized, self.vectorizer, mds='tsne')
        pyLDAvis.save_html(panel, os.path.join("../Output/" + f'{self.dirName}/{self.dirName}_lda.html'))
        print('File saved')
         
    def buildImprovisedLDAModel(self): 
        """This builds the optimized LDA model by using GridSearchCV
        """
        print('Building improvised model')
        search_params = {'n_components': [10, 15, 20, 25, 30], 'learning_decay': [.5, .7, .9]}
        lda = LatentDirichletAllocation()
        model = GridSearchCV(lda, param_grid=search_params)
        model.fit(self.vectorized)
        self.best_lda_model = model.best_estimator_
        self.best_model_output = self.best_lda_model.fit_transform(self.vectorized)
        print("Best Models Params: ", model.best_params_)
        print("Best Log Likelihood Score: ", model.best_score_)
        print("Model Perplexity: ", self.best_lda_model.perplexity(self.vectorized))
        panel = pyLDAvis.sklearn.prepare(self.best_lda_model, self.vectorized, self.vectorizer, mds='tsne')
        pyLDAvis.save_html(panel, os.path.join("../Output/" + f'{self.dirName}/{self.dirName}_best_lda.html'))
        print('File saved')
 
    def wordsInTopics(self):
        """Display first 10 words in each topic
        """
        print('First 10 words in each topic:')
        featureNames = self.vectorizer.get_feature_names()
        for idx, topic in enumerate(self.best_lda_model.components_):
            print ("Topic ", idx, " ".join(featureNames[i] for i in topic.argsort()[:-10 - 1:-1]))       
    
    def calculateDominantTopic(self):
        """This function calculates which topic is dominant for each data point/row in the dataframe
        """
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
        """This function displays the distribution of data/rows/papers per topic
        """
        self.df_topic_distribution = self.df_document_topic['dominant_topic'].value_counts().reset_index(name="Num Documents")
        self.df_topic_distribution.columns = ['Topic Num', 'Num Documents']
        print('Topic distribution')
        print(self.df_topic_distribution.sort_values(by=['Topic Num']))

    def topKeywordsInEachTopic(self, n_words=20):
        """This function displays top keywords in each topic

        Args:
            n_words (int, optional): Number of words you want to display. Defaults to 20.
        """
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
        """This function prints the abstract for the given topic

        Args:
            topic (int, optional): Topic number for which you want to display the abstract. Defaults to 0.
        """
        abstract = self.data_frame[self.data_frame.dominant_topic == topic].Abstract_clean
        print(f'Abstract belonging to topic number {topic}')
        print(abstract)

    def topCitedTopics(self):
        """This function calculates the top cited topics according to total cites, topic age, paper count, cite per year and cite per topic
        """
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
        """This function calculates the top five cited topics according to total cites, topic age, paper count, cite per year and cite per topic
        """
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
    
    def hotAndColdTopicByDate(self):
        medians = []
        for i in range(self.best_lda_model.n_components):
            group_rows = self.data_frame[self.data_frame.dominant_topic == i]
            median = group_rows.Date.astype('datetime64[ns]').quantile(0.5, interpolation="midpoint")
            medians.append(median)
        
        median_dates = pd.DataFrame(medians, columns=['Date'])
        median_dates['Date'].dt.date 

        self.hot = median_dates['Date'].idxmax() 
        hot_words = self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(self.hot)]
        print('Hot Words')
        print(hot_words)

        hot_topics = self.data_frame[self.data_frame['dominant_topic'] == self.hot]
        print('Hot topic titles:')
        print(hot_topics.Title_clean)

        self.cold = median_dates['Date'].idxmin() 
        cold_words = self.df_topic_keywords[self.df_topic_keywords.Topic == 'Topic '+str(self.cold)]
        print('Cold Words')
        print(cold_words)

        cold_topics = self.data_frame[self.data_frame['dominant_topic'] == self.cold]
        print('Cold topic titles')
        print(cold_topics.Title_clean)
   
    def plotTopicTrend(self):
        self.data_frame['Year'] = pd.DatetimeIndex(self.data_frame['Date']).year
 
        topic_dictionaries = []

        for i in range(self.best_lda_model.n_components):
            group_rows = self.data_frame[self.data_frame.dominant_topic == i]
            topic_years = group_rows.Year
            topic_year_count = Counter(topic_years) 
            topic_dictionaries.append(topic_year_count)
            
        topic_trend = pd.DataFrame.from_dict(topic_dictionaries)
        topic_trend.set_index(topic_trend.columns[0])
        topic_trend.fillna(0, inplace=True) 
        topic_trend_transposed = topic_trend.T
        topic_trend_transposed['Year'] = list(topic_trend.columns)
        topic_trend_transposed.drop(['Year'], axis=1, inplace=True)
        topic_trend_transposed.sort_index(inplace=True)
        ax = topic_trend_transposed.plot(figsize=(20, 10), title='Topic trends')
        ax.set_xticklabels(topic_trend_transposed.index)
        ax.get_figure().savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_topic_trends.png"))
        print('Topic Trends image saved')

    def plotHotVsCold(self):
        hot_topic_data = self.data_frame[self.data_frame['dominant_topic'] == self.hot]
        hot_topic_data_years =  hot_topic_data.Year
        hot_topic_year_count = [Counter(hot_topic_data_years)] 
        hot_topic_year_count=  pd.DataFrame.from_dict(hot_topic_year_count)
        hot_topic_year_count['Type'] = 'Hot topic'
        
        cold_topic_data = self.data_frame[self.data_frame['dominant_topic'] == self.cold]
        cold_topic_data_years =  cold_topic_data.Year
        cold_topic_year_count = [Counter(cold_topic_data_years)] 
        cold_topic_year_count=  pd.DataFrame.from_dict(cold_topic_year_count)
        cold_topic_year_count['Type'] = 'Cold Topic'

        combined = pd.concat([hot_topic_year_count, cold_topic_year_count], ignore_index=True)
        combined.fillna(0, inplace=True)
        
        combined_trasnposed = combined.T 
        combined_trasnposed.rename(columns={0: "Hot Topic", 1: "Cold Topic"}, inplace=True)
        combined_trasnposed.drop(['Type'], axis=0, inplace=True)
        combined_trasnposed.sort_index(inplace=True)
        
        ax = combined_trasnposed.plot(figsize=(20, 10), title='Hot vs Cold')
        ax.set_xticklabels(combined_trasnposed.index)
        ax.get_figure().savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_hot_vs_cold.png"))
        print('Hot vs cold image saved')

    def trendAnalysisUsingTheta(self):
        theta = self.best_model_output
        years = pd.DatetimeIndex(self.data_frame['Date']).year
        theta_df = pd.DataFrame(theta)
        theta_df['Years'] = years

        unique_years = theta_df['Years'].unique()
        theta_mean_by_year = []

        for i in range(len(unique_years)):
            grouped_thetas = theta_df[theta_df['Years'] == unique_years[i]]
            theta_mean_by_year.append(grouped_thetas.mean())
            
        theta_mean_by_year = pd.DataFrame(theta_mean_by_year)
        x = theta_mean_by_year['Years']

        cols = theta_mean_by_year.drop(['Years'], axis=1).columns

        model_details = []

        for index, value in enumerate(cols):
            y = theta_mean_by_year[value]
            est = sma.OLS(y, x)
            fitted_model = est.fit()
            details = {
                'topic' : value,
                'pvalue' : fitted_model.pvalues[0],
                'coef' : fitted_model.params[0]
            }
            model_details.append(details)
            
        model_details_df = pd.DataFrame.from_dict(model_details)  
        positive_slope = model_details_df[model_details_df['coef'] >=0]
        negative_slope = model_details_df[model_details_df['coef'] <0]
        print(positive_slope.shape, negative_slope.shape)

        p_level = [0.01, 0.03, 0.05]
        trends = []

        for i in range(len(p_level)):
            positive_group = positive_slope[positive_slope['pvalue'] <= p_level[i]]
            negative_group = negative_slope[negative_slope['pvalue'] <= p_level[i]]
            count_pos = len(positive_group)
            count_neg = len(negative_group)
            data = {
                'P-level' : p_level[i],
                'Negative Trend': count_neg,
                'Positive Trend' : count_pos,
                'Hot Topics' : positive_group.topic.values,
                'Cold Topics' : negative_group.topic.values
                
            }
            trends.append(data)
            
        trends = pd.DataFrame(trends)
        
        thetas_by_year = theta_mean_by_year 
        thetas_by_year.sort_values(by='Years',inplace=True)

        hot_topics =  list(trends[trends['P-level'] == 0.05]['Hot Topics'])
        cold_topics =  list(trends[trends['P-level'] == 0.05]['Cold Topics']) 

        hot_topic_trend = thetas_by_year[hot_topics[0]]
        if  hot_topic_trend.shape[1] > 0:
            hot_topic_trend['Years'] = theta_mean_by_year.Years
            
        cold_topic_trend = thetas_by_year[cold_topics[0]]
        if  cold_topic_trend.shape[1] > 0:
            cold_topic_trend['Years'] = theta_mean_by_year.Years


        if hot_topic_trend.shape[1] > 0:
            ax = hot_topic_trend.plot(x='Years',figsize=(20, 10))
            ax.set_xticklabels(theta_mean_by_year.Years)
            ax.get_figure().savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_hot_based_on_theta.png"))
            print('Hot topics based on theta image saved')
        else: 
            print('No hot topic')

        
        if cold_topic_trend.shape[1] > 0:
            ax = cold_topic_trend.plot(x='Years',figsize=(20, 10))
            ax.set_xticklabels(cold_topic_trend.Years)
            ax.get_figure().savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_cold_based_on_theta.png"))
            print('Cold topics based on theta image saved')
            
        else: 
            print('No cold topic')