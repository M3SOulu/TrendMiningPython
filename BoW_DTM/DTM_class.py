import nltk
import os
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
  
  def __init__(self, data_frame):
    self.data_frame = data_frame
    self.vec_df = pd.DataFrame()
    self.frequent_words = pd.DataFrame()
    self.sorted_frequent_words = pd.DataFrame()
    self.top_words = pd.DataFrame()
    self.dirName = ""
    
    print(f'Data has {len(data_frame)} rows')


  def createOutputDir(self, dirName):
    self.dirName = dirName
    does_folder_exist = os.path.exists(f'../Output/{dirName}')
    if (does_folder_exist):
      print("Output directory already exists.")        
      # Create Data folder if did not exist to store the csv file
    else:
      os.mkdir(f'../Output/{dirName}')
      print('Folder created for output storage')


  def get_data(self):
    return self.data_frame
  
  def print_data_head(self, rows=3):
    print("Data head with top", rows, "rows")
    print(self.data_frame.head(rows))

  def print_data_tail(self, rows=3):
    print("Data tail with last", rows, "rows")
    print(self.data_frame.tail(rows))

  def print_dtm(self, rows=3):
    print("Vectorized data with top", rows, "rows")
    print(self.vec_df.head(rows))

  def print_frequent_words(self,rows=3):
    print("Frequent top", rows, "rows")
    print(self.frequent_words.head(rows))

  def print_sorted_frequent_words(self, rows=3):
    print(f'Top {rows} most frequent words:')
    self.sorted_frequent_words.set_index('word')
    print (self.sorted_frequent_words.head(rows) )  
  
  def print_top_words(self, rows=3):
    print("Top", rows, "words")
    print(self.top_words.head(rows))

  def remove_stop_words(self, custom_stopwords = [] ):
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
    data_frame = self.data_frame
    data_frame['Merged_title_and_abs'] = data_frame["Title_without_stopwords"] + data_frame["Abstrat_without_stopwords"]
    return data_frame

  def stemming(self):
    data_frame = self.data_frame
    porter_stemmer = PorterStemmer() 
    data_frame['Tokenized_data'] = data_frame.apply(lambda row: nltk.word_tokenize(row['Merged_title_and_abs']), axis=1)
    data_frame['Stem_data'] = data_frame['Tokenized_data'].apply(lambda x : [porter_stemmer.stem(y) for y in x])
    return data_frame

  def document_term_matrix(self, column_name):
    data_frame = self.data_frame 
    vec = CountVectorizer()
    stem_data = data_frame.apply(lambda row : ' '.join(row[column_name]), axis=1)
    stem_data  = stem_data.tolist()
    X = vec.fit_transform(stem_data)
    self.vec_df = pd.DataFrame(X.toarray(), columns = vec.get_feature_names())

  def frequent_terms(self): 
    vec_df = self.vec_df
    self.frequent_words['word'] = vec_df.columns
    self.frequent_words['frequency'] = list(vec_df.sum())

  def sort_frequent_terms(self):
    self.sorted_frequent_words = pd.DataFrame(columns=['word', 'frequency'])
    self.sorted_frequent_words = self.frequent_words.sort_values(by=['frequency'], ascending=False)
   
  def keep_top_words(self, max_frequency=100): 
    self.top_words = self.sorted_frequent_words[self.sorted_frequent_words['frequency'] >= max_frequency]

  def visualize_frequent_words(self):
    plt.rcParams["figure.figsize"] = 20,40
    sns.barplot(x="frequency", y="word", data=self.top_words)
    plt.savefig(os.path.join("../Output/" + self.dirName, "reddit_frequent_terms.png"))
 
  def dendogram_clusting(self):
    distance_matrix = pdist(self.vec_df, metric='euclidean')
    plt.figure(figsize=(25, 200))
    plt.title('Hierarchical Clustering Dendrogram') 
    dendrogram = sch.dendrogram(sch.linkage(distance_matrix, method = 'ward'),
                            orientation="right", 
                            labels=self.data_frame['Title_without_stopwords'].tolist(),
                            leaf_font_size=9
                            )
    plt.savefig(os.path.join("../Output/" + self.dirName, "reddit_dendogram.png"))
   