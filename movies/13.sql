SELECT DISTINCT p.name FROM people p JOIN stars s1 ON p.id = s1.person_id JOIN movies m1 ON s1.movie_id = m1.id JOIN stars s2
ON m1.id = s2.movie_id JOIN people p2 ON s2.person_id = p2.id WHERE
 p2.name = 'Kevin Bacon'  AND p.name != 'Kevin Bacon';
