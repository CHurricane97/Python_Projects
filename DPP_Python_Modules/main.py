from strToJson import WyswietlOdpowiedz
import os

convert = WyswietlOdpowiedz()


def mainMenu():
    while True:
        nl = "\n"
        options = "1. Znajdz regiony kozystajace z waluty waluty" + nl
        options += "2. Znajdz kraj po kodzie kraju" + nl
        options += "3. Sprawdz detale regionu kraju" + nl
        options += "4. Sprawdź miasta w regionie kraju" + nl
        options += "5. Znajdź miasta w lokacji" + nl
        options += "6. Znajdź miasta w danym promieniu od innego miasta" + nl
        options += "7. Sprawdz detale danego miasta" + nl
        options += "0. Exit" + nl
        choice = int(input(options))
        if choice == 0:
            break
        elif choice == 1:
            subMenu1()
        elif choice == 2:
            subMenu2()
        elif choice == 3:
            subMenu3()
        elif choice == 4:
            subMenu4()
        elif choice == 5:
            subMenu5()
        elif choice == 6:
            subMenu6()
        elif choice == 7:
            subMenu7()


    return


def subMenu1():
    choice = str(input("Wpisz kod waluty np \"GBP\"\n"))
    print(convert.getCountryFromCurrency(choice))
    os.system("pause")
    os.system('cls')


def subMenu2():
    choice = str(input("Wpisz kod kraju np \"US\"\n"))
    print(convert.getCountryDetailsFromCountry("true", choice))
    os.system("pause")
    os.system('cls')


def subMenu3():
    choice = str(input("Wpisz kod kraju np \"US\"\n"))
    choice1 = str(input("Wpisz kod regionu np \"CA\"\n"))
    print(convert.getRegionsDetailsFromCountryAndRegionCode("true", "EN", choice, choice1))
    os.system("pause")
    os.system('cls')


def subMenu4():
    choice = str(input("Wpisz kod kraju np \"US\"\n"))
    choice1 = str(input("Wpisz kod regionu np \"CA\"\n"))
    print(convert.CountryRegionsCitiesFromCountryAndRegionCode("true", "EN", choice, choice1))
    os.system("pause")
    os.system('cls')


def subMenu5():
    location = str(input("Wpisz kod lokacji w formacie ISO-6709 np: \"+46+002\"\n"))
    print(convert.getCityListFromLocation(location))
    os.system("pause")
    os.system('cls')

def subMenu6():
    cityCode = str(input("Wpisz kod miasta np \"Q60\"\n"))
    radius = str(input("Wpisz promien np \"100\"\n"))
    print(convert.getNearbyCitiesFromRadiusNearOtherCity(radius, cityCode))
    os.system("pause")
    os.system('cls')

def subMenu7():
    cityCode = str(input("Wpisz kod miasta np \"Q60\"\n"))
    print(convert.getCityDetailsFromCityCode("true", cityCode))
    os.system("pause")
    os.system('cls')

if __name__ == '__main__':
    mainMenu()
