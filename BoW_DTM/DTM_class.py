import os
import nltk
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer
import scipy.cluster.hierarchy as sch
from scipy.spatial.distance import pdist  
from Utils.create_file import createFile
from sklearn.feature_extraction.text import CountVectorizer



nltk.download('punkt')
nltk.download('stopwords')

class DTM():
  """
  This is the class implementation for generating Document-Term Matrix and Dendogram clustring
  """
  
  def __init__(self, data_frame):
    self.data_frame = data_frame
    self.vec_df = pd.DataFrame()
    self.frequent_words = pd.DataFrame()
    self.sorted_frequent_words = pd.DataFrame()
    self.top_words = pd.DataFrame()
    self.dirName = ""
    
    print(f'Data has {len(data_frame)} rows')


  def createOutputDir(self, dirName):
    """This function creates the folder to store the output graphs and images

    Args:
        dirName (str): Name of the output folder
    """
    self.dirName = dirName
    does_folder_exist = os.path.exists(f'../Output/{dirName}')
    if (does_folder_exist):
      print("Output directory already exists.")         
    else:
      os.makedirs(f'../Output/{dirName}')
      print('Folder created for output storage')

  def saveFile(self, file, path):
    """This function saves the file with all new columns

    Args:
        file (str): file name
        path (str): file path
    """
    createFile(file, path)
    self.data_frame.to_csv(path + '/' + file )



  def get_data(self):
    """This function returns the dataframe itself

    Returns:
        dataframe: data that is operated upon
    """
    return self.data_frame
  
  def print_data_head(self, rows=3):
    """This function prints the top rows of the data

    Args:
        rows (int, optional): number of rows from dataset you want to print. Defaults to 3.
    """
    print("Data head with top", rows, "rows")
    print(self.data_frame.head(rows))

  def print_data_tail(self, rows=3):
    """This function prints last rows of the data

    Args:
        rows (int, optional): number of rows from dataset you want to print. Defaults to 3.
    """
    print("Data tail with last", rows, "rows")
    print(self.data_frame.tail(rows))

  def print_dtm(self, rows=3):
    """This function prints the vectorized data

    Args:
        rows (int, optional): number of rows from vectorized data you want to print. Defaults to 3.
    """
    print("Vectorized data with top", rows, "rows")
    print(self.vec_df.head(rows))

  def print_frequent_words(self,rows=3):
    """This function prints the most frequent words

    Args:
        rows (int, optional): number of rows to be printed. Defaults to 3.
    """
    print("Frequent top", rows, "rows")
    print(self.frequent_words.head(rows))

  def print_sorted_frequent_words(self, rows=3):
    """This function prints the frequent words in sorted order

    Args:
        rows (int, optional): number of rows to be printed. Defaults to 3.
    """
    print(f'Top {rows} most frequent words:')
    self.sorted_frequent_words.set_index('word')
    print (self.sorted_frequent_words.head(rows) )  
  
  def print_top_words(self, rows=3):
    """This function prints the   to top words

    Args:
        rows (int, optional): number of rows to be printed. Defaults to 3.
    """
    print("Top", rows, "words")
    print(self.top_words.head(rows))

  def remove_stop_words(self, custom_stopwords = [] ):
    """This function is used to remove the stop words

    Args:
        custom_stopwords (list, optional): any other custom stop word. Defaults to [].

    Returns:
        dataframe: dataframe with removed stop words in abstract and in title 
    """
    try:
      data_frame = self.data_frame
      stop_words = set(stopwords.words("english"))
      stop_words = stop_words.union(custom_stopwords)
      print('total stop words:', len(stop_words))
      data_frame['Abstrat_without_stopwords'] = data_frame['Abstract_clean'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
      data_frame['Title_without_stopwords'] = data_frame['Title_clean'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop_words)]))
      return data_frame
    except Exception as e:
      print(e)

  def combine_title_and_abs(self):
    """This function combines the title and abstract with no stop words

    Returns:
        dataframe: dataframe with merged title and abstract in a new column
    """
    data_frame = self.data_frame
    data_frame['Merged_title_and_abs'] = data_frame["Title_without_stopwords"] + data_frame["Abstrat_without_stopwords"]
    return data_frame

  def stemming(self):
    """This function is used to stem and tokenize the data

    Returns:
        dataframe: dataframe with tokenized and stemmed data
    """
    data_frame = self.data_frame
    porter_stemmer = PorterStemmer() 
    data_frame['Tokenized_data'] = data_frame.apply(lambda row: nltk.word_tokenize(row['Merged_title_and_abs']), axis=1)
    data_frame['Stem_data'] = data_frame['Tokenized_data'].apply(lambda x : [porter_stemmer.stem(y) for y in x])
    return data_frame

  def document_term_matrix(self, column_name):
    """This function generated document term matrix

    Args:
        column_name (str): column of the dataframe to which this function is applied
    """
    data_frame = self.data_frame 
    vec = CountVectorizer()
    stem_data = data_frame.apply(lambda row : ' '.join(row[column_name]), axis=1)
    stem_data  = stem_data.tolist()
    X = vec.fit_transform(stem_data)
    self.vec_df = pd.DataFrame(X.toarray(), columns = vec.get_feature_names())


  def frequent_terms(self): 
    """This function is used to get frequent terms
    """
    vec_df = self.vec_df
    self.frequent_words['word'] = vec_df.columns
    self.frequent_words['frequency'] = list(vec_df.sum())

  def sort_frequent_terms(self):
    """This function sorts the frequent terms based on frequency
    """
    self.sorted_frequent_words = pd.DataFrame(columns=['word', 'frequency'])
    self.sorted_frequent_words = self.frequent_words.sort_values(by=['frequency'], ascending=False)
   
  def keep_top_words(self, max_frequency=100): 
    """This function keeps top words based on the max_frequency

    Args:
        max_frequency (int, optional): frequency threshold. Defaults to 100.
    """
    self.top_words = self.sorted_frequent_words[self.sorted_frequent_words['frequency'] >= max_frequency]

  def visualize_frequent_words(self):
    """Saves the frequent words to an image
    """
    plt.rcParams["figure.figsize"] = 20,40
    sns.barplot(x="frequency", y="word", data=self.top_words)
    plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_frequent_terms.png"))
 
  def dendogram_clusting(self):
    """Generates and saves dendogram to an image
    """
    distance_matrix = pdist(self.vec_df, metric='euclidean')
    plt.figure(figsize=(25, 200))
    plt.title('Hierarchical Clustering Dendrogram') 
    dendrogram = sch.dendrogram(sch.linkage(distance_matrix, method = 'ward'),
                            orientation="right", 
                            labels=self.data_frame['Title_without_stopwords'].tolist(),
                            leaf_font_size=9
                            )
    plt.savefig(os.path.join("../Output/" + self.dirName, f"{self.dirName}_dendogram.png"))
   