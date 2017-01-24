import random

def generateRandUnique(digits):
    number=random.sample(range(0,10),digits)
    while number[0]==0:
        number=random.sample(range(0,10),digits)

    print("Random number generated.")
    print("Random number contains " + str(digits) + " digits. Never starts with 0.")
    return number

def isUniqueDigits(number,digits):
    if number.isdigit() and len(number)==digits and len(set(number))==digits:
        return True
    else:
        return False

def getInput(randomNumber):
    val=input("Guess value: ")
    while not isUniqueDigits(val,len(randomNumber)):
        print("Incorrect input. Try again...")
        val=input("Guess value: ")
    valList=[int(i) for i in list(val)]
    return valList
    

def getLivestock(num1list, num2list):
    cows=0
    bulls=0
    for i in num2list:
        if i in num1list:
            cows+=1
            if num1list.index(i)==num2list.index(i):
                cows-=1
                bulls+=1
    print("COWS: " + str(cows))
    print("BULLS: " + str(bulls))
    return [cows,bulls]

def main():
    randomNumber=generateRandUnique(4)
    guessCounter=0

    while True:
        testList=getInput(randomNumber)
        guessCounter+=1
        #print("DEBUG VALUE: RANDOM NUMBER LIST = " + str(randomNumber))
        if getLivestock(randomNumber,testList)[1]==len(randomNumber):
            print("You win! (Total guesses: " + str(guessCounter) + ")")
            break

if __name__ == "__main__":
    main()
