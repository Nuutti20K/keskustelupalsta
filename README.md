# Keskustelupalsta

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan keskusteluja.
* Käyttäjä näkee sovellukseen lisätyt keskustelut.
* Käyttäjä pystyy etsimään keskusteluja hakusanalla.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät keskustelut.
* Käyttäjä pystyy valitsemaan keskustelulle yhden tai useamman luokittelun (esim. keskustelun aihe ja kenelle keskutelu on suunnattu).
* Käyttäjä pystyy lisäämään viestejä ja kuvia keskusteluun.

## Sovelluksen nykyinen tilanne

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään ja ulos sovelluksesta
	* Salasanassa ja tunnuksessa ei ole vielä merkki- tai pituusrajoituksia
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan keskusteluja
* Käyttäjä näkee lisätyt keskustelut
* Käyttäjä pystyy etsiä keskusteluja otsikolla
* Käyttäjä pystyy lisäämään viestejä keskusteluun
	* Viestejä voi muokata ja poistaa
 	* Viesteissä ei ole vielä päiväystä 
* Sovelluksessa on käyttäjäsivut
	* Sivuilla näkyy käyttäjän lisäämät keskustelut sekä viestien ja keskustelujen määrä
* Keskusteluille voi valita aiheluokittelun
	* Luokittelu ei vielä näy pääsivulta, vaan vasta kun keskustelu avataan

## Sovelluksen asennus

Asenna `flask` -kirjasto:

```
pip install flask
```

Luo tietokannan taulut:

```
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```

Sovelluksen voi käynnistää komennolla:

```
flask run
```
