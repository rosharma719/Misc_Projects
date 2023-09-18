import pandas as pd


#These were hardcoded to make testing easier. In the future, I'll write out a CSV file + format
numChoices = 5
numGoods = 3
goodsList = ["Apples", "Bananas", "Oranges"]
choiceList = [[5, 1, 0], 
              [0, 0.5, 5], 
              [3, 0, 1], 
              [0.5, 0, 4], 
              [0, 3, 0]]
priceList = [[1, 2, 5], 
             [2, 2, 0.1], 
             [2, 1, 3], 
             [3, 5, 0.5], 
             [1, 1, 0.5]]
budgetList = [7, 1.5, 9, 3.5, 3]


# Rows = index of choice
# Columns = index of good
# [row][column] = quantity chosen/price of each good 


sumList = [[0] * numChoices for _ in range(numChoices)]

def getProduct(x, y):
    sum = 0 
    for i in range(0, numGoods): 
        sum += choiceList[x][i]*priceList[y][i]
    return(sum)


for x in range(0, numChoices): 
    for y in range(0, numChoices): 
        sumList[x][y] = getProduct(x, y)

strictPreferences = []
fakePref = []

print("DIRECT REVEALED PREFERENCES: ")
for x in range(0, numChoices): 
    for y in range(0, numChoices): 
        if y != x: 
            if sumList[x][y] < sumList[y][y] and sumList[x][y] < budgetList[y]:
                print("Choice", y + 1, "is directly revealed strictly preferred to Choice", x + 1)
                arr = [x, y] 
                strictPreferences.append(arr)

            if sumList[x][y] == sumList[y][y]: 
                print("Choice", y + 1, "is directly revealed weakly preferred to Choice", x+1 )

# SUM LIST 
# rows = choice 
# columns = price 
# [rows][columns] = cost of choices x at prices y 
# [[7, 12.0, 11, 20.0, 6.0], 
# [26.0, 1.5, 15.5, 5.0, 3.0], 
# [8, 6.1, 9, 9.5, 3.5], 
# [20.5, 1.4, 13.0, 3.5, 2.5], 
# [6, 6.0, 3, 15.0, 3.0]]


print("INDIRECT REVEALED PREFERENCES: ")
for x in range(0, len(strictPreferences)): 
    for y in range(0, len(strictPreferences)): 
        if (strictPreferences[x][0] == strictPreferences[y][1]): 
            print("Choice", strictPreferences[x][1]+1, "is indirectly revealed preferred to ", strictPreferences[y][0]+1)
#I haven't yet done strict VS weak indirect revealed preference 
