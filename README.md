# FilmRatings
Aineopintojen harjoitustyö: Tietokantasovellus kurssia varten tehty elokuva-arvostelu sovellus.   
    
Käyttäjä voi lisätä sovelluksen avulla elokuville pisteytyksiä (rating), sekä kirjoittaa niille kokonaisia arvosteluja (review). Sovelluksesta voi hakea myös elokuvia elokuvan nimen, ohjaajan, tai näyttelijöiden perusteella.   
[Tarkempi kuvaus aiheesta ja sovelluksen alunperin suunnitellusta toiminnallisuudesta](https://github.com/antlammi/FilmRatings/blob/master/dokumentaatio/Toiminnallisuus.md)        
[Sovellus Heroku-palvelussa](https://shielded-hamlet-29677.herokuapp.com/)      
[User Storyt](https://github.com/antlammi/FilmRatings/blob/master/dokumentaatio/userstoryt.md)      
[Informaatiota tietokannasta](https://github.com/antlammi/FilmRatings/blob/master/dokumentaatio/tietokanta.md)      
### Testitunnukset
Sovellukseen voi tällä hetkellä luoda omat tunnukset, joilla voi vapaasti käyttää kaikkea normaalikäyttäjälle sallittua toiminnallisuutta. Lisäksi on käytössä ennalta määritelty admin tili, seuraavilla tiedoilla:
        
Username: **admin**     
Password: **admin**
## Asennusohjeet
Mikäli haluaa ladata sovelluksen omalle koneelleen, herokuversion käyttämisen sijaan, onnistuu tämäkin.
Aloita kloonaamalla ensin git repositorion omalle koneelle. Tämän jälkeen tulee luoda hakemiston sisälle python virtuaaliympäristö komennolla       
        
        python3 -m venv venv

Tämän jälkeen tulee ottaa python virtuaaliympäristö käyttöön komennolla 
        
        source venv/bin/activate

Vielä tulee asentaa sovelluksen riippuvuudet ajamalla komento 

        pip install -r requirements.txt

kun viruaaliympäristö on käytössä. Tämän jälkeen sovellus on valmis käytettäväksi ja sen voi ajaa komennolla 

        python3 run.py
Nyt kun sovellus on asennettuna, voi halutessaan vilkaista [sovelluksen käyttöohjetta](https://github.com/antlammi/FilmRatings/blob/master/dokumentaatio/Käyttöohjeet.md)


