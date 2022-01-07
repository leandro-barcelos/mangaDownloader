import os
import requests
import shutil
from logos import logos

try:
    os.mkdir(f"Chapters")
except FileExistsError:
    pass

mangas = {
    "1":{
        "name":"one-piece",
        "id": "2",
        "logo": logos[0]
    },
    "2":{
        "name": "bleach",
        "id": "552",
        "logo": logos[1]
    },
    "3":{
        "name": "tokyo-ghoul",
        "id": "4524",
        "logo": logos[2]
    },
    "4":{
        "name": "one-punch-man",
        "id": "3262",
        "logo": logos[3]
    },
    "5":{
        "name": "uzumaki",
        "id": "4717",
        "logo": logos[4]
    },
    "6":{
        "name": "yuyuhakusho",
        "id": "4926",
        "logo": logos[5]
    }
}


print(12 * "=" + " Manga Downloader" + 12 * "=")
option = input("""
1 - One Piece
2 - Bleach
3 - Tokyo Ghoul
4 - One Punch Man
5 - Uzumaki
6 - Yu Yu Hakusho


=> """)



manga = mangas[option]

class Chapter:
    def __init__(self, chapterNumber):
        self.number = chapterNumber
        if self.number < 10:
            chapterID = f'1000{self.number}000'
        elif self.number < 100:
            chapterID = f'100{self.number}000'
        elif self.number < 1000:
            chapterID = f'10{self.number}000'
        else:
            chapterID = f"1{self.number}000"
        self.URL = f"https://cdn.readdetectiveconan.com/file/mangap/{manga['id']}/{chapterID}/"
        self.getPages()

    def getPages(self):
        print()
        print("=" * 20)
        print(f"\nDownloading chapter {self.number}...")
        self.pages = []
        filetypes = [".jpg", ".jpeg", ".png"]
        type_ = 0
        for i in range(1,100):
            response = requests.get(self.URL + str(i) + filetypes[type_])
            while response.status_code == 404:
                if i <=5:
                    if type_ == len(filetypes) - 1:
                        break
                    else:
                        type_ += 1
                        response = requests.get(self.URL + str(i) + filetypes[type_])
                        continue
                break
            if response.status_code == 404:
                break

            page = response.content
            self.pages.append(page)
        print(f"Loaded!\n")
        
def chapterInputToList(chapterInput):
    chapterList = []
    try:
        chapterList = [int(chapterInput)]
    except ValueError:
        if ',' in chapterInput:
            chapterList = chapterInput.split(',')
            for i in range(len(chapterList)):
                chapterList[i] = int(chapterList[i])
        elif '-' in chapterInput:
            start, end = chapterInput.split("-")
            chapterList = list(range(int(start), int(end) + 1))
        else:
            print("ERROR: Invalid chapter.")

    print("\nDownloading chapters:")
    for chapter in chapterList:
        saveChapterToFolder(Chapter(chapter))
        

def saveChapterToFolder(chapter):
    try:
        os.mkdir(f"Chapters/{manga['name']}")
    except FileExistsError:
        pass

    print("Creating chapter folder...")
    chapterFolder = f"Chapters/{manga['name']}/chapter{chapter.number}"
    try:
        os.mkdir(chapterFolder)
    except FileExistsError:
        pass
    print("Done!")

    print("Saving pages to folder...")
    for i in range(len(chapter.pages)):
        with open(chapterFolder + f"/{i+1}.jpeg", "wb") as file:
            file.write(chapter.pages[i])
    print("Done!")

    print("Zipping the chapter folder...")
    shutil.make_archive(chapterFolder, 'zip', chapterFolder)
    print("Done!")

    print("Converting zip to cbz...")
    os.rename(chapterFolder + f'.zip', chapterFolder + f'.cbz')
    print("Done!")

    print("Removing chapter folder...")
    shutil.rmtree(chapterFolder, ignore_errors=True)
    print("Done!")

    print("Finished downloading!")


print(manga["logo"])

chapterInputToList(input("\n\nSelect chapters:\n-> "))
