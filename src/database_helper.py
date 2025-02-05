import sqlite3
import os

class MusicTrackDatabase:
    def __init__(self, table="tracks"):
        self.table = table
        self.database_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
        self.database_path = os.path.join(self.database_dir, self.table + ".db")

        self.ensure_data_directory()  # Ensure /data directory exists
        self.make()

    def ensure_data_directory(self):
        """Ensure that the /data directory exists."""
        if not os.path.exists(self.database_dir):
            os.makedirs(self.database_dir)

    def make(self):
        """Create the tracks table if it does not exist."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {self.table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    artist TEXT NOT NULL,
                    file_path TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def insert(self, js):
        """Insert a new track into the database."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {self.table} (title, artist, file_path) VALUES (?, ?, ?)",
                (js["title"], js["artist"], js["file_path"])
            )
            connection.commit()
            return cursor.lastrowid

    def remove_track_by_id(self, track_id):
        """Deletes a track by ID and returns the number of deleted rows."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {self.table} WHERE id=?", (track_id,))
            connection.commit()
            return cursor.rowcount

    def find_track_by_title_and_artist(self, title, artist):
        """Retrieves a single track with given details (returns None if not found)."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT id, title, artist, file_path FROM {self.table} WHERE title=? AND artist=?", (title, artist))
            row = cursor.fetchone()
            if row:
                return {"id": row[0], "title": row[1], "artist": row[2], "file_path": row[3]}
            return None

    def get_all_tracks(self):
        """Retrieves all tracks from the database (returns an empty list if none exist)."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT id, title, artist, file_path FROM {self.table}")
            rows = cursor.fetchall()
            return [{"id": row[0], "title": row[1], "artist": row[2], "file_path": row[3]} for row in rows] if rows else []
