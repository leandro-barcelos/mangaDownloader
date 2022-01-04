import os


try:
    os.mkdir(f"Chapters")
except FileExistsError:
    pass

print(12 * "=" + " Manga Downloader" + 12 * "=")
manga = input("""
1 - One Piece
2 - Bleach
3 - Tokyo Ghoul
4 - One Punch Man


=> """)

if manga == "1":
    import onePiece
elif manga == "2":
    import bleach
elif manga == "3":
    import tokyoGhoul
elif manga == "4":
    import onePunch
