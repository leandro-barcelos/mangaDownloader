import os
import requests
import shutil


class Manga:
    def __init__(self, name, id):
        self.name = name
        self.mangaID = id
        self.mangaURL = f"https://cdn.readdetectiveconan.com/file/mangap/{self.mangaID}/"
        
    def downloadChapter(self, chapter_number):
        
        try:
            os.mkdir(f"Chapters")
        except FileExistsError:
            pass
        
        try:
            os.mkdir(f"Chapters/{self.name}")
        except FileExistsError:
            pass
        
        # GET CHAPTER URL
        
        chapterID = "1"
        chapter_number = str(chapter_number)
        
        while len(chapter_number) < 4:
            chapter_number = "0" + chapter_number
            
        chapterID += f"{chapter_number}000/"
        
        chapterURL = self.mangaURL + chapterID
        
        # DOWNLOAD PAGES
        
        type = "jpg"
        
        response = requests.get(chapterURL + f"1.{type}")
        if response.status_code == 404:
            type = "jpeg"
            response = requests.get(chapterURL + f"1.{type}")
            
        
        chapterFolder = f"Chapters/{self.name}/chapter{chapter_number}"    
        
        if response.status_code != 404:
            try:
                os.mkdir(chapterFolder)
            except FileExistsError:
                pass
        
        
        i = 1
        while response.status_code != 404:
            
            page = response.content
            
            with open(chapterFolder + f"/{i}.{type}", "wb") as file:
                file.write(page)
            
            i += 1
            response = requests.get(chapterURL + f"{i}.{type}")
            
        shutil.make_archive(chapterFolder, 'zip', chapterFolder)

        os.rename(chapterFolder + f'.zip', chapterFolder + f'.cbz')

        shutil.rmtree(chapterFolder, ignore_errors=True)
        