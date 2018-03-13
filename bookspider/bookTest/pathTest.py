import os
dirpath = r"C:\Users\Administrator\Desktop\book" + "\\" + "a" + "\\" + "b"
filepath = dirpath + "\\" + "2.txt"
if not os.path.exists(dirpath):
    os.makedirs(dirpath)
with open(filepath,"w",encoding="utf-8") as file:
    file.write("1234567")
