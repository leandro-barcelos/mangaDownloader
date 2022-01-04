import os
import requests
import shutil

manga = "uzumaki"

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
        self.URL = f"https://cdn.readdetectiveconan.com/file/mangap/4717/{chapterID}/"
        self.getPages()

    def getPages(self):
        print()
        print("=" * 20)
        print(f"\nDownloading chapter {self.number}...")
        self.pages = []
        for i in range(1,100):
            response = requests.get(self.URL + f"{i}.jpg")
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
        os.mkdir(f"Chapters/{manga}")
    except FileExistsError:
        pass

    print("Creating chapter folder...")
    chapterFolder = f"Chapters/{manga}/chapter{chapter.number}"
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


print("""

$$\   $$\                                             $$\       $$\ 
$$ |  $$ |                                            $$ |      \__|
$$ |  $$ |$$$$$$$$\ $$\   $$\ $$$$$$\$$$$\   $$$$$$\  $$ |  $$\ $$\ 
$$ |  $$ |\____$$  |$$ |  $$ |$$  _$$  _$$\  \____$$\ $$ | $$  |$$ |
$$ |  $$ |  $$$$ _/ $$ |  $$ |$$ / $$ / $$ | $$$$$$$ |$$$$$$  / $$ |
$$ |  $$ | $$  _/   $$ |  $$ |$$ | $$ | $$ |$$  __$$ |$$  _$$<  $$ |
\$$$$$$  |$$$$$$$$\ \$$$$$$  |$$ | $$ | $$ |\$$$$$$$ |$$ | \$$\ $$ |
 \______/ \________| \______/ \__| \__| \__| \_______|\__|  \__|\__|
                                                                    

                .  .              .__             .        .      
                |\\/| _.._  _  _.  |  \\ _ .    ,._ | _  _. _| _ ._.
                |  |(_][ )(_](_]  |__/(_) \\/\\/ [ )|(_)(_](_](/,[  
                          ._|                
""")

chapterInputToList(input("\n\nSelect chapters:\n-> "))
