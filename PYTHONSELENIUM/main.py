import os

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.implicitly_wait(30)
driver.maximize_window()


class waluta:
    def __init__(self, nazwa, jedn, kurs):
        self.nazwa = nazwa
        self.jedn = jedn
        self.kurs = float(kurs.replace(",", "."))


def porownaj(lwn, lws):
    licznik = len(lwn)
    for i in range(licznik):
        if lwn[i].kurs == lws[i].kurs:
            print(str(lwn[i].nazwa) + " | " + str(lwn[i].jedn) + " | " + str(lwn[i].kurs) + "zł Bez zmian")
        else:
            print(str(lwn[i].nazwa) + " | " + str(lwn[i].jedn) + " | " + str(lwn[i].kurs) +
                  "zł Zmiana: " + str(float(lwn[i].kurs) - float(lws[i].kurs)))


def saveToFile(plik, dane):
    file = open(plik, "w")
    zawartosc = ""
    for x in dane:
        zawartosc += str(x.nazwa) + "," + str(x.jedn) + "," + str(x.kurs) + "\n"
    file.write(zawartosc)
    file.close()


def readFromFile(plik):
    lps = []
    file = open(plik, "r")
    for x in file:
        r = x.split(",")
        lps.append(waluta(r[0], r[1], str(r[2])))
    file.close()
    return lps


driver.get('https://www.nbp.pl/home.aspx?f=/kursy/kursya.html')

table = driver.find_element(By.CLASS_NAME, 'nbptable')

body = table.find_element(By.TAG_NAME, 'tbody')

items = body.find_elements(By.TAG_NAME, 'tr')

lw = []
for item in items:
    name = item.find_element(By.CLASS_NAME, 'left')
    curr = item.find_elements(By.CLASS_NAME, 'right')
    lw.append(waluta(name.text, curr[0].text, curr[1].text))
if os.path.exists("danewalut.txt"):
    porownaj(lw, readFromFile("danewalut.txt"))
saveToFile("danewalut.txt", lw)
driver.quit()
