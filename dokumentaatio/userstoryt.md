- Käyttäjänä voin tarkastella listaa palveluun hiljattain lisätyistä elokuvista/arvosteluista
  - Elokuvat
  ```
    SELECT * FROM Film ORDER BY Film.date_modified desc limit 5
  ```
  - Arvostelut
  ```
    SELECT Film.name, Film.id, Account.username, Account.id, rating.score, rating.review, rating.title FROM Rating, Account,
    Film WHERE length(Rating.review) > 0 AND Rating.user_id = Account.id AND Rating.film_id = Film.id 
    ORDER BY Rating.date_modified desc limit 5
  ```

- Käyttäjänä voin tarkastella listaa parhaista tietokannasta löytyvistä elokuvista/ohjaajista/näyttelijöistä
  - Elokuvat
  ```
    SELECT name, id, avg(Rating.score) AS avg FROM Film, Rating WHERE Film.id = rating.film_id 
    GROUP BY Film.id ORDER BY avg DESC LIMIT 5
  ```
  - Ohjaajat
  ```
    SELECT director.id, director.name, AVG(Rating.score) as avg FROM Director, Rating, FILM 
    WHERE Director.id = Film.director_id AND Film.id = rating.film_id 
    GROUP BY director.id Order By avg desc LIMIT 5
  ```
  - Näyttelijät
  
   ```
    SELECT Actor.name, Actor.id, AVG(Rating.score) AS avg FROM Actor, Rating, Film_actor, Film
    WHERE Film_actor.actor_id = Actor.id AND film_actor.film_id = Film.id 
    AND Film.id = Rating.film_id GROUP BY Actor.id ORDER BY avg DESC LIMIT 5
    ```
- Käyttäjänä voin tarkastella tietokannasta löytyvien elokuvien listaa keskivertoarvioiden kanssa
  - Heroku versio
  ```
  SELECT film.id, film.name, film.year, director_id, director.name, avg(Rating.score) AS avg FROM Director, Film 
  LEFT JOIN Rating on Rating.film_id = id WHERE Director.id = film.director_id 
  GROUP BY Film.id, director.name ORDER BY film.id
  ```
  - Lokaali versio
  ```
  SELECT film.id, film.name, film.year, director_id, director.name, avg(Rating.score) AS avg FROM Director, Film 
  LEFT JOIN Rating on Rating.film_id = film.id WHERE Director.id = film.director_id 
  GROUP BY Film.id, director.name ORDER BY film.id
  ```
  - Tämän listan voi järjestää nimen, ohjaajan nimen, julkaisuvuoden tai keskivertoarvion perusteella (tehdään pythonilla)
  
- Käyttäjänä voin tarkastella yksittäisen elokuvan tietoja
  - Elokuvan tiedot
  ```
    SELECT * FROM Film WHERE id = :id
  ```
  - Elokuvaan liittyvät arvostelut
  ```
    SELECT Rating.user_id, Rating.score, Rating.title, Account.username FROM Rating, Account 
    WHERE length(Rating.review) > 0 AND Account.id = Rating.user_id AND Rating.film_id = :id
  ```
  - Elokuvan pisteytysten määrä
  ```
  SELECT Count(*) from Rating LEFT JOIN Film ON Rating.film_id = Film.id WHERE Film.id = :id
  ```
  - Elokuvan pisteytysten keskiarvo
  ```
  SELECT AVG(Rating.score) from Rating LEFT JOIN Film ON Rating.film_id = Film.id WHERE Film.id = :id
  ```
  - Elokuvan näyttelijät
  ```
  SELECT * FROM FilmActor WHERE film_id = :id
  ```
    (Pythonilla tehty for loop jokaiselle edellisen kyselyn id:lle, jossa seuraava kysely)
  ```
  SELECT * ACTOR WHERE id = :id 
  ```
- Käyttäjänä voin tarkastella tietokannasta löytyvien ohjaajien listaa
  ```
    SELECT * FROM Director
  ```
  - Tämän listan voi järjestää nimen, kansallisuuden tai iän perusteella (tehdään pythonilla)
  
- Käyttäjänä voin tarkastella yksittäisen ohjaajan tietoja
  - Ohjaajan tiedot
  ```
    SELECT * FROM Director where id = :id
  ```
  - Ohjaajan keskivertopisteytys
  ```
  SELECT AVG(Rating.score) from Rating LEFT JOIN Film ON Rating.film_id = Film.id
  WHERE Film.director_id = :id"
   ```
   - Ohjaajan elokuvat
   ```
   SELECT * FROM FILM WHERE Director_id = :id
   ```
- Käyttäjänä voin tarkastella tietokannasta löytyvien näyttelijöiden listaa
```
  SELECT * FROM Actor
```
  - Tämän listan voi järjestää nimen, kansallisuuden tai iän perusteella (tehdään pythonilla)

- Käyttäjänä voin tarkastella yksittäisen näyttelijän tietoja
  - Näyttelijän tiedot
  ```
    SELECT * FROM Actor where id=:id
  ```
  - Näyttelijän keskivertopisteytys
  ```
  SELECT AVG(Rating.score) FROM Rating 
  LEFT JOIN Film on Rating.film_id = film.id 
  LEFT JOIN film_actor on film_actor.film_id = film.id
  WHERE film_actor.actor_id = :id
  ```
  - Näyttelijän elokuvat
  ```
  SELECT * FROM FilmActor WHERE user_id = :id
  ```
  (for loop edellisen kyselyn tuloksille)
  ```
  SELECT * FROM Film WHERE id = :id
  ```
- Käyttäjänä voin tarkastella tietokannasta löytyvien arvosteluiden listaa
  ```
  SELECT Film.name, Film.id, Account.username, Account.id, rating.score, rating.title FROM Rating, Account, Film
  WHERE length(Rating.review) > 0 AND Rating.user_id = Account.id AND Rating.film_id = Film.id
  ```
  - Tämän listan voi järjestää elokuvan nimen, pisteytyksen, käyttäjän nimen, tai arvostelun otsikon perusteella(pythonilla)

- Käyttäjänä kykenen tarkastelemaan muiden rekisteröityneiden käyttäjien profiileja
  ```
    SELECT * FROM Account WHERE id = :id
  ```
  - Profiilista löytyy kyseisen käyttäjän kuvaus (tulee ylemmän kyselyn mukana)
  
  - Profiilista löytyy kyseisen käyttäjän suosikkielokuvat
  ```
  SELECT Film.name, Film.id, Rating.score AS avg FROM Rating, Film, Account
  WHERE Film.id = Rating.film_id AND Rating.user_id = Account.id AND Account.id = :id ORDER BY avg DESC LIMIT 5
  ```
  - Profiilista löytyy kyseisen käyttäjän suosikkinäyttelijät
  ```
  SELECT Actor.name, Actor.id, AVG(Rating.score) AS avg FROM Actor, Rating, Film_actor, Film, Account
  WHERE Film_actor.actor_id = Actor.id AND film_actor.film_id = Film.id
  AND Film.id = Rating.film_id AND Rating.user_id = Account.id AND Account.id = :id
  GROUP BY Actor.id ORDER BY avg DESC LIMIT 5
  ```
  - Profiilista löytyy kyseisen käyttäjän suosikkiohjaajat
  ```
  SELECT Director.name, Director.id, AVG(Rating.score) AS avg FROM Director, Rating, Film, Account 
  WHERE Director.id = Film.director_id AND Film.id = Rating.film_id AND Rating.user_id = Account.id AND Account.id = :id 
  GROUP BY Director.name, Director.id ORDER BY avg DESC LIMIT 5
  ```
  - Profiilista löytyy kyseisen käyttäjän arvostelut
  ```
  SELECT Film.name, Film.id, Account.username, Account.id, rating.score, rating.review, rating.title 
  FROM Rating, Account, Film
  WHERE length(Rating.review) > 0 AND Rating.user_id = Account.id AND Rating.film_id = Film.id AND Account.id = :id 
  ORDER BY Rating.date_modified DESC
  ```
  
- Käyttäjänä voin rekisteröityä palveluun
```
INSERT INTO Account (name, username, password, urole) VALUES (?, ?, ?, "DEFAULT")
```
- Käyttäjänä voin kirjautua sisään
```
SELECT * FROM Account WHERE username = ? AND password = ?
```
- Käyttäjänä voin kirjautua ulos
```
SELECT * FROM Account WHERE username = ? AND password = ?
```
- Sisäänkirjautuneena käyttäjänä kykenen lisäämään elokuvalle pisteytyksen tai arvostelun
```
INSERT INTO Rating (film_id, user_id, score, title, review) VALUES (?, current_user.id, ?, ?, ?)
```
- Sisäänkirjautuneena käyttäjänä kykenen tarkastelemaan omia pisteytyksiäni ja arvostelujani
```
SELECT Film.name, Film.id, Account.username, Account.id, rating.score, rating.review, rating.title FROM Rating, Account, Film
WHERE Rating.user_id = Account.id AND Rating.film_id = Film.id AND Account.id = :id
```
- Sisäänkirjautuneena käyttäjänä kykenen muokkaamaan tai poistamaan antamiani pisteytyksiä/arvosteluita
```
UPDATE Rating SET score = ?; title = ?, review = ? WHERE id = ?
```
- Sisäänkirjautuneena käyttäjänä pystyn muokkaamaan omaa kuvausta, nimeä tai usernamea
```
UPDATE Account set name = ?, username = ?, bio = ? WHERE id = ?
```
- Sisäänkirjautuneena käyttäjänä pystyn muuttamaan salasanaani
```
UPDATE ACCOUNT set password = ? WHERE ID = ?
```
- Admin-käyttäjänä kykenen lisäämään tietokantaan elokuvia/ohjaajia/näyttelijöitä
  - Elokuvat
  ```
  INSERT INTO Film (name, description, director_id, year, poster) VALUES (?, ?, ?, ?, ?)  
  ```
  - Ohjaajat
  ```
  INSERT INTO Director(name, bio, age, nationality) VALUES (?, ?, ?, ?)  
  ```
  - Näyttelijät
  ```
  INSERT INTO Actor(name, bio, age, nationality) VALUES (?, ?, ?, ?)  
  ```
- Admin-käyttäjänä kykenen muokkaamaan tietokannasta löytyviä elokuvia/ohjaajia/näyttelijöitä
  - Elokuvat
  ```
  UPDATE Film SET name=?, description=?, director_id = ?, year = ?, poster = ? WHERE ID = ?
  ```
  - Ohjaajat
  ```
  UPDATE Director SET name=?, bio=?, nationality = ?, age = ? WHERE ID = ?
  ```
  - Näyttelijät
  ```
  UPDATE Actor SET name=?, bio=?, nationality = ?, age = ? WHERE ID = ?
  ```
- Admin-käyttäjänä kykenen poistamaan tietokannasta löytyviä elokuvia/ohjaajia/näyttelijöitä
  - Elokuvat
  ```
  DELETE FROM Film WHERE ID = ?
  ```
  - Ohjaajat
   ```
  DELETE FROM Director WHERE ID = ?
  ```
  - Näyttelijät
  ```
  DELETE FROM Actor WHERE ID = ?
  ```

- Admin-käyttäjänä kykenen tarkastelemaan kaikkien palvelussa annettujen pisteytysten listaa

  ```
  SELECT Film.name, Film.id, Account.username, Account.id, rating.score, rating.review, rating.title 
  FROM Rating, Account, Film
  WHERE Rating.user_id = Account.id AND Rating.film_id = Film.id
  ```
  
- Admin-käyttäjänä kykenen poistamaan minkä tahansa palveluun lisätyn pisteytyksen
  ```
  DELETE From Rating WHERE User_id = ? AND Film_id = ?
  ```
