# Keskustelusovellus

Sovelluksen ominaisuudet:

Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.

Sovelluksen etusivulla näkyy lankoja eri aiheista. Käyttäjä voi lisätä kommentin lankaan.

Jokaisella langalla on otsikko ja aihe. Lisäksi langassa voi olla tekstiä, linkki tai kuva.

Käyttäjä voi äänestää lankoja sekä kommentteja ylös tai alas.

Käyttäjä voi muokata oman langan tai kommentin sisältöä.

Käyttäjä voi etsiä lankoja tai kommentteja annetun sanan perusteella. Lankoja voi myös etsiä aiheittain.

Ylläpitäjä voi poistaa lankoja sekä kommentteja.

# Toteutetut ominaisuudet:
Langat ja kommentit, kuvan lisääminen lankaan, aiheet.

Tavallisen käyttäjän tunnuksen luominen sekä sisäänkirjautuminen ja uloskirjautuminen.

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
