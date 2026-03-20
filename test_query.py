import sqlite3

try:
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    cur.execute("SELECT keywords FROM blog_blog LIMIT 1")
    rows = cur.fetchall()
    print("Success: Can select keywords. Rows:", rows)
except Exception as e:
    print(f"Error selecting from database: {e}")
finally:
    if 'conn' in locals():
        conn.close()
