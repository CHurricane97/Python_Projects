import uuid

from silnik import game as g
from silnik import rock as r
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

idList = {}

iterator = -1


def saveToFile(gameId, tempgame):
    f = open(str(gameId) + ".txt", "w")

    sep = "\n"
    s = str(gameId).replace("\n", "") + sep \
        + str(tempgame.player1Nick).replace("\n", "") + sep \
        + str(tempgame.player2Nick).replace("\n", "") + sep \
        + str(tempgame.turn).replace("\n", "") + sep \
        + str(tempgame.passCounter).replace("\n", "") + sep \
        + str(tempgame.blackStonesSet).replace("\n", "") + sep \
        + str(tempgame.whiteStonesSet).replace("\n", "") + sep \
        + str(tempgame.started).replace("\n", "") + sep \
        + str(tempgame.isOngoing).replace("\n", "") + sep
    if tempgame.koRock is not None:
        s += str(tempgame.koRock.row).replace("\n", "") + "," + str(tempgame.koRock.column).replace("\n", "") \
             + "," + str(tempgame.koRock.stoneColour).replace("\n", "") + sep
    else:
        s += "-1" + "," + "-1" + "," + "-1" + sep
    for i in range(11):
        for j in range(11):
            if not (i == 0 or j == 0 or i == 10 or j == 10):
                s += str(i).replace("\n", "") + "," + str(j).replace("\n", "") + "," \
                     + str(tempgame.board.matrix[i, j].stoneColour).replace("\n", "") + sep

    f.write(s)
    f.close()


def loadStateFromFile(pathToFile):
    f = open(pathToFile, "r")
    itera = 0
    tempgame = g.Game(9, 9, -22, "temp")
    for x in f:
        if itera == 0:
            tempgame.gameID = int(x.replace("\n", ""))
        elif itera == 1:
            tempgame.player1Nick = x.replace("\n", "")
        elif itera == 2:
            tempgame.player2Nick = x.replace("\n", "")
        elif itera == 3:
            tempgame.turn = int(x.replace("\n", ""))
        elif itera == 4:
            tempgame.passCounter = int(x.replace("\n", ""))
        elif itera == 5:
            tempgame.blackStonesSet = int(x.replace("\n", ""))
        elif itera == 6:
            tempgame.whiteStonesSet = int(x.replace("\n", ""))
        elif itera == 7:
            tempgame.started = bool(x.replace("\n", ""))
        elif itera == 8:

            tempgame.isOngoing = int(x.replace("\n", ""))
            print(tempgame.isOngoing)
        elif itera == 9:
            kor = x.split(",")
            print(kor)
            if int(kor[0].replace("\n", "")) == -1 and int(kor[1].replace("\n", "")) == -1 \
                    and int(kor[2].replace("\n", "")) == -1:
                tempgame.koRock = None
            else:
                tempgame.koRock = r.Rock(int(kor[0].replace("\n", "")), int(kor[1].replace("\n", "")),
                                         int(kor[2].replace("\n", "")))
        else:
            rr = x.split(",")
            tempgame.board.setRock(int(rr[0].replace("\n", "")), int(rr[1].replace("\n", "")),
                                   int(rr[2].replace("\n", "")))
        itera += 1
    f.close()

    return tempgame


@app.route("/load/")
def loadGame():
    gameId = int(request.args.get("gameId"))
    data = str(request.args.get("data"))
    game = loadStateFromFile(str(gameId) + ".txt")
    xyz = data.split("\n")
    for s in xyz:
        rock = s.split(",")
        game.getCurrentBoard().setRock(int(rock[0]), int(rock[1]), int(rock[2]))
    saveToFile(gameId, game)
    return jsonify({"load": "load"})


@app.route("/create/")
def createGame():
    nick = str(request.args.get("nick"))
    global iterator
    iterator += 1
    gameID = iterator
    idList[gameID] = False
    # createFile(gameID)
    saveToFile(gameID, g.Game(9, 9, gameID, nick))
    return jsonify({"gameId": gameID})


@app.route("/join/")
def joinGame():
    nick = str(request.args.get("nick"))
    ng = -1
    for gm in list(idList.keys())[:]:
        if gm in idList:
            if not idList[gm]:
                idList[gm] = True
                game = loadStateFromFile(str(gm) + ".txt")
                game.player2Nick = nick
                saveToFile(game.gameID, game)
                ng = game.gameID
                break
    return jsonify({"gameId": ng})


@app.route("/leave/")
def leaveGame():
    gameId = int(request.args.get("gameId"))
    game = loadStateFromFile(str(gameId) + ".txt")
    if game.isOngoing == 0 or game.player2Nick == "":
        idList.pop(gameId)
        os.remove(str(gameId) + ".txt")
        return jsonify({"remove": "Gra: " + str(gameId) + " zostala usunieta"})
    else:
        game.isOngoing = 0
        print(game.isOngoing)
        saveToFile(gameId, game)
        return jsonify({"remove": "Gra: " + str(gameId) + " w trakcie usuwania"})


@app.route("/onGoing/")
def isOnGoing():
    gameId = int(request.args.get("gameId"))
    game = loadStateFromFile(str(gameId) + ".txt")
    return jsonify({"onGoing": game.isOngoing})


@app.route("/pass/")
def passMove():
    gameId = int(request.args.get("gameId"))
    game = loadStateFromFile(str(gameId) + ".txt")
    if game.passTurn():
        game.isOngoing = 0
    saveToFile(gameId, game)
    return jsonify({"passCounter": game.passCounter})


@app.route("/checkT/")
def turn():
    gameId = int(request.args.get("gameId"))
    game = loadStateFromFile(str(gameId) + ".txt")
    return jsonify({"turn": game.turn})


@app.route("/board/")
def showBoard():
    gameId = int(request.args.get("gameId"))
    game = loadStateFromFile(str(gameId) + ".txt")
    board = game.board
    numberInZeroRow = 1
    numberInZeroColumn = 1
    numberInLastRow = 1
    numberInLastColumn = 1
    line = ""
    for i in range(board.rowNumber):
        for j in range(board.columnNumber):
            if board.matrix[i, j].stoneColour == 0:
                char = " "
            elif board.matrix[i, j].stoneColour == 1:
                char = "B"
            elif board.matrix[i, j].stoneColour == 2:
                char = "C"
            elif board.matrix[i, j].stoneColour == 3:
                if board.rowNumber < 12 or board.columnNumber < 12:
                    if (i == 0 or i == board.rowNumber - 1) and (j == 0 or j == board.columnNumber - 1):
                        char = "O"
                    elif i == 0:
                        char = numberInZeroColumn
                        numberInZeroColumn += 1
                    elif i == board.rowNumber - 1:
                        char = numberInLastColumn
                        numberInLastColumn += 1
                    elif j == 0:
                        char = numberInZeroRow
                        numberInZeroRow += 1
                    else:
                        char = numberInLastRow
                        numberInLastRow += 1
                else:
                    char = "O"
            else:
                char = "E"
            line += "|" + str(char)
        line += "|"
        line += "\n"
    return jsonify({"board": line})


@app.route("/points/")
def showPoints():
    gameId = int(request.args.get("gameId"))
    game = loadStateFromFile(str(gameId) + ".txt")
    blackTerritoryPoints = game.getTerritoryPoints(1)
    whiteTerritoryPoints = game.getTerritoryPoints(2)
    blackStonePoints = game.countStones(2)
    whiteStonePoints = game.countStones(1)

    p1 = game.getP1()
    p2 = game.getP2()
    return jsonify({"points": "Gracz Czarny " + p1 + " Teryrorium: "
                              + str(blackTerritoryPoints) +
                              " Kamienie: " +
                              str(blackStonePoints) +
                              " Punkty: " +
                              str(blackTerritoryPoints +
                                  blackStonePoints) +
                              "\n" + "Gracz Bialy " + p2 + " Teryrorium: " +
                              str(whiteTerritoryPoints) +
                              " Kamienie: " +
                              str(whiteStonePoints) +
                              " Punkty:  "
                              + str(whiteTerritoryPoints +
                                    whiteStonePoints + 7.5)
                              + "\n"})


@app.route("/cords/")
def insertCoordinates():
    gameId = int(request.args.get("gameId"))
    y = int(request.args.get("y"))
    x = int(request.args.get("x"))
    game = loadStateFromFile(str(gameId) + ".txt")

    posX = -1
    posY = -1
    while posX < 1 or posX > game.getCurrentBoard().rowNumber - 1 \
            or posY < 1 or posY > game.getCurrentBoard().rowNumber - 1:
        posX = x
        posY = y
    if not game.insertStone(posX, posY):
        return jsonify({"response": "Zly Ruch!"})
    saveToFile(gameId, game)
    print(game.turn)
    return jsonify({"response": "Ruch Zatwierdzony"})


if __name__ == '__main__':
    app.run()
