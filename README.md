# Keskustelusovellus

Sovelluksen ominaisuudet:

Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.

Sovelluksen etusivulla näkyy lankoja eri aiheista. Käyttäjä voi lisätä kommentin lankaan.

Jokaisella langalla on otsikko ja aihe. Lisäksi langassa voi olla tekstiä tai kuva.

Käyttäjillä on profiilit jossa näkyy käyttäjän langat ja kommentit.

Aiheita voi seurata. Omat sivulla näkyy lankoja käyttäjän seuraamilta aiheilta.

# Käynnistysohjeet
Kloona repositiorio ja luo kansioon .env tiedosto jonka sisältö on seuraavanlainen:

`DATABASE_URL=<tietokannan-paikallinen-osoite>`

`SECRET_KEY=<salainen-avain>`

Aktivoi virtuaaliympäristö ja asenna riippuvuudet komennoilla

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r ./requirements.txt`

Määritä tietokannan skeema komennolla

`psql < schema.sql`

Käynnistä sovellus komennolla

`flask run`.
