### Tietokantakaavio
![tietokantakaavio](https://github.com/antlammi/FilmRatings/blob/master/dokumentaatio/Tietokantakaavio%20v3.png)
### Schema
##### Ohjaaja
  ```
  CREATE TABLE director (
    id INTEGER NOT NULL, 
    date_created DATETIME, 
    date_modified DATETIME, 
    name VARCHAR(400) NOT NULL, 
    nationality VARCHAR(400), 
    age INTEGER, 
    bio VARCHAR(1200), 
    PRIMARY KEY (id)
  );
  ```
##### Käyttäjä
  ```
  CREATE TABLE account (
    id INTEGER NOT NULL, 
    date_created DATETIME, 
    date_modified DATETIME, 
    name VARCHAR(144) NOT NULL, 
    username VARCHAR(144) NOT NULL, 
    password VARCHAR(144) NOT NULL, 
    urole VARCHAR(80) NOT NULL, 
    bio VARCHAR(1200), 
    PRIMARY KEY (id)
  );
  ```
##### Näyttelijä
  ```
  CREATE TABLE actor (
    id INTEGER NOT NULL, 
    date_created DATETIME, 
    date_modified DATETIME, 
    name VARCHAR(400) NOT NULL, 
    nationality VARCHAR(400), 
    age INTEGER, 
    bio VARCHAR(1200), 
    PRIMARY KEY (id)
  );
  ```
##### Elokuva
  ```
  CREATE TABLE film (
    id INTEGER NOT NULL, 
    date_created DATETIME, 
    date_modified DATETIME, 
    name VARCHAR(400) NOT NULL, 
    description VARCHAR(1200), 
    year INTEGER, 
    director_id INTEGER, 
    poster VARCHAR(400), 
    PRIMARY KEY (id), 
    FOREIGN KEY(director_id) REFERENCES director (id)
  );
  ```
##### Pisteytys/Arvostelu
  ```
  CREATE TABLE rating (
    user_id INTEGER NOT NULL, 
    film_id INTEGER NOT NULL, 
    date_created DATETIME, 
    date_modified DATETIME, 
    score INTEGER NOT NULL, 
    title VARCHAR(100), 
    review VARCHAR(10000), 
    PRIMARY KEY (user_id, film_id), 
    FOREIGN KEY(user_id) REFERENCES account (id), 
    FOREIGN KEY(film_id) REFERENCES film (id)
  );
  ```
##### Elokuva-Näyttelijä liitostaulu
  ```
  CREATE TABLE film_actor (
    film_id INTEGER NOT NULL, 
    actor_id INTEGER NOT NULL, 
    date_created DATETIME, 
    date_modified DATETIME, 
    PRIMARY KEY (film_id, actor_id), 
    FOREIGN KEY(film_id) REFERENCES film (id), 
    FOREIGN KEY(actor_id) REFERENCES actor (id)
  );
  ```
