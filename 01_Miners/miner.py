from stackoverflow.mine_stackoverflow import  mine_stackoverflow_data
from reddit.mine_reddit import mine_reddit_data
from scopus.mine_scopus import mine_scopus_data

# Mine Stackoverflow data
# Pass the search string to the function
mine_stackoverflow_data('machine learning')

# Mine Reddit data
# Pass the subreddit to mine (without spaces)
mine_reddit_data("MachineLearning")

# Mine Scopus data
# Pass the query string
# Make sure you are connected to university VPN
mine_scopus_data("TITLE(machine learning) AND PUBYEAR > 2021")