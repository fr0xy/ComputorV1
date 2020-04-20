import sys
import re
import my_math


def splitPlusMinus(equation):
    polynome = [0] * 1024
    index = 0
    while (index != -1):
        powerIndex = equation.find("*X^", index)
        if (powerIndex == -1):
            return polynome
        nb = float(equation[index:powerIndex])
        lowestIndexList = [equation[powerIndex:len(equation)].find(char) for char in ["+", "-"]]
        lowestIndexList = [a for a in lowestIndexList if a != -1]
        if (len(lowestIndexList) != 0):
            lowestIndex = min(lowestIndexList) + powerIndex
        else:
            lowestIndex = len(equation)
        power = int(equation[powerIndex + 3:lowestIndex])
        polynome[power] += nb
        index = lowestIndex
    return polynome

def simplify(polynomes):
    i = 0
    while i < 1024:
        polynomes[0][i] -= polynomes[1][i]
        polynomes[1][i] = 0
        i += 1
    if (testDegree(polynomes) == 0):
        return False
    else:
        symplifyTab(polynomes[0], 2)
    return True

def symplifyTab(numbers, i):
    j = 0
    flagRest = False
    flagTooBig = False
    while j < len(numbers):
        if i > abs(numbers[j]) and numbers[j] != 0:
            flagTooBig = True
        if (numbers[j] % i != 0):
            j = 0
            flagRest = True
            break
        j += 1
    if (flagTooBig):
        return
    elif (flagRest):
        symplifyTab(numbers, i + 1)
    else:
        j = 0
        while j < len(numbers):
            numbers[j] = numbers[j] / i
            j += 1
        symplifyTab(numbers, i + 1)

def display(polynomes):
    i = 0
    y = 0
    displayForm = ""
    while y < 2:
        flagFirst = True
        i = 1023
        while i >= 0:
            if (polynomes[y][i] != 0):
                if (flagFirst == False):
                    displayForm += " + "
                displayForm = displayForm + str(polynomes[y][i]) + " * X^" + str(i)
                flagFirst = False
            i -= 1
        if (len(displayForm) == 0):
            displayForm += "0"
        if (y == 0):
            displayForm += " = 0"
        y += 1
    print("Forme simplifier: ")
    print(displayForm)

def testDegree(polynomes):
    i = 0
    poly = 0
    while(i < 1024):
        if (polynomes[0][i] != 0):
            poly = i
        i += 1
    return poly

def calculateDiscri(polynomes):
    return (polynomes[0][1] * polynomes[0][1] - 4 * polynomes[0][2] * polynomes[0][0])

def solveDegree1(polynomes):
    polynomes[1][0] = -polynomes[0][0]
    polynomes[0][0] = 0
    polynomes[1][0] = polynomes[1][0] / polynomes[0][1]
    polynomes[0][1] = 1
    print("Une solution : X = " + str(polynomes[1][0]))

def solveNeutre(polynomes):
    solution = - polynomes[0][1] / 2 * polynomes[0][2]
    print("Une solution : X = " + str(solution))

def solvePositive(polynomes, discriminent):
    solution1 = (- polynomes[0][1] - my_math.sqrt(discriminent)) / (2 * polynomes[0][2])
    solution2 = (- polynomes[0][1] + my_math.sqrt(discriminent)) / (2 * polynomes[0][2])
    print("Deux solutions reelles : X = " + str(solution1) + " et X = " + str(solution2))

def solveNegative(polynomes, discriminent):
    solution1 = str(-polynomes[0][1] / 2 * polynomes[0][0]) + " + i * " + str(my_math.sqrt(-discriminent) / 2 * polynomes[0][0])
    solution2 = str(-polynomes[0][1] / 2 * polynomes[0][0]) + " - i * " + str(my_math.sqrt(-discriminent) / 2 * polynomes[0][0])
    print("Deux solutions reelles : X = " + solution1 + " et X = " + solution2)

def main():
    if len(sys.argv) != 2:
        print("Error")
        return
    arg = sys.argv[1]
    arg = arg.replace(' ', '')
    equations = arg.split('=')
    polynomes = list()
    for equation in equations:
        if (splitPlusMinus(equation) == None):
            return
        polynomes.append(splitPlusMinus(equation))
    if (simplify(polynomes) == False):
        if(polynomes[0][0] != 0):
            print("Il n'existe aucune solution pour l'equation")
        else:
            print("L'ensemble des reels est solutions de l'equation")
        display(polynomes)
        return
    display(polynomes)
    print("Polynome de degree " + str(testDegree(polynomes)))
    if (testDegree(polynomes) > 2):
        print("Resolution impossible")
        return
    if (polynomes[0][2] != 0):
        discriminent = calculateDiscri(polynomes)
        print("Discriminent : " + str(discriminent))
        if (discriminent > 0):
            solvePositive(polynomes, discriminent)
        if (discriminent == 0):
            solveNeutre(polynomes)
        if (discriminent < 0):
            solveNegative(polynomes, discriminent)
    elif (polynomes[0][1] != 0):
        solveDegree1(polynomes)
        

main()