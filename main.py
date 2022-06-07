import os
import json
import pyfiglet
from manga import Manga

mangas = 0

with open("mangas.json", "r") as file:
    mangas = json.load(file)

print(12 * "=" + " Manga Downloader" + 12 * "=")

for i, manga in enumerate(mangas):
    print(f"{i+1} - {mangas[manga]['name']}")

choice = int(input("-> "))

manga = mangas[list(mangas)[choice-1]]

manga = Manga(manga["name"], manga["id"])

print()
    
print(pyfiglet.figlet_format(manga.name))
chapters = input("Enter chapter to download: ")

chapterList = []
try:
    chapterList = [int(chapters)]
except ValueError:
    if ',' in chapters:
        chapterList = [int(x) for x in chapters.split(',')]
    elif '-' in chapters:
        start, end = [int(x) for x in chapters.split('-')]
        chapterList = [x for x in range(start, end + 1)]
    else:
        print("ERROR: Invalid chapter input.")

for i, chapter in enumerate(chapterList):
    print(f"({i+1}/{len(chapterList)})Downloading {manga.name} Chapter {i+1}...")
    manga.downloadChapter(chapter)
    print("Done! \n")