import requests
from bs4 import BeautifulSoup
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS ariel")
cursor.close()
db.close()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ariel"
)

cursor = db.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS pages (
        id INT AUTO_INCREMENT PRIMARY KEY,
        url VARCHAR(255) UNIQUE,
        title TEXT,
        paragraph TEXT
    )
""")
db.commit()

def dfs(url, visited):
    if url in visited:
        return
    visited.add(url)

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title"

        paragraph = soup.find("p").text if soup.find("p") else "No Content"

        cursor.execute("INSERT IGNORE INTO pages (url, title, paragraph) VALUES (%s, %s, %s)", (url, title, paragraph))
        db.commit()

        for link in soup.find_all("a", href=True):
            next_url = f"http://localhost:8000/{link['href']}"
            dfs(next_url, visited)

    except Exception as e:
        print(f"Error accessing {url}: {e}")

visited_urls = set()
dfs("http://localhost:8000/index.html", visited_urls)
cursor.close()
db.close()
print("Scraping selesai!")