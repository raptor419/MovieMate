import pandas as pd

links = pd.read_csv("links.csv")
ratings = pd.read_csv("ratings.csv")
small = pd.read_csv("smallmovie.csv")
result = pd.merge(links,ratings,on=['movieId'])
final = pd.merge(result,small,how='inner',on=['imdbId'])
final = final[['userId','movieId','rating']]
print(final.nunique())
final.to_csv("out.csv")