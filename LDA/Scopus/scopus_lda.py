import pandas as pd
from LDA.LDA import LDA


try:
    scopus_data = pd.read_csv('../../Data/scopus_data.csv')
except FileNotFoundError:
    print("FileNotFoundError: File not found. Please make sure you have mined the data first")
except NameError:
    print("NameError: File not found. Please make sure you have mined the data first")
except Exception as e:
    print("Something went wrong with file reading", e)


scopus_lda = LDA(scopus_data)
scopus_lda.createOutputDir('Scopus')
scopus_lda.mergeTokenizedData()
scopus_lda.lemmatization(allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
scopus_lda.vectorization()
scopus_lda.computeSparsicity()
scopus_lda.buildLDAModel()
scopus_lda.visualizeLDAvis()
scopus_lda.buildImprovisedLDAModel()
