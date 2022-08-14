import pandas as pd
from LDA.LDA import LDA


try:
    stackoverflow_data = pd.read_csv('../../Data/stackoverflow_data.csv')
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)


stackoverflow_lda = LDA(stackoverflow_data)
stackoverflow_lda.createOutputDir('Stackoverflow')
stackoverflow_lda.mergeTokenizedData()
stackoverflow_lda.lemmatization(allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
stackoverflow_lda.vectorization()
stackoverflow_lda.computeSparsicity()
stackoverflow_lda.buildLDAModel()
stackoverflow_lda.visualizeLDAvis()
stackoverflow_lda.buildImprovisedLDAModel()
stackoverflow_lda.wordsInTopics()
stackoverflow_lda.calculateDominantTopic()
stackoverflow_lda.getTopicDistribution()
stackoverflow_lda.topKeywordsInEachTopic()
stackoverflow_lda.printAbstractForTopic(0)
stackoverflow_lda.topCitedTopics()
stackoverflow_lda.getTopFive()