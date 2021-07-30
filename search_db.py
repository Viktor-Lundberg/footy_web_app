import sqlite3

con = sqlite3.connect('footy.db')
cursor = con.cursor()

# Test for UPDATE records
cursor.execute("UPDATE game SET away_team = 342 WHERE away_team = 'Sunderland'")
cursor.execute("UPDATE game SET home_team = 342 WHERE home_team = 'Sunderland'")
cursor.execute("UPDATE game SET away_team = 386  WHERE away_team = 'Yeovil'")
cursor.execute("UPDATE game SET home_team = 386 WHERE home_team = 'Yeovil'")
con.commit()
