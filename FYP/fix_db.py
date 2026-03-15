import sqlite3

try:
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    # Add the column if it doesn't exist
    cur.execute("ALTER TABLE blog_blog ADD COLUMN keywords varchar(255) NOT NULL DEFAULT ''")
    conn.commit()
    print("Successfully added keywords column to blog_blog")
except Exception as e:
    print(f"Error modifying database: {e}")
finally:
    if 'conn' in locals():
        conn.close()
