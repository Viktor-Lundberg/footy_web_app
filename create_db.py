import csv
import sqlite3


file = open('england.csv')
csvfile = csv.reader(file, dialect="excel")
clubfile = open('england_club_data.csv')
clubcsv = csv.reader(clubfile, dialect='excel')


con = sqlite3.connect('footy.db')
cursor = con.cursor()
cursor.execute('DROP TABLE IF EXISTS game')
cursor.execute('DROP TABLE IF EXISTS team')



create_db_table_team = """CREATE TABLE team (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT,
    founded TEXT,
    latitude INTEGER,
    longitude INTEGER,
    nickname TEXT,
    home_ground TEXT,
    higest_div INTEGER,
    col1 TEXT,
    col2 TEXT
)

"""

cursor.execute(create_db_table_team)


create_db_table = """CREATE TABLE game (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE,
    home_team INTEGER,
    away_team INTEGER,
    home_team_score INTEGER,
    away_team_score INTEGER,
    final_score INTEGER,
    result TEXT,
    FOREIGN KEY(home_team) REFERENCES team(team_id),
    FOREIGN KEY(away_team) REFERENCES team(team_id)
)

"""

cursor.execute(create_db_table)

# Populate club table from csv
for row in clubcsv:
    if row[1] == 'lat':
        continue
    cursor.execute('INSERT INTO team(team_name, founded, latitude, longitude, nickname, home_ground, higest_div, col1, col2) VALUES(?,?,?,?,?,?,?,?,?)'
    , (row[0],row[6],row[1],row[2],row[11], row[8], row[3],row[4], row[5]))
    
con.commit()


# Populate game table from csv and use team_id from club table as foriegn key for home_team and away_team  
for row in csvfile:
    if row[1] == 'Season':
        continue
    hometeam = (f'{row[2]}',)
    search = cursor.execute('SELECT team_id FROM team WHERE team_name = ?', hometeam)
    team_id_hometeam = cursor.fetchone()
    awayteam = (f'{row[3]}',)
    search_awayteam = cursor.execute('SELECT team_id FROM team WHERE team_name = ?', awayteam)
    team_id_awayteam = cursor.fetchone()
    print(row)
    try:
        cursor.execute('INSERT INTO game(date, home_team,away_team, home_team_score, away_team_score, final_score, result) VALUES(?,?,?,?,?,?,?)', (row[0],team_id_hometeam[0],team_id_awayteam[0],row[5], row[6], row[4], row[11]))
    except:
        if (team_id_hometeam == None) and (team_id_awayteam == None):
            cursor.execute('INSERT INTO game(date, home_team,away_team, home_team_score, away_team_score, final_score, result) VALUES(?,?,?,?,?,?,?)', (row[0],row[2], row[3],row[5], row[6], row[4], row[11]))
        elif team_id_hometeam == None:
            cursor.execute('INSERT INTO game(date, home_team,away_team, home_team_score, away_team_score, final_score, result) VALUES(?,?,?,?,?,?,?)', (row[0],row[2], team_id_awayteam[0],row[5], row[6], row[4], row[11]))
        else:
            cursor.execute('INSERT INTO game(date, home_team,away_team, home_team_score, away_team_score, final_score, result) VALUES(?,?,?,?,?,?,?)', (row[0],team_id_hometeam[0], row[3],row[5], row[6], row[4], row[11]))
    print('Values inserted')
con.commit()
    
# Update with correct foreign keys for Sunderland och Yeovil    
cursor.execute("UPDATE game SET away_team = 342 WHERE away_team = 'Sunderland'")
cursor.execute("UPDATE game SET home_team = 342 WHERE home_team = 'Sunderland'")
cursor.execute("UPDATE game SET away_team = 386  WHERE away_team = 'Yeovil'")
cursor.execute("UPDATE game SET home_team = 386 WHERE home_team = 'Yeovil'")
con.commit()    
