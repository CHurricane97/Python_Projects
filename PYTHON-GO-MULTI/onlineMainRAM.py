import uuid

from silnik import game as g
from silnik import rock as r
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

posX = -1
posY = -1
games = {}

iterator = -1


@app.route("/load/")
def loadGame():
    gameId = int(request.args.get("gameId"))
    data = str(request.args.get("data"))
    xyz = data.split("\n")
    for s in xyz:
        rock = s.split(",")
        games[gameId].getCurrentBoard().setRock(int(rock[0]), int(rock[1]), int(rock[2]))
    return jsonify({"load": "load"})


@app.route("/create/")
def createGame():
    nick = str(request.args.get("nick"))
    global iterator
    iterator += 1
    games[iterator] = g.Game(9, 9, iterator, nick)
    return jsonify({"gameId": games[iterator].gameID})


@app.route("/onGoing/")
def isOnGoing():
    gameId = int(request.args.get("gameId"))
    return jsonify({"onGoing": games[gameId].isOngoing})


@app.route("/pass/")
def passMove():
    gameId = int(request.args.get("gameId"))
    if games[gameId].passTurn():
        games[gameId].isOngoing = 0
    return jsonify({"passCounter": games[gameId].passCounter})


@app.route("/checkT/")
def turn():
    gameId = int(request.args.get("gameId"))
    return jsonify({"turn": games[gameId].turn})


@app.route("/join/")
def joinGame():
    nick = str(request.args.get("nick"))
    ng = -1
    for gm in list(games.keys())[:]:
        if gm in games:
            if not games[gm].started:
                games[gm].started = True
                games[gm].player2Nick = nick
                ng = gm
                break
    return jsonify({"gameId": ng})


@app.route("/leave/")
def leaveGame():
    gameId = int(request.args.get("gameId"))
    if games[gameId].isOngoing == 0 or games[gameId].player2Nick == "":
        games.pop(gameId)
        return jsonify({"remove": "Gra: " + str(gameId) + " zostala usunieta"})
    else:
        games[gameId].isOngoing = 0
        return jsonify({"remove": "Gra: " + str(gameId) + " w trakcie usuwania"})


@app.route("/board/")
def showBoard():
    gameId = int(request.args.get("gameId"))
    board = games[gameId].board
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
    blackTerritoryPoints = games[gameId].getTerritoryPoints(1)
    whiteTerritoryPoints = games[gameId].getTerritoryPoints(2)
    blackStonePoints = games[gameId].countStones(2)
    whiteStonePoints = games[gameId].countStones(1)

    p1 = games[gameId].getP1()
    p2 = games[gameId].getP2()
    print(p1)
    print(p2)
    print("ss")
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
    games[gameId].posX = -1
    games[gameId].posY = -1
    while games[gameId].posX < 1 or games[gameId].posX > games[gameId].getCurrentBoard().rowNumber - 1 \
            or games[gameId].posY < 1 or games[gameId].posY > games[gameId].getCurrentBoard().rowNumber - 1:
        games[gameId].posX = x
        games[gameId].posY = y
    if not games[gameId].insertStone(games[gameId].posX, games[gameId].posY):
        return jsonify({"response": "Zly Ruch!"})
    print(games[gameId].turn)
    return jsonify({"response": "Ruch Zatwierdzony"})


if __name__ == '__main__':
    app.run()
