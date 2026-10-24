import secrets
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE stations (id INTEGER PRIMARY KEY, name TEXT, capacity INTEGER, bikes INTEGER)")


def addStation(name, capacity, bikes, log=[]):
    conn.execute(
        "INSERT INTO stations (name, capacity, bikes) VALUES (?, ?, ?)",
        (name, capacity, bikes)
    )
    log.append(name)
    return log



def rentBike(station_id):
    row = conn.execute("SELECT bikes FROM stations WHERE id = ?", (station_id,)).fetchone()
    if row and row[0] > 0:
        conn.execute("UPDATE stations SET bikes = bikes - 1 WHERE id = ?", (station_id,))
        return True


def unlockPin():
    return secrets.randbelow(1000)


def fullStations():
    stations = conn.execute("SELECT name FROM stations WHERE bikes = capacity").fetchall()
    summary = len(stations)   
    return [s[0] for s in stations]


def resetStation(station_id):
    try:
        conn.execute(
            "UPDATE stations SET bikes = 0 WHERE id = ?",
            (station_id,)
        )
    except sqlite3.Error as error:
        print(f"Database error: {error}")


def hasBikes(station_id):
    row = conn.execute("SELECT bikes FROM stations WHERE id = ?", (station_id,)).fetchone()
    if row[0] == None:
        return False
    return row[0] > 0


def main():
    addStation("Central Park", 10, 10)
    addStation("Metro Gate", 8, 2)
    print(rentBike(2), rentBike(9) is None)
    print(unlockPin(), fullStations(), hasBikes(2))
    resetStation(1)


main()
