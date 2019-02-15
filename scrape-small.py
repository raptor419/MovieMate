import json
import requests
import zipfile
import csv
import pymongo
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from bson.binary import Binary
# from recommend.models import UserRating, Movie
from gridfs import GridFS
import base64

top250links = 'top250links.txt'

def scrape_movie(movielink, debug=False):
    print(movielink)
    moviepage = requests.get(movielink[:-1])
    print(movielink[-9:-2])
    movieid = movielink[-9:-2]
    soup = bs(moviepage.content, 'html.parser')
    print(soup.select(".title_wrapper h1"))
    titlenyear = soup.select(".title_wrapper h1")[0].text
    movietitle = titlenyear[0:len(titlenyear) - 8]
    movieyear = titlenyear[len(titlenyear) - 6:len(titlenyear) - 2]
    moviecoverurl = soup.select(".poster img")[0]['src']
    moviecover = requests.get(moviecoverurl).content
    movierating = soup.select(".ratingValue span")[0].text
    metascore = soup.select(".metacriticScore")
    metascore = metascore[0].text.strip() if metascore else None
    movielength = soup.select(".subtext time")[0].text.strip()
    genresndate = [i.text for i in soup.select(".subtext a")]
    releasedate = genresndate[-1].strip()
    genreslist = genresndate[:-1]
    print(genreslist)
    moviegenres = ""
    for x in range(len(genresndate) - 1):
        moviegenres = moviegenres + ',' + genresndate[x]
    moviegenres = moviegenres[1:]
    moviedesc = soup.select(".summary_text")[0].text.strip()

    if debug:
        print("Title: " + movietitle)
        print("IMDB Rating: " + movierating + "/10")
        if metascore: print("Metascore: " + metascore + "/100")
        print("Length: " + movielength)
        print("Year: " + movieyear)
        print("Genre: " + moviegenres)
        print("Description: " + moviedesc)
        print("Release date: " + releasedate)
        print("Summary: " + moviedesc)

    data = dict()
    data['imdb_id'] = movieid
    data['title'] = movietitle
    data['year'] = movieyear
    data['movie_logo'] = movieid+'.jpg'
    with open('./media/'+data['movie_logo'],'wb') as f:
        f.write(moviecover)
    data['imdb_rating'] = float(movierating)
    # data['metascore'] = metascore
    # data['length'] = movielength
    data['release_date'] = releasedate
    data['genre'] = moviegenres
    data['summary'] = moviedesc
    return data


def scrape(a=0):
    db = connect_to_db()
    with open(top250links, "r") as file:
        lines = file.readlines()
    for i in range(len(lines)):
        data = scrape_movie(lines[i])
        data['_id'] = int(i+1)
        data['id'] = int(i+1)
        # djmovie = Movie(
        #     _id=data['_id'],
        #     imdb_id=data['imdb_id'],
        #     year=data['year'],
        #     title=data['title'],
        #     movie_logo=data['cover'],
        #     genres=data['genres'],
        #     imdb_rating=data['imdb_rating'],
        #     release_date=data['release_date']
        # )
        # djmovie.save()
        print(i, data['imdb_id'], data['title'])
        save(db, data)

def outmovie():
    with open(top250links, "r") as file:
        lines = file.readlines()
    with open("ml-latest-small/smallmovie.csv",'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['imdbId'])
        for line in lines:
            print(line[-9:-2])
            writer.writerow([int(line[-9:-2])])
    csvfile.close()
    


def connect_to_db():
    client = MongoClient('localhost', 27017)
    db = client['moviedbsmall']
    return db


def save(db, data):
    coll = db.recommend_movie
    ent_id = coll.insert_one(data)
    print(ent_id)

scrape()
# outmovie()

