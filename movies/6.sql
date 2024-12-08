SELECT AVG(ratings.rating) FROM ratings,movies WHERE movies.year = 2012 and movies.id = ratings.movie_id;
