import sqlite3
import os

class MusicTrackDatabase:
    def __init__(self, table="tracks"):
        self.table = table
        self.database_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
        self.database_path = os.path.join(self.database_dir, self.table + ".db")

        self.ensure_data_directory()
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
                    title TEXT PRIMARY KEY,
                    encoded_track TEXT NOT NULL
                )
                """
            )
            connection.commit()

    def insert(self, js):
        """Insert a new track into the database if the title is not already present."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            
            # Check if the title already exists
            cursor.execute(f"SELECT 1 FROM {self.table} WHERE title = ?", (js["title"],))
            if cursor.fetchone():  # If a row is found, the title exists
                return 409  # Conflict
            
            # Insert the new track
            cursor.execute(
                f"INSERT INTO {self.table} (title, encoded_track) VALUES (?, ?)",
                (js["title"], js["encoded_track"])
            )
            connection.commit()
            return cursor.lastrowid

    def remove_track_by_title(self, title):
        """Deletes a track by ID and returns the number of deleted rows."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f"DELETE FROM {self.table} WHERE title=?", (title,))
            connection.commit()
            return cursor.rowcount

    def find_track_by_title(self, title):
        """Retrieves a single track with given details (returns None if not found)."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT title, encoded_track FROM {self.table} WHERE title=?", (title,))
            row = cursor.fetchone()
            if row:
                return {"title": row[0], "encoded_track": row[1]}
            return None

    def get_all_tracks(self):
        """Retrieves all tracks from the database (returns an empty list if none exist)."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute(f"SELECT title, encoded_track FROM {self.table}")
            rows = cursor.fetchall()
            return [{"title": row[0], "encoded_track": row[1]} for row in rows] if rows else []

    def reset_database(self):
        """Deletes all tracks from the database."""
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM tracks")
            connection.commit()