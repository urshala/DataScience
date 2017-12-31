import pandas as pd 
import numpy 

#read each file
unames = ['user_id', 'gender', 'age', 'occupation', 'zip']
users = pd.read_table('users.dat', sep='::', header=None, names=unames, engine='python')

rnames = ['user_id', 'movie_id', 'rating', 'timestamp']
ratings = pd.read_table('ratings.dat', sep='::', header=None, names=rnames, engine='python')

mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('movies.dat', sep='::', header=None, names=mnames, engine='python')


#Merge all the data
data = pd.merge(pd.merge(ratings, users), movies)

mean_ratings = data.pivot_table('rating', index='genres', columns='gender', aggfunc='mean')

#Top 20 genres for female users
top_genre_for_female = mean_ratings.sort_values('F', ascending=False)[:21]
print(top_genre_for_female)

#Top 20 genres for male users
top_genre_for_male = mean_ratings.sort_values('M', ascending=False)[:21]
print(top_genre_for_male)

# 20	 movie	 categories	 in	 terms	 of	 greatest disagreement among viewers,independent of	gender
ratings_by_genre = data.groupby('genres').size() 
active_genres = ratings_by_genre.index[ratings_by_genre >= 100]

rating_std_by_genre = data.groupby('genres')['rating'].std()
rating_std_by_genre = rating_std_by_genre.ix[active_genres] 
rating_std_by_genre.sort_values(ascending=False) 

print(rating_std_by_genre[:21])
