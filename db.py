import sqlite3
from datetime import datetime


NAME = "town.db"


def create_tables():
    conn = sqlite3.connect(NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            User TEXT NOT NULL UNIQUE,
            Name TEXT NOT NULL,
            Created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS UserStatus (
            StatusID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            Status TEXT CHECK (Status IN ('Online', 'Offline', 'Away', 'DND')) NOT NULL,
            Time TIMESTAMP NOT NULL,
            FOREIGN KEY (UserID) REFERENCES Users (UserID)
        );
        """
    )

    conn.commit()
    conn.close()


def insert_user_status(user, name, status, time):
    conn = sqlite3.connect(NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT UserID FROM Users WHERE User = ?;", (user,))
    user_id = cursor.fetchone()

    if user_id is None:
        cursor.execute("INSERT INTO Users (User, Name) VALUES (?, ?);", (user, name))
        conn.commit()
        user_id = cursor.lastrowid
    else:
        user_id = user_id[0]

    cursor.execute(
        """
    INSERT INTO UserStatus (UserID, Status, Time)
    VALUES (?, ?, ?);
        """,
        (user_id, status, time),
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Some testing.

    NAME = "test.db"
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    create_tables()
    insert_user_status("bruce.wayne", "Bruce Wayne", "Offline", time)
    insert_user_status("diana.prince", "Diana Prince", "DND", time)
    insert_user_status("peter.parker", "Peter Parker", "Online", time)
    insert_user_status("tony.stark", "Tony Stark", "Online", time)
    insert_user_status("harry.potter", "Harry Potter", "Online", time)
    insert_user_status("walter.white", "Walter White", "Offline", time)
    insert_user_status("jon.snow", "Jon Snow", "Away", time)
    insert_user_status("james.bond", "James Bond", "Offline", time)
    insert_user_status("ethan.hunt", "Ethan Hunt", "Online", time)
    insert_user_status("thomas.shelby", "Thomas Shelby", "Away", time)
