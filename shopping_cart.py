import pandas as pd
from scipy.stats.mstats import spearmanr

data = pd.read_csv("C:/Users/kragg/OneDrive/Desktop/SHOPPING_CART - Sheet1.csv")

sat = data["SATISFACTION_RANK"]
for x in range(1,len(data.columns)): 
    y = data[data.columns[x]].values.tolist()
    if ((-1*spearmanr(sat,y)[0]) > 0.5):
        print("Best metrics of satisfaction: ", data.columns[x])
    if ((spearmanr(sat,y)[0]) > 0.5):
        print("Best metrics of dissatisfaction: ", data.columns[x])


for x in range(1, len(data.columns)):
    y = data[data.columns[x]].values.tolist()
    for z in range(1, len(data.columns)): 
        c = data[data.columns[z]].values.tolist()
        if ((-1*spearmanr(c,y)[0]) > 0.5 and c != y):
            print("Predicted complements: ", data.columns[x], " ", data.columns[z])
        if ((spearmanr(c,y)[0]) > 0.5 and c != y):
            print("Predicted substitutes: ", data.columns[x], " ", data.columns[z])

#Insights: Significant potential for miscorrelation (e.g. tea and butter are predicted substitutes)
#We lose predictive insight with generality and convenience: 
#"Good, neutral, bad" are more likely metrics than "Rank this compared to your last 30 grocery trips"


        
