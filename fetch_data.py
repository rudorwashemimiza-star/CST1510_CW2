from pathlib import Path

import pandas as pd 

import requests

URL = "https://api.github.com/orgs/python/repos"
PARAMS = {"per_page" : 100}
RAW_FILE = Path("DATA/raw.csv")

STORE = ["name", "language","size","forks_count","stargazers_count", "updated_at","created_at", "open_issues_count"]
RENAME = {"stargazers_count": "stars", "forks_count":"forks",
          "open_issues_count": "open_issues", "created_at": "date_created","updated_at": "date_updated"}
REQUIRED =["name", "language"]


def get_data(url,params):
     """Gets data from an API and returns the json response.""" 
     try:
         result = requests.get(url, params = params , timeout=30)
         result.raise_for_status()
         return result.json()
     except requests.RequestException as error:
          print("Could not access the data", error)
          return None



def make_table(data, record_key):
     """Converts the API data into a pandas table"""
     records = data[record_key] if record_key else data 
     return pd.json_normalize(records, sep="_")

def tidy_data(df):
     """Renames, selects and cleans the columns"""
     df = df[STORE]
     df = df.rename(columns=RENAME)
     df = df.dropna(subset=REQUIRED)
     return df



def save_data(df,path):
     """Saves the cleaned table as a csv file"""
     path.parent.mkdir(exist_ok=True)
     df.to_csv(path,index=False)
     print(f"Saved {len(df)} rows to {path}")

if __name__ == "__main__":
     data = get_data(URL,PARAMS)

     if data is not None:
          table = make_table(data, None)
          table = tidy_data(table)
          print(table.head())
          save_data(table, RAW_FILE)
          

    