

CREATE TABLE ASIAKAS(
asiakas_ID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
yritys_nimi VARCHAR(64),
sahkoposti VARCHAR(64),
puhelinnumero INTEGER,
kaupunki VARCHAR(64),
katu VARCHAR(64), 
postinumero int  
);

CREATE TABLE TUOTTEET(
tuotenumero INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
nimi VARCHAR(64),
hinta INTEGER
);

CREATE TABLE TILAUKSEN_TASMAYS(
tilausnumero INTEGER,
tuotenumero INTEGER,
maara INTEGER,
PRIMARY KEY (tilausnumero ,tuotenumero),
FOREIGN KEY (tilausnumero) REFERENCES TILAUS(tilausnumero)
ON UPDATE RESTRICT ON DELETE RESTRICT,
FOREIGN KEY (tuotenumero) REFERENCES TUOTTEET(tuotenumero)
ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE TILAUS(
tilausnumero INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
asiakas_ID INTEGER,
tilaus_pvm DATE NOT NULL DEFAULT CURRENT_DATE,
tilauksen_tila VARCHAR(64) DEFAULT'Käsittelyssä',
FOREIGN KEY (asiakas_ID) REFERENCES ASIAKAS(asiakas_ID)
ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE LASKU(
laskunumero INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
tilausnumero INTEGER UNIQUE,
summa INTEGER,
alv INTEGER NOT NULL DEFAULT 24,
tilinumero varchar(64) DEFAULT 'fi3500010001',
viitenumero INTEGER UNIQUE,
lasku_pvm DATE NOT NULL DEFAULT CURRENT_DATE,
lasku_erapvm DATE NOT NULL DEFAULT CURRENT_DATE, 
FOREIGN KEY (tilausnumero) REFERENCES TILAUS(tilausnumero)
ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE MYYNTIRESKONTRA(
asiakas_ID INTEGER NOT NULL,
laskunumero INTEGER NOT NULL,
saldo INTEGER,
laskutila VARCHAR(64) DEFAULT 'AVOIN',
PRIMARY KEY (asiakas_ID, laskunumero),
FOREIGN KEY (asiakas_ID) REFERENCES ASIAKAS(asiakas_ID)
ON UPDATE RESTRICT ON DELETE RESTRICT,
FOREIGN KEY (laskunumero) REFERENCES LASKU(laskunumero)
ON UPDATE RESTRICT ON DELETE RESTRICT
);

CREATE TABLE KIRJANPITO(
tositenumero INTEGER PRIMARY KEY  AUTOINCREMENT NOT NULL,
laskunumero INTEGER,
tili VARCHAR(64),
kirjaus_pvm DATE NOT NULL DEFAULT CURRENT_DATE,
FOREIGN KEY (laskunumero) REFERENCES LASKU(laskunumero)
ON UPDATE RESTRICT ON DELETE RESTRICT);

CREATE TABLE PERINTA(
perintanumero INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
laskunumero INTEGER,
korko INTEGER DEFAULT 10,
perinta_pvm DATE NOT NULL DEFAULT CURRENT_DATE,
FOREIGN KEY (laskunumero) REFERENCES MYYNTIRESKONTRA(laskunumero)
ON UPDATE RESTRICT ON DELETE RESTRICT
);

INSERT INTO TUOTTEET(nimi,hinta)
SELECT 'Banaani' AS nimi, 1 AS hinta 
UNION ALL SELECT 'Omena',5
UNION ALL SELECT 'Hilavitkutin',10
UNION ALL SELECT 'Pikku-Piru',666
UNION ALL SELECT 'Lettuja',4
UNION ALL SELECT 'Avaruusraketti',9999999
UNION ALL SELECT 'simapullo',0
UNION ALL SELECT 'Lettuja',22
UNION ALL SELECT 'Lettuja',44
UNION ALL SELECT 'Lettuja',543
UNION ALL SELECT 'Lettuja',6;

INSERT INTO ASIAKAS(yritys_nimi,sahkoposti, puhelinnumero,kaupunki,katu,postinumero)
SELECT 	'metapaja' AS yritys_nimi, 'pomo@metapaja.fi' AS sahkoposti, 04066644433 AS puhelinnumero, 'HELSINKI' AS kaupunki, 'Yliopistokatu', 00100 AS postinumero
UNION ALL SELECT 'Pikkufirma','heebo@pikkufirma.fi',09087687676,'TAMPERE','Duunarikatu 20',12321
UNION ALL SELECT 'isofirma','iso@isofirma.fi',09063411676,'TURKU','Porvarikatukatu',40505
UNION ALL SELECT 'firma','tj@firma.fi',34536756757,'TAMPERE','Duunarikatu 29',12321
UNION ALL SELECT 'Matin_tmi','matti@vaan.fi',000000000,'TAMPERE','Duunarikatu 19',00321
UNION ALL SELECT 'firma','tj@firma.fi',00536759751,'TAMPERE','Duunarikatu 19',12321
UNION ALL SELECT 'firma','tj@firma.fi',33847526757,'TAMPERE','Duunarikatu 66',18821
UNION ALL SELECT 'EVIL CORP','puhdas@pahuus.fi',896654527,'HELSINKI','koyhatkyykkyynkatu 666',66666;



INSERT INTO TILAUS(asiakas_ID)
SELECT 1 AS asiakas_ID
UNION ALL SELECT 2
UNION ALL SELECT 3
UNION ALL SELECT 4
UNION ALL SELECT 5
UNION ALL SELECT 6;

INSERT INTO TILAUKSEN_TASMAYS(tilausnumero,tuotenumero,maara)
SELECT 1 AS tilausnumero, 6 AS tuotenumero, 1 AS maara
UNION ALL SELECT 1,2,3
UNION ALL SELECT 2,2,4
UNION ALL SELECT 2,3,5
UNION ALL SELECT 3,4,1
UNION ALL SELECT 3,5,1
UNION ALL SELECT 4,5,2
UNION ALL SELECT 5,4,1
UNION ALL SELECT 5,5,10
UNION ALL SELECT 6,5,2;

 
INSERT INTO LASKU(tilausnumero,summa,viitenumero)
SELECT 1 AS tilausnumero, SUM(TUOTTEET.hinta), 10001
FROM TILAUS JOIN TILAUKSEN_TASMAYS ON TILAUS.tilausnumero = TILAUKSEN_TASMAYS.tilausnumero JOIN TUOTTEET ON TILAUKSEN_TASMAYS.tuotenumero =TUOTTEET.tuotenumero
WHERE TILAUKSEN_TASMAYS.tilausnumero = 1;

INSERT INTO LASKU(tilausnumero,summa,viitenumero)
SELECT 2 AS tilausnumero, SUM(TUOTTEET.hinta), 10002
FROM TILAUS JOIN TILAUKSEN_TASMAYS ON TILAUS.tilausnumero = TILAUKSEN_TASMAYS.tilausnumero JOIN TUOTTEET ON TILAUKSEN_TASMAYS.tuotenumero =TUOTTEET.tuotenumero
WHERE TILAUKSEN_TASMAYS.tilausnumero = 2;

INSERT INTO LASKU(tilausnumero,summa,viitenumero)
SELECT 3 AS tilausnumero, SUM(TUOTTEET.hinta), 10003
FROM TILAUS JOIN TILAUKSEN_TASMAYS ON TILAUS.tilausnumero = TILAUKSEN_TASMAYS.tilausnumero JOIN TUOTTEET ON TILAUKSEN_TASMAYS.tuotenumero =TUOTTEET.tuotenumero
WHERE TILAUKSEN_TASMAYS.tilausnumero = 3;

INSERT INTO LASKU(tilausnumero,summa,viitenumero)
SELECT 4 AS tilausnumero, SUM(TUOTTEET.hinta), 10004
FROM TILAUS JOIN TILAUKSEN_TASMAYS ON TILAUS.tilausnumero = TILAUKSEN_TASMAYS.tilausnumero JOIN TUOTTEET ON TILAUKSEN_TASMAYS.tuotenumero =TUOTTEET.tuotenumero
WHERE TILAUKSEN_TASMAYS.tilausnumero = 4;

INSERT INTO LASKU(tilausnumero,summa,viitenumero)
SELECT 5 AS tilausnumero, SUM(TUOTTEET.hinta), 10005
FROM TILAUS JOIN TILAUKSEN_TASMAYS ON TILAUS.tilausnumero = TILAUKSEN_TASMAYS.tilausnumero JOIN TUOTTEET ON TILAUKSEN_TASMAYS.tuotenumero =TUOTTEET.tuotenumero
WHERE TILAUKSEN_TASMAYS.tilausnumero = 5;

INSERT INTO LASKU(tilausnumero,summa,viitenumero)
SELECT 6 AS tilausnumero, SUM(TUOTTEET.hinta), 10006
FROM TILAUS JOIN TILAUKSEN_TASMAYS ON TILAUS.tilausnumero = TILAUKSEN_TASMAYS.tilausnumero JOIN TUOTTEET ON TILAUKSEN_TASMAYS.tuotenumero =TUOTTEET.tuotenumero
WHERE TILAUKSEN_TASMAYS.tilausnumero = 6;

INSERT INTO MYYNTIRESKONTRA(asiakas_ID,laskunumero,saldo)
SELECT TILAUS.asiakas_ID, LASKU.laskunumero, LASKU.summa
FROM LASKU JOIN TILAUS ON LASKU.tilausnumero = TILAUS.tilausnumero 
WHERE LASKU.laskunumero = 1 ;

INSERT INTO MYYNTIRESKONTRA(asiakas_ID,laskunumero,saldo)
SELECT TILAUS.asiakas_ID, LASKU.laskunumero, LASKU.summa
FROM LASKU JOIN TILAUS ON LASKU.tilausnumero = TILAUS.tilausnumero 
WHERE LASKU.laskunumero = 2 ;

INSERT INTO MYYNTIRESKONTRA(asiakas_ID,laskunumero,saldo)
SELECT TILAUS.asiakas_ID, LASKU.laskunumero, LASKU.summa
FROM LASKU JOIN TILAUS ON LASKU.tilausnumero = TILAUS.tilausnumero 
WHERE LASKU.laskunumero = 3 ;

INSERT INTO MYYNTIRESKONTRA(asiakas_ID,laskunumero,saldo)
SELECT TILAUS.asiakas_ID, LASKU.laskunumero, LASKU.summa
FROM LASKU JOIN TILAUS ON LASKU.tilausnumero = TILAUS.tilausnumero 
WHERE LASKU.laskunumero = 4 ;

INSERT INTO MYYNTIRESKONTRA(asiakas_ID,laskunumero,saldo)
SELECT TILAUS.asiakas_ID, LASKU.laskunumero, LASKU.summa
FROM LASKU JOIN TILAUS ON LASKU.tilausnumero = TILAUS.tilausnumero 
WHERE LASKU.laskunumero = 5 ; 

INSERT INTO MYYNTIRESKONTRA(asiakas_ID,laskunumero,saldo)
SELECT TILAUS.asiakas_ID, LASKU.laskunumero, LASKU.summa
FROM LASKU JOIN TILAUS ON LASKU.tilausnumero = TILAUS.tilausnumero 
WHERE LASKU.laskunumero = 6 ;


CREATE TRIGGER PAIVITA_STATUS_OK AFTER UPDATE OF saldo ON MYYNTIRESKONTRA 
BEGIN
UPDATE MYYNTIRESKONTRA SET laskutila = 'MAKSETTU' WHERE saldo =0;
END;

CREATE TRIGGER KIRJAUS AFTER UPDATE OF laskutila ON MYYNTIRESKONTRA
WHEN NEW.laskutila ='MAKSETTU'
BEGIN
INSERT INTO KIRJANPITO(laskunumero,tili) 
SELECT MYYNTIRESKONTRA.laskunumero, '3000_MYYNTI' AS tili
FROM MYYNTIRESKONTRA
WHERE laskutila = 'MAKSETTU';
END;

CREATE TRIGGER POISTA_1 AFTER INSERT ON KIRJANPITO 
BEGIN 
DELETE FROM MYYNTIRESKONTRA WHERE laskutila ='MAKSETTU';
END;

CREATE TRIGGER KARHUA AFTER UPDATE OF laskutila ON MYYNTIRESKONTRA
WHEN NEW.laskutila ='MYÖHÄSSÄ'
BEGIN
INSERT INTO PERINTA(laskunumero) 
SELECT laskunumero
FROM MYYNTIRESKONTRA
WHERE laskutila = 'MYÖHÄSSÄ';
END;

CREATE TRIGGER POISTA_2 AFTER INSERT ON PERINTA 
BEGIN 
DELETE FROM MYYNTIRESKONTRA WHERE laskutila ='MYÖHÄSSÄ';
END;

CREATE TRIGGER LASKU  AFTER INSERT ON TILAUS 
BEGIN 
DELETE FROM MYYNTIRESKONTRA WHERE laskutila ='MYÖHÄSSÄ';
END;

CREATE INDEX LASKU_IND ON LASKU(laskunumero);
CREATE INDEX TILAUS_IND ON TILAUS(tilausnumero)


