import numpy as np
import os


class Rock:
    def __init__(self, posX, posY, colour):
        self.row = posX
        self.column = posY
        self.stoneColour = colour
        self.neighbours = []

    def setColour(self, colour):
        self.stoneColour = colour

    def returnSelf(self):
        return self

    def setNeighbours(self, nN, nS, nW, nE):
        self.neighbours.append(nN)
        self.neighbours.append(nS)
        self.neighbours.append(nE)
        self.neighbours.append(nW)


class Board:

    def __init__(self, rows, columns):
        self.rowNumber = rows + 2
        self.columnNumber = columns + 2
        self.matrix = np.ndarray(shape=(self.rowNumber, self.columnNumber), dtype=Rock)

        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                if i == 0 or j == 0 or i == self.rowNumber - 1 or j == self.columnNumber - 1:
                    self.matrix[i, j] = Rock(i, j, 3)
                else:
                    self.matrix[i, j] = Rock(i, j, 0)
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                if i != 0 and j != 0 and i != self.rowNumber - 1 and j != self.columnNumber - 1:
                    self.matrix[i, j].setNeighbours(self.matrix[i - 1, j], self.matrix[i + 1, j],
                                                    self.matrix[i, j + 1], self.matrix[i, j - 1])

    def resetBoard(self):
        for i in range(self.rowNumber):
            for j in range(self.columnNumber):
                if i == 0 or j == 0 or i == self.rowNumber - 1 or j == self.columnNumber - 1:
                    self.matrix[i, j].setColour(3)
                else:
                    self.makeEmpty(i, j)

    def getRock(self, x, y):
        return self.matrix[x, y]

    def setRock(self, x, y, colour):
        self.matrix[x, y].setColour(colour)

    def makeEmpty(self, x, y):
        self.matrix[x, y].stoneColour = 0

    def showBoard(self):
        numR0 = 1
        numC0 = 1
        numRmax = 1
        numCmax = 1

        for i in range(self.rowNumber):
            line = ""
            for j in range(self.columnNumber):
                if self.matrix[i, j].stoneColour == 0:
                    char = " "
                elif self.matrix[i, j].stoneColour == 1:
                    char = "B"
                elif self.matrix[i, j].stoneColour == 2:
                    char = "C"
                elif self.matrix[i, j].stoneColour == 3:
                    if self.rowNumber < 12 or self.columnNumber < 12:
                        if (i == 0 or i == self.rowNumber - 1) and (j == 0 or j == self.columnNumber - 1):
                            char = "X"
                        elif i == 0:
                            char = numC0
                            numC0 += 1
                        elif i == self.rowNumber - 1:
                            char = numCmax
                            numCmax += 1
                        elif j == 0:
                            char = numR0
                            numR0 += 1
                        else:
                            char = numRmax
                            numRmax += 1
                    else:
                        char = "X"
                else:
                    char = "E"
                line += "|" + str(char)
            line += "|"
            print(line)


class Game:
    turn = 2
    passCounter = 0

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.board = Board(rows, columns)
        self.toKill = set()
        self.pointsBlack = 0
        self.pointsWhite = 0
        self.posx = -1
        self.posy = -1
        self.koRock = None

    def checkNoBreath(self, rock):
        toCheck = set()

        for neighbour in rock.neighbours:
            if neighbour in self.toKill:
                continue
            if neighbour.stoneColour == 0:
                self.toKill.clear()
                return False
            elif neighbour.stoneColour == rock.stoneColour:
                toCheck.add(neighbour)

        self.toKill.add(rock)

        for rockCheck in toCheck:
            if not self.checkNoBreath(rockCheck):
                return False
        return True

    def checkTeritoryForPoints(self, rock, oponentColor, points, used):
        checkPoint = set()

        for neighbour in rock.neighbours:
            if neighbour in points:
                continue
            if neighbour.stoneColour == oponentColor:
                points.clear()
                return False
            elif neighbour.stoneColour == rock.stoneColour:
                checkPoint.add(neighbour)

        points.add(rock)
        used.add(rock)

        for rockCheck in checkPoint:
            if not self.checkTeritoryForPoints(rockCheck, oponentColor, points, used):
                return False
        return True

    def getTeritoryPoints(self):
        self.pointsBlack = 0
        self.pointsWhite = 0
        used = set()
        pointsList = set()
        for i in range(self.board.rowNumber):
            for j in range(self.board.columnNumber):
                if self.board.matrix[i, j].stoneColour == 0 and self.board.matrix[i, j] not in used:
                    self.checkTeritoryForPoints(self.board.matrix[i, j], 1, pointsList, used)
                    self.pointsBlack += len(pointsList)
                    pointsList.clear()
                    self.checkTeritoryForPoints(self.board.matrix[i, j], 2, pointsList, used)
                    self.pointsWhite += len(pointsList)
                    pointsList.clear()
        if self.pointsBlack == self.rows * self.columns:
            self.pointsBlack = 0
        if self.pointsWhite == self.rows * self.columns:
            self.pointsWhite = 0

    def passTurn(self):
        self.changeTour()
        self.passCounter += 1
        if self.passCounter >= 2:
            return True
        else:
            return False

    def killStones(self):
        for rock in self.toKill:
            if len(self.toKill) == 1:
                self.koRock = rock
            self.board.makeEmpty(rock.row, rock.column)
        self.toKill.clear()

    def insertStone(self, x, y):
        if self.checkValidPositionForInsert(x, y):
            self.board.setRock(x, y, self.turn)
            self.changeTour()
            self.findGroupToKill(self.turn)
            if not self.checkSuicide(x, y):
                self.board.makeEmpty(x, y)
                self.changeTour()
                return False
            self.passCounter = 0
            return True
        else:
            return False

    def removeStone(self, row, column):
        if self.checkValidPositionForRemove(row, column):
            self.board.makeEmpty(row, column)
            self.changeTour()
            self.passCounter = 0
            return True
        else:
            return False

    def checkValidPositionForInsert(self, x, y):
        if self.board.getRock(x, y).stoneColour != 0:
            return False
        elif self.koRock is not None:
            if self.koRock.row == x and self.koRock.column == y:

                self.board.setRock(x, y, self.turn)
                count = 0
                for n in self.board.matrix[x, y].neighbours:
                    if self.checkNoBreath(n):
                        if len(self.toKill) == 1:
                            count += 1
                        else:
                            count = 0
                            break
                self.board.makeEmpty(x, y)

                if count == 1:
                    return False

            self.koRock = None
            return True
        else:
            return True

    def checkValidPositionForRemove(self, x, y):
        if (self.board.getRock(x, y).stoneColour == 1 or self.board.getRock(x, y).stoneColour == 2):
            return True
        else:
            return False

    def checkSuicide(self, x, y):
        if self.checkNoBreath(self.board.matrix[x, y]):
            return False
        else:
            return True

    def findGroupToKill(self, colorToKill):
        for i in range(self.board.rowNumber):
            for j in range(self.board.columnNumber):
                if self.board.matrix[i, j].stoneColour == colorToKill:
                    self.checkNoBreath(self.board.matrix[i, j])
                    self.killStones()

    def changeTour(self):
        if self.turn == 2:
            self.turn = 1
        else:
            self.turn = 2

    def countStones(self, color):
        count = 0
        for i in range(self.board.rowNumber):
            for j in range(self.board.columnNumber):
                if self.board.matrix[i, j].stoneColour == color:
                    count += 1
        return count

    def gameMenu(self):
        os.system('cls')
        self.getTeritoryPoints()
        self.board.showBoard()

        bp1 = self.pointsBlack
        wp1 = self.pointsWhite
        bp2 = self.countStones(2)
        wp2 = self.countStones(1)

        print("Czarny Terytorium: " + str(bp1) + " Czarny Kamienie: " + str(bp2) + " Czarny Suma: " + str(bp1 + bp2))
        print("Bialy Terytorium: " + str(wp1) + " Bialy Kamienie: " + str(wp2) + " Bialy Suma: " + str(wp1 + wp2))

        if self.turn == 2:
            player = "Czarnego"
        else:
            player = "Bialego"
        print("Tura gracza " + player)

        ch = int(input("Wybierz opcje:\n1.Wstaw\n2.Spasuj\n"))
        if ch == 1:
            self.posx = -1
            self.posy = -1
            while self.posx < 1 or self.posx > self.board.rowNumber - 1 or self.posy < 1 or self.posy > self.board.rowNumber - 1:
                self.posx = int(input("Podaj rzad\n"))
                self.posy = int(input("Podaj kolumne\n"))
            if not self.insertStone(self.posx, self.posy):
                print("Blendny Ruch")
                os.system("pause")
        elif ch == 2:
            if self.passTurn():
                return True  # konczenie gry
        return False

    def finalMenu(self):

        ch = -1
        while ch != 1:
            os.system('cls')
            self.getTeritoryPoints()
            self.board.showBoard()

            bp1 = self.pointsBlack
            wp1 = self.pointsWhite
            bp2 = self.countStones(2)
            wp2 = self.countStones(1)

            print(
                "Czarny Terytorium: " + str(bp1) + " Czarny Kamienie: " + str(bp2) + " Czarny Suma: " + str(bp1 + bp2))
            print("Bialy Terytorium: " + str(wp1) + " Bialy Kamienie: " + str(wp2) + " Bialy Suma: " + str(wp1 + wp2))

            ch = int(input("Wybierz opcje:\n1.Oblicz punktacje kocowa\n2.Usuwaj kamienie\n"))
            if ch == 2:
                self.posx = -1
                self.posy = -1
                while self.posx < 1 or self.posx > self.board.rowNumber - 1 or self.posy < 1 or self.posy > self.board.rowNumber - 1:
                    self.posx = int(input("Podaj rzad\n"))
                    self.posy = int(input("Podaj kolumne\n"))
                if not self.removeStone(self.posx, self.posy):
                    print("Blendny Ruch")
                    os.system("pause")
        os.system('cls')
        self.getTeritoryPoints()
        self.board.showBoard()

        bp1 = self.pointsBlack
        wp1 = self.pointsWhite
        bp2 = self.countStones(2)
        wp2 = self.countStones(1)

        print("Czarny Terytorium: " + str(bp1) + " Czarny Kamienie: " + str(bp2) + " Czarny Suma: " + str(bp1 + bp2))
        print("Bialy Terytorium: " + str(wp1) + " Bialy Kamienie: " + str(wp2) + " Bialy Suma: " + str(wp1 + wp2))

        os.system("pause")
        self.turn = 2
        self.passCounter = 0

    def mainMenu(self):
        while True:
            os.system('cls')
            wybor = int(input("Co chcesz zrobic?\n1-Nowa gra 9x9\n2-Wczytaj stan gry z pliku\n0-Wyjdz\n"))
            if wybor == 1:
                self.board.resetBoard()
                self.turn = 2

                while True:

                    if self.gameMenu():
                        break
                self.finalMenu()
            elif wybor == 2:
                self.readGameStateFromFile("dane.txt")
                while True:
                    if self.gameMenu():
                        break
                self.finalMenu()
            elif wybor == 0:
                break

    def readGameStateFromFile(self, pathToFile):
        self.board.resetBoard()
        f = open(pathToFile, "r")
        for x in f:
            r = x.split(",")
            self.board.setRock(int(r[0]), int(r[1]), int(r[2]))


if __name__ == '__main__':
    g = Game(9, 9)
    g.mainMenu()
