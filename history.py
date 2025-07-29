import sqlite3
import os
import shutil
from datetime import datetime

def fetch_chrome_history():
    path = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History")
    temp_path = "temp_history"  # Avoid lock issues

    shutil.copy2(path, temp_path)
    conn = sqlite3.connect(temp_path)
    cursor = conn.cursor()

    cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 10")
    results = cursor.fetchall()
    
    print("\n🌐 Recent Chrome Browsing History:")
    for row in results:
        print(f"Title: {row[1]}")
        print(f"URL: {row[0]}")
        print("-" * 40)

    conn.close()
    os.remove(temp_path)

if __name__ == "__main__":
    fetch_chrome_history()
