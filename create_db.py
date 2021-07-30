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

# Club table
for row in clubcsv:
    if row[1] == 'lat':
        continue
    cursor.execute('INSERT INTO team(team_name, founded, latitude, longitude, nickname, home_ground, higest_div, col1, col2) VALUES(?,?,?,?,?,?,?,?,?)'
    , (row[0],row[6],row[1],row[2],row[11], row[8], row[3],row[4], row[5]))
    
con.commit()


# game table TO DO AWAY_TEAM; UPDATE SUNDERLAND AND YOVIL, + Game values
for row in csvfile:
    if row[1] == 'Season':
        continue
    hometeam = (f'{row[2]}',)
    search = cursor.execute('SELECT team_id FROM team WHERE team_name = ?', hometeam)
    team_id_hometeam = cursor.fetchone()
    awayteam = (f'{row[3]}',)
    print(awayteam)
    search_awayteam = cursor.execute('SELECT team_id FROM team WHERE team_name = ?', awayteam)
    team_id_awayteam = cursor.fetchone()
    print(team_id_awayteam)
    print(row)
    try:
        cursor.execute('INSERT INTO game(date, home_team,away_team) VALUES(?,?,?)', (row[0],team_id_hometeam[0],team_id_awayteam[0]))
    except:
        if (team_id_hometeam == None) and (team_id_awayteam == None):
            cursor.execute('INSERT INTO game(date, home_team, away_team) VALUES(?,?,?)', (row[0],row[2], row[3]))
        elif team_id_hometeam == None:
            cursor.execute('INSERT INTO game(date, home_team, away_team) VALUES(?,?,?)', (row[0],row[2], team_id_awayteam[0]))
        else:
            cursor.execute('INSERT INTO game(date, home_team, away_team) VALUES(?,?,?)', (row[0],team_id_hometeam[0], row[3]))
    print('HOME TEAM INSERTED')
con.commit()
    
    
    
