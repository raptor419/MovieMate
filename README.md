# MovieMate

MovieMate is a Django Movie Recommender System Webapp using Matrix Factorization

## Deploying
```bash
git clone https://github.com/raptor419/moviemate.git
mondgodb/bin/mongod --dbpath ./mondgodb/bin/mongod/data/
source venv/bin/activate
python manage.py runserver
```

## Algorithm
We choose to use Matrix Factorization Method
### Matrix Factorization  
K in the problem statement is dynamic in our usecase, i.e it changes according to no of movies rates and alogrithms starts working from the first movie rated by the user

### Web scraping
Done using bs4  
To webscrape MovieLens Small Dataset
```bash
python scrape.py
```
To webscrape IMDb Top 250
```bash
python scrape-small.py
```
Currently we are using IMDb Top 250 for testing purposes, but MovieLens Dataset can be used too.
Though it is not optimal.

## Usage

Login using App user credentials, rate movies and get recommendations

### App User Details
Usernames:  
1,2,3  
Password for all:   
1password

### Django Superuser Details  
username: admin  
password: 1aaaaa1  

## Acknowledgements
The following tools are used to develop the Webapp which made such a rapid development possible.  
[Djongo](https://github.com/nesdis/djongo)  
[pyCollaborativeFiltering](https://github.com/ChangUk/pyCollaborativeFiltering) (though it is not deployed in the webapp)

