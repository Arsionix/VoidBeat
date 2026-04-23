import sqlite3

conn = sqlite3.connect('db/voidbeat.db')
cursor = conn.cursor()

tracks = [
    ("Трек 1", "Исполнитель 1", "/static/music/track1.mp3", "flow", 180),
    ("Трек 2", "Исполнитель 2", "/static/music/track2.mp3", "flow", 210),
    ("Трек 3", "Исполнитель 3", "/static/music/track3.mp3", "flow", 195),
]

cursor.execute("DELETE FROM tracks")

for t in tracks:
    cursor.execute("""
        INSERT INTO tracks (title, artist, file_url, mode, duration, plays_count)
        VALUES (?, ?, ?, ?, ?, 0)
    """, t)

conn.commit()
conn.close()
