# TrendMining

Trend Mining project

## Setup

- Start by [setting up anaconda](https://www.anaconda.com/products/distribution#windows).
- Using the following command, create a conda environment named "trendMiningEnv".
  > `conda create --name trendMiningEnv`
- Activate the environment by.
  > `conda activate trendMiningEnv`
- You can close the environment by the following command.
  > `conda deactivate`
- Launch the anaconda navigator by using the following command.
  > `anaconda-navigator`
- Once anaconda-navigator is up choose the newly created `trendMiningEnv` and launch `VS Code` through the anaconda-navogator GUI.
- Install required packages by running the following command in the root of this project.
  > `pip install requirements.txt`

## Mining data

- Navigate into `Miners` directory.
- Pass the search parameters to the mining functions.
- Run the file by `python miner.py`.
- The mined and cleaned data will be, by default, saved to `Data` folder.
