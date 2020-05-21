import requests
import zipfile
import pandas as pd
import graphviz
from sklearn import tree
from pandas.api.types import is_numeric_dtype

def download_file(url, local_fname):
  "Download file at URL to local directory"
  try:
    with open(local_fname, "wb") as f:
      f.write(requests.get(url).content)
  except Exception:
    print("Couldn't download file")


def unzip(fname, dest="."):
  "Unzip all files in the zip file to dest"
  with zipfile.ZipFile(fname) as f:
    f.extractall(dest)


def display_all(df):
  "helper to display large tables in the notebook"
  with pd.option_context("display.max_rows", 1000):
    with pd.option_context("display.max_columns", 1000):
      display(df)

def fill_missing(df, col, name, na_dict=None):
    if is_numeric_dtype(col):
      if pd.isnull(col).sum(): df[f'{name}_na'] = pd.isnull(col)
      if na_dict:
        df[name] = col.fillna(na_dict[name])
      else:
        df[name] = col.fillna(col.median())

def numericalize (df, col, name):
  if not is_numeric_dtype(col):
    df[name] = col.cat.codes + 1   

def process_df(df, y_field, subset=None, na_dict=None):
  if subset: df = df.sample(n=subset)
  df = df.copy()
  y = df[y_field].values
  df.drop(y_field, axis=1, inplace=True)

  for n,c in df.items():
    fill_missing(df, c, n)
    numericalize(df, c, n)
  return pd.get_dummies(df, dummy_na=True), y


def split_vals (df, n): return df[:n].copy(), df[n:].copy()

def draw_tree(dtree, df, rotate=True, filled=True, precision=3, *args):
  return graphviz.Source(tree.export_graphviz(dtree, feature_names=df.columns, rotate=rotate, filled=filled, precision=precision, *args))
