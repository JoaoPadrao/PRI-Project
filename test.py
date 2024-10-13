import pandas as pd

def getSmallDescriptions():
    df = pd.read_csv("final.csv")
    
    small_descriptions = df[df['Description'].str.split().str.len() < 30]
    return len(small_descriptions)

print(getSmallDescriptions())