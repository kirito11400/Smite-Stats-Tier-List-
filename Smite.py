import pandas as pd

def calculatetierratings(df):
    tierratings = {}

    for idx, row in df.iterrows():
        counts = {'S': 0, 'A': 0, 'B': 0, 'C': 0}

       
        for col in df.columns:
            if col != 'God' and df[col].dtype in [int, float]:
                value = row[col]
                if pd.notnull(value):
                    if value >= df[col].quantile(0.90):
                        counts['S'] += 1
                    elif value >= df[col].quantile(0.70):
                        counts['A'] += 1
                    elif value >= df[col].quantile(0.40):
                        counts['B'] += 1
                    else:
                        counts['C'] += 1

        
        maxcount = max(counts.values())
        dominanttier = [tier for tier, count in counts.items() if count == maxcount][0]

        
        if dominanttier == 'S':
            tierratings[row['God']] = 'God Tier'
        elif dominanttier == 'A':
            tierratings[row['God']] = 'King Tier'
        elif dominanttier == 'B':
            tierratings[row['God']] = 'Soldier Tier'
        else:
            tierratings[row['God']] = 'Peasant Tier'

    return tierratings

if __name__ == '__main__':
    
    df = pd.read_csv('smite_gods.csv')

    
    tierratings = calculatetierratings(df)

    
    for god, tier in tierratings.items():
        print(f"{god} is rated as: {tier}")
