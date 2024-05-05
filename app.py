from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)


df = pd.read_csv('smite_gods.csv')

def calculate_tier_ratings(df):
    tierratings = {}

    for idx, row in df.iterrows():
        counts = {'S': 0, 'A': 0, 'B': 0, 'C': 0}

        # Iterate over numeric columns to categorize into 'S', 'A', 'B', 'C'
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

        # Determine dominant tier based on counts
        maxcount = max(counts.values())
        dominanttier = [tier for tier, count in counts.items() if count == maxcount][0]

        # Assign tier label based on the dominant tier
        if dominanttier == 'S':
            tierratings[row['God']] = 'God Tier'
        elif dominanttier == 'A':
            tierratings[row['God']] = 'King Tier'
        elif dominanttier == 'B':
            tierratings[row['God']] = 'Soldier Tier'
        else:
            tierratings[row['God']] = 'Peasant Tier'

    return tierratings

def process_new_god_stats(newgodstats):
    counts = {'S': 0, 'A': 0, 'B': 0, 'C': 0}

    for statvalue in newgodstats.values():
        if statvalue >= 0.90:
            counts['S'] += 1
        elif statvalue >= 0.70:
            counts['A'] += 1
        elif statvalue >= 0.40:
            counts['B'] += 1
        else:
            counts['C'] += 1

    maxcount = max(counts.values())
    dominanttier = [tier for tier, count in counts.items() if count == maxcount][0]

    if dominanttier == 'S':
        return 'God Tier'
    elif dominanttier == 'A':
        return 'King Tier'
    elif dominanttier == 'B':
        return 'Soldier Tier'
    else:
        return 'Peasant Tier'

@app.route('/')
def index():
   
    tier_ratings = calculate_tier_ratings(df)

   
    god_tier = []
    king_tier = []
    soldier_tier = []
    peasant_tier = []

    for god, tier in tier_ratings.items():
        if tier == 'God Tier':
            god_tier.append(god)
        elif tier == 'King Tier':
            king_tier.append(god)
        elif tier == 'Soldier Tier':
            soldier_tier.append(god)
        elif tier == 'Peasant Tier':
            peasant_tier.append(god)

    return render_template('index.html', god_tier=god_tier, king_tier=king_tier,
                           soldier_tier=soldier_tier, peasant_tier=peasant_tier)

@app.route('/add_god', methods=['GET', 'POST'])
def add_god():
    if request.method == 'POST':
       
        god_name = request.form['god_name']
        stat1 = float(request.form['stat1'])
        stat2 = float(request.form['stat2'])
        stat3 = float(request.form['stat3'])

  
        new_god_stats = {'Stat1': stat1, 'Stat2': stat2, 'Stat3': stat3}

   
        new_god_tier = process_new_god_stats(new_god_stats)

       
        new_god_df = pd.DataFrame([{'God': god_name, 'Stat1': stat1, 'Stat2': stat2, 'Stat3': stat3}])

       
        global df
        df = pd.concat([df, new_god_df], ignore_index=True)

        return redirect(url_for('index'))
    
    return render_template('add_god.html')

if __name__ == '__main__':
    app.run(debug=True)
