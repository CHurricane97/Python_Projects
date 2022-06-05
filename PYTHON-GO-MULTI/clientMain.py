import requests
import json
import time
import os

turn = 2


def createGame(nick):
    response = requests.get('http://127.0.0.1:5000/create/' + nick)
    data = response.text
    return json.loads(data)['gameId']


def joinGame(nick):
    response = requests.get('http://127.0.0.1:5000/join/' + nick)
    data = response.text
    return json.loads(data)['gameId']


def mainMenu():
    nick = ""
    while nick == "":
        nick = input("Podaj Nick\n")
    while True:
        os.system('cls')
        choice = int(input("1.Stworz gre\n2.Dolacz do gry\n3.Zaladuj z pliku\n4.Wyjscie\n"))
        if choice == 1:
            gameID = createGame(nick)
            inGameMenu(gameID, 2)

        elif choice == 2:
            gameID = joinGame(nick)
            if gameID == -1:
                print("Brak dostepnych gier")
            else:
                inGameMenu(gameID, 1)

        elif choice == 3:
            file = open("data.txt", "r")
            text = ""
            for s in file:
                text += s
            gameID = createGame(nick)
            requests.get('http://127.0.0.1:5000/load/' + str(gameID) + "/" + text)
            inGameMenu(gameID, 2)

        elif choice == 4:
            break


def inGameMenu(gameID, color):
    while True:
        os.system('cls')
        response = requests.get('http://127.0.0.1:5000/onGoing/' + str(gameID))
        data = response.text
        if json.loads(data)['onGoing'] == 0:
            os.system('cls')
            response = requests.get('http://127.0.0.1:5000/board/' + str(gameID))
            data = response.text
            print(json.loads(data)['board'])

            response = requests.get('http://127.0.0.1:5000/points/' + str(gameID))
            data = response.text
            print(json.loads(data)['points'])

            response = requests.get('http://127.0.0.1:5000/leave/' + str(gameID))
            data = response.text
            print(json.loads(data)['remove'])
            os.system("pause")
            break

        response = requests.get('http://127.0.0.1:5000/checkT/' + str(gameID))
        data = response.text

        if int(json.loads(data)['turn']) == 1:
            print("Tura Gracza Białego")
        else:
            print("Tura Gracza Czarnego")

        if int(json.loads(data)['turn']) == color:
            response = requests.get('http://127.0.0.1:5000/board/' + str(gameID))
            data = response.text
            print(json.loads(data)['board'])

            response = requests.get('http://127.0.0.1:5000/points/' + str(gameID))
            data = response.text
            print(json.loads(data)['points'])

            choice = int(input("1.Wstaw\n2.Spasuj\n3.Wycofaj się\n"))
            if choice == 1:
                x = -1
                y = -1
                while x < 1 or x > 9 or y < 1 or y > 9:
                    y = int(input("Podaj Rząd:\n"))
                    x = int(input("Podaj Kolumne:\n"))
                response = requests.get('http://127.0.0.1:5000/cords/' + str(x) + ',' + str(y) + ',' + str(gameID))
                data = response.text
                print(json.loads(data)['response'])
                os.system("pause")
            elif choice == 2:
                response = requests.get('http://127.0.0.1:5000/pass/' + str(gameID))
                data = response.text
                if int(json.loads(data)['passCounter']) == 2:
                    print("Gra zakonczona")
                    os.system("pause")
                    break
            elif choice == 3:
                response = requests.get('http://127.0.0.1:5000/leave/' + str(gameID))
                data = response.text
                print(json.loads(data)['remove'])
                print("Opuszczono gre")
                os.system("pause")
                break

        else:

            choice = int(input("1.Odswierz stan gry\n2.wycofaj sie\n"))
            if choice == 1:
                print("Sprawdzam...")
                os.system("pause")


            elif choice == 2:
                response = requests.get('http://127.0.0.1:5000/leave/' + str(gameID))
                data = response.text
                print(json.loads(data)['remove'])
                print("Opuszczono gre")
                os.system("pause")
                break


if __name__ == '__main__':
    mainMenu()
