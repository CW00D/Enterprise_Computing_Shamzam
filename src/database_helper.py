import sqlite3
import os

class Music_Track_Database:
    def __init__(self, table="tracks"):
        self.table = table
        self.database_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
        self.database_path = os.path.join(self.database_dir, self.table + ".db")
        
        # Ensure /data directory exists
        if not os.path.exists(self.database_dir):
            os.makedirs(self.database_dir)
        
        self.make()

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

    def add_track(self):
        #Add track to db
        pass

    def remove_track(self):
        #Remove a track from db
        pass

    def get_all_tracks(self):
        #Return all tracks from db
        pass

    def check_track(self):
        #Check if track in db
        pass