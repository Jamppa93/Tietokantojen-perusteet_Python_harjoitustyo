import sys
import time
import sqlite3
import bokeh

from bokeh.io import show, output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

####################################################################
#PANEELIT
####################################################################

def main_panel():
    print("******************************************")
    print("PARAS KAIKISTA- Myyntireskontra 2000")
    print("******************************************")
    print("1) HAE TIETOA")
    print("2) PÄIVITÄ LASKUN TILA")
    print("3) LISÄÄ TIETOJA")
    print("4) VISUALISOI TILAUSKANTA")
    print("0) POISTU OHJELMASTA")
    return int(input("ANNA VALINTASI: "))

def search_panel():
    print("******************************************")
    print("HAKUVAIHTOEHDOT")
    print("******************************************")
    print("1) HAE KAIKKI TILAUKSET")
    print("2) HAE KAIKKI LASKUT")
    print("3) HAE KAIKKI YRITYKSET")
    print("4) HAE MAKSETUT JA ERÄÄNTYNEET LASKUT")
    print("5) TARKASTA SALDOTILANNE")
    print("6) TULOSTA TUOTTEET")
    print("0) PALAA PÄÄOHJELMAAN.")
    return int(input("ANNA VALINTASI: "))

def update_panel():
    print("******************************************")
    print("TIETOJEN PÄIVITYS")
    print("******************************************")
    print("1) KIRJAA MYYNTILASKU MAKSETUKSI")
    print("2) KIRJAA MYYNTILASKU ERÄÄNTYNEEKSI")
    print("0) PALAA PÄÄOHJELMAAN")
    return int(input("ANNA VALINTASI: "))

def add_panel():
    print("******************************************")
    print("TIETOJEN LISÄYS")
    print("******************************************")
    print("1) LISÄÄ YRITYS YRITYSKANTAAN")
    print("2) LISÄÄ TUOTTEITA MYYTÄVÄKSI")
    print("3  LISÄÄ TILAUS JA LASKU TIETOKANTAAN")
    print("0) PALAA PÄÄOHJELMAAN")
    return int(input("VALINTASI: "))

####################################################################
#HAUT
####################################################################
def search():
    while True:
        ans = search_panel()
        if ans == 1:
            query_1_()
        elif ans == 2:
            query_2_()
        elif ans == 3:
            query_3_()
        elif ans == 4:
            query_4_()
        elif ans == 5:
            query_5_()
        elif ans == 6:
            query_6_()
        elif ans == 0:
            print("PALATAAN PÄÄOHJELMAAN.")
            time.sleep(1)
            return
        else:
            continue

def query_1_():
    cursor = collector()
    table_1 = cursor.execute('SELECT TILAUS.tilausnumero,ASIAKAS.yritys_nimi,TILAUS.tilaus_pvm, TILAUS.tilauksen_tila\
                            FROM TILAUS  JOIN ASIAKAS ON TILAUS.asiakas_ID = ASIAKAS.asiakas_ID;')
    names = list(map(lambda x: x[0], table_1.description))
    table_1 = table_1.fetchall()
    print(names)
    printer(table_1)
    return

def query_2_():
    cursor = collector()
    table_2 = cursor.execute('SELECT ASIAKAS.asiakas_ID, LASKU.*, MYYNTIRESKONTRA.laskutila  FROM LASKU JOIN TILAUS ON LASKU.tilausnumero = TILAUS.tilausnumero\
                                 JOIN ASIAKAS ON TILAUS.asiakas_ID = ASIAKAS.asiakas_ID  JOIN MYYNTIRESKONTRA ON LASKU.laskunumero = MYYNTIRESKONTRA.laskunumero;')
    names = list(map(lambda x: x[0], table_2.description))
    table_2 = table_2.fetchall()
    print("")
    print(names)
    printer(table_2)
    return

def query_3_():
    cursor = collector()
    table_3 = cursor.execute('SELECT "YRITYS NRO:" AS selite_1, ASIAKAS.asiakas_ID, ASIAKAS.yritys_nimi, ASIAKAS.sahkoposti FROM ASIAKAS;')
    names = list(map(lambda x: x[0], table_3.description))
    table_3 = table_3.fetchall()
    print(names)
    printer(table_3)
    return

def query_4_():
    cursor = collector()
    print("SAADUT MAKSUT MYYNTILASKUISTA:") 
    table_info_paid = cursor.execute('SELECT KIRJANPITO.*, LASKU.summa FROM KIRJANPITO JOIN LASKU ON KIRJANPITO.laskunumero = LASKU.laskunumero;')
    names = list(map(lambda x: x[0], table_info_paid.description))
    table_info_paid = table_info_paid.fetchall()
    print(names)
    printer(table_info_paid)
    print("")
    print("ERÄÄNTYNEET  MYYNTILASKUT:")
    table_info_unpaid = cursor.execute('SELECT PERINTA.*, LASKU.summa FROM  PERINTA JOIN LASKU ON PERINTA.laskunumero = LASKU.laskunumero;')
    names = list(map(lambda x: x[0], table_info_unpaid.description))
    table_unpaid = table_info_unpaid.fetchall()
    print(names)
    printer(table_unpaid)
    return

def query_5_():
    cursor = collector()
    statistic = []
    
    names = ["LIIKEVAIHTO","AVOIMENA", "MAKSETTU", "ERÄÄNTYNYT"]
    table_revenue = cursor.execute('SELECT SUM(LASKU.summa) FROM LASKU') ; table_revenue = table_revenue.fetchall()
    statistic.append(table_revenue)    
    table_open =cursor.execute('SELECT SUM(LASKU.summa) FROM MYYNTIRESKONTRA JOIN LASKU ON MYYNTIRESKONTRA.laskunumero = LASKU.laskunumero;') ; table_open = table_open.fetchall()
    statistic.append(table_open)
    table_paid =cursor.execute('SELECT SUM(LASKU.summa) FROM KIRJANPITO  JOIN  LASKU ON KIRJANPITO.laskunumero= LASKU.laskunumero;'); table_paid = table_paid.fetchall()
    statistic.append(table_paid)
    table_unpaid = cursor.execute('SELECT SUM(LASKU.summa) FROM PERINTA JOIN  LASKU ON PERINTA.laskunumero= LASKU.laskunumero;'); table_unpaid = table_unpaid.fetchall()
    statistic.append(table_unpaid)        
    print("")
    for i in range(0,4):
        print (names[i]+": "+str(statistic[i])+" EUROA")
    return

def query_6_():
    cursor = collector()
    table_6 = cursor.execute('SELECT * FROM TUOTTEET;')
    names = list(map(lambda x: x[0], table_6.description))
    table_6 = table_6.fetchall()
    print(names)
    printer(table_6)
    return


                
####################################################################
# MUUTA TIETOJA
####################################################################
def update():
    while True:
        ans = update_panel()
        if ans ==1:
            payment_on_time()
        elif ans ==2:
            black_list()
        elif ans == 0:
            print("PALATAAN PÄÄOHJELMAAN.")
            time.sleep(1)
            return
        else:
            continue

def payment_on_time():

    conn = sqlite3.connect("harkka.sqlite3")
    cursor = conn.cursor()
    print("SIIRRÄ LASKU KIRJANPITOON")
    print("")
    invoice = ask()
    update_payment_on_time = cursor.execute('UPDATE MYYNTIRESKONTRA SET laskutila="MAKSETTU" WHERE laskunumero=?',invoice)
    conn.commit()
    time.sleep(1) 
    print("LASKU ON KIRJATTU MAKSETUKSI JA SIIRRETTY KIRJANPITOON.")
    return

def black_list():
    print("SIIRRÄ LASKU PERINTÄÄN")
    print("")
    conn = sqlite3.connect("harkka.sqlite3")
    cursor = conn.cursor()
    invoice = ask()
    update_black_list = cursor.execute('UPDATE MYYNTIRESKONTRA SET laskutila="MYÖHÄSSÄ" WHERE laskunumero=?',invoice)
    conn.commit()
    time.sleep(1)
    print("LASKU ON KIRJATTU ERÄÄNTYNEEKSI JA SIIRRETTY PERINTÄÄN.")
    return
####################################################################
#LISÄÄ TIETOA
####################################################################
def add_info():
    while True:
        ans = add_panel()
        if ans ==1:
            new_comp()
        elif ans ==2:
            new_prod()
        elif ans ==3:
            new_order()
        elif ans ==4:
            new_bill()
        elif ans == 0:
            print("PALATAAN PÄÄOHJELMAAN.")
            time.sleep(1)
            return
        else:
            continue


def new_comp():
    conn = sqlite3.connect("harkka.sqlite3")
    cursor = conn.cursor()
    while True:
        try:
            comp_name = input("ANNA YRITYKSEN NIMI: ")
            comp_email = input("ANNA YRITYKSEN SÄHKÖPOSTI: ")
            comp_phone = int(input("ANNA YRITYKSEN PUHELINUMERO NUMEROINA: "))
            comp_city = input("ANNA YRITYKSEN KOTIKAUPUNKI: ")
            comp_addres = input("ANNA YRITYKSEN KATUOSOITE: ")
            comp_postal = int(input("ANNA YRITYKSEN POSTINUMERO: "))
            break
        except Error as e:
            continue
    cursor.execute('INSERT INTO ASIAKAS(yritys_nimi,sahkoposti,puhelinnumero,kaupunki,katu,postinumero) VALUES(?,?,?,?,?,?)',(comp_name,comp_email,comp_phone,comp_city,comp_addres,comp_postal))
    time.sleep(1)
    print("YRITYS ON LISÄTTY TIETOKANTAAN.")
    conn.commit()
    return

def new_prod():
    conn = sqlite3.connect("harkka.sqlite3")
    cursor = conn.cursor()
    while True:
        try:
            prod_name = input("ANNA TUOTTEEN NIMI: ")
            prod_price = input("ANNA TUOTTEEN HINTA KOKONAISLUKUNA EUROISSA: ")
            break
        except Error as e:
            continue
    cursor.execute('INSERT INTO TUOTTEET(nimi,hinta) VALUES(?,?)',(prod_name,prod_price,))
    time.sleep(1)
    print("TUOTE ON LISÄTTY TIETOKANTAAN.")
    conn.commit()
    return

def new_order():
    print(" VARMISTA; ETTÄ ASIAKASNUMERO ON KÄYTÖSSÄ.")
    conn = sqlite3.connect("harkka.sqlite3")
    cursor = conn.cursor()
    cust_num =input("ANNA ASIAKASNUMERO: ")
    cursor.execute('INSERT INTO TILAUS(asiakas_ID)values(?)',(cust_num,))
    conn.commit()

    
    order_num = cursor.execute('SELECT COUNT(*)FROM TILAUS')
    order_num = order_num.fetchall()
    for i in order_num:
        order_num = i[0]
    order_num = str(order_num)

    
    while True:
        conn = sqlite3.connect("harkka.sqlite3")
        cursor = conn.cursor()
        prod_code = input("ANNA TUOTTEEN TUOTEKOODI: ")
        prod_quantity = (input("ANNA TUOTTEEN MÄÄRÄ KOKONAISLUKUNA: "))                  
        cursor.execute('INSERT INTO TILAUKSEN_TASMAYS(tilausnumero,tuotenumero,maara) VALUES(?,?,?)',(order_num,prod_code,prod_quantity,))
        conn.commit()
        ans = input("LISÄTÄÄNKÖ LISÄÄ TUOTTEITA TILAUKSEEN? (K/E) ")
        if ans == "E":
            print("TUOTTEET ON LISÄTTY TILAUKSEEN.")
            break
        
    conn = sqlite3.connect("harkka.sqlite3")
    cursor = conn.cursor()
    total_bill=  cursor.execute('SELECT SUM(TUOTTEET.hinta*TILAUKSEN_TASMAYS.maara)FROM TUOTTEET JOIN TILAUKSEN_TASMAYS ON TILAUKSEN_TASMAYS.tuotenumero =TUOTTEET.tuotenumero\
                                GROUP BY TILAUKSEN_TASMAYS.tilausnumero HAVING TILAUKSEN_TASMAYS.tilausnumero = ?;',(order_num,))
    total_bill = total_bill.fetchall()
    for i in total_bill:
        total_bill = i[0]
    total_bill = str(total_bill)
    invoice_number = 1000+int(order_num)
    invoice_numner = str(invoice_number)
    
    conn = sqlite3.connect("harkka.sqlite3")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO LASKU(tilausnumero,summa,viitenumero ) VALUES(?,?,?)',(order_num,total_bill,invoice_number,))
    conn.commit()

    bill_number =   total_bill=  cursor.execute('SELECT COUNT(*) FROM LASKU')
    for i in bill_number:
        bill_number = i[0]
    bill_number = str(bill_number)

    conn = sqlite3.connect("harkka.sqlite3")
    cursor = conn.cursor()
    cursor.execute('INSERT INTO MYYNTIRESKONTRA(asiakas_ID,laskunumero,saldo) SELECT TILAUS.asiakas_ID, LASKU.laskunumero, LASKU.summa\
                    FROM LASKU JOIN TILAUS ON LASKU.tilausnumero = TILAUS.tilausnumero WHERE LASKU.laskunumero = ? ;',(bill_number,))
    conn.commit()
    
    print("TILAUS JA LASKU ON LISÄTTY JÄRJESTELMÄÄN.")   
    time.sleep(1)
    return


####################################################################
#VISUALISOINTI
####################################################################
    
def count():
    cursor =  collector()
    companies_city = cursor.execute('SELECT ASIAKAS.kaupunki, COUNT(TILAUS.tilausnumero) FROM ASIAKAS JOIN TILAUS ON ASIAKAS.asiakas_ID = TILAUS.asiakas_ID GROUP BY kaupunki')
    companies_city = companies_city.fetchall()
    return companies_city  
        
def draw(cities, counts):

    output_file("tilauskanta_per_kaupunki.html")
    source = ColumnDataSource(data=dict(cities=cities, counts=counts))
    p = figure(x_range=cities, plot_height=350, toolbar_location=None, title="TILAUKSET PER KAUPUNKI")
    p.vbar(x='cities', top='counts', width=0.9, source=source, legend="cities",
           line_color='white', fill_color=factor_cmap('cities', palette=Spectral6, factors=cities))
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.y_range.end = 9
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    show(p)

def vizualize():
    data = count()
    col_names = []
    order_count = []
    for i in data:
        col_names.append(i[0])
        order_count.append(i[1])
    draw(col_names,order_count)   
    return
####################################################################
#YLEISET 
####################################################################


def ask():
    while True:
        try: 
            query = input("Syötä laskunnumero: ")
            query = (query,)
        except KeyboardInterrupt:
            print("Syöttämäsi lasku on virheellinen, syötä nimi uudestaan."+"\n")
            time.sleep(1)
            continue
        if len(query)==0:
            print("Et antanut nimeä, syötä nimi uudestaan."+"\n")
            time.sleep(1)
            continue
        else:
            break
    return query

def load_database(): # varmaan turha
    try:
        conn = sqlite3.connect("harkka.sqlite3")
        conn.close
        return 
    except Error as e:
        print(e)
        print("TIETOKANTAA EI LÖYTYNYT, SAMMUTETAAN.")
        sys.exit(0)

def collector():
    conn = sqlite3.connect("harkka.sqlite3")
    cursor = conn.cursor()
    return cursor

def printer(table):
    for i in table:
        print(i)
    return

    
def main():
    load_database()
    while True:
        ans = main_panel()
        if ans == 1:
            search()
        elif ans == 2:
            update()
        elif ans == 3:
            add_info()
        elif ans == 4:
            vizualize()
        elif ans == 0:
            print("KIITOS OHJELMAN KÄYTÖSTÄ")
            print("******************************************")
            sys.exit(0)
        else:
            continue
####################################################################
main()
        

