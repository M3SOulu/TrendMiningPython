import pandas as pd
from LDA.LDA import LDA


try:
    reddit_data = pd.read_csv('../../Data/reddit_data.csv')
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)

reddit_lda = LDA(reddit_data)
reddit_lda.createOutputDir('Reddit')
reddit_lda.mergeTokenizedData()
reddit_lda.lemmatization(allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
reddit_lda.vectorization()
reddit_lda.computeSparsicity()
reddit_lda.buildLDAModel()
reddit_lda.visualizeLDAvis()
reddit_lda.buildImprovisedLDAModel()
