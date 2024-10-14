import pandas as pd
import ast

def getSmallDescriptions():
    df = pd.read_csv("final.csv")
    
    small_descriptions = df[df['Description'].str.split().str.len() < 30]
    #Print the lines with less than 30 words
    #print(small_descriptions)

    #return csv file with the lines with less than 30 words
    #small_descriptions.to_csv("small_descriptions.csv", index=False)
    
    return len(small_descriptions)

#print(getSmallDescriptions())

def cleanNullParticipants():
    df = pd.read_csv("final.csv")

    dfFiltered = df[(df['Winner'] == 'Massacre') | (df['Winner'] == 'Draw') | (df['Winner'] == 'Accidental incident') | (df['Winner'] == 'Incident')]
    dfFiltered.loc[dfFiltered['Participants'].isnull(), 'Participants'] = "[]"

    df.update(dfFiltered)
    print(df[df['Participants'].isnull()]['ID'])

    """
    df.loc[df['Participants'].isnull(), 'Participants'] = df.apply(
        lambda row: [row['Winner'], row['Loser']] if pd.notnull(row['Winner']) and pd.notnull(row['Loser']) else [], axis=1
    )
    """

    df.loc[df['Participants'].isnull(), 'Participants'] = df.apply(
        lambda row: (
            [name.strip() for name in str(row['Winner']).split(',')] + 
            [name.strip() for name in str(row['Loser']).split(',')]
        ) if pd.notnull(row['Winner']) and pd.notnull(row['Loser']) else [], 
        axis=1
    )

    #print(df['Participants'].isnull().sum())


    df.to_csv("final.csv", index=False)

cleanNullParticipants()