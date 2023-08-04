#!/usr/bin/env python

import os

main_folder = os.getcwd()

subdirectories = [f.path for f in os.scandir(main_folder) if f.is_dir()]

for subdirectory in subdirectories:
    os.chdir(subdirectory) 
    for file in os.listdir(subdirectory):
        if os.path.isfile(os.path.join(subdirectory, file)):
            fileNew = file.replace(".jpg", "")
            if not os.path.exists("subdir"):
                os.makedirs("subdir")
            if not os.path.exists(subdirectory + "/subdir/" + fileNew + ".png"):
                os.system("convert -filter Lanczos -density 500 -quality 100 -resize 746x1038 " + file + " " + fileNew + ".png")
                os.rename(fileNew + ".png", subdirectory + "/subdir/" + fileNew + ".png")
    
    os.chdir(subdirectory + "/subdir/")
    os.system("montage -density 300 -quality 100 -tile 3x3 -geometry +2+2 *.png montage.png")
    if not os.path.exists("subdir"):
        os.makedirs("subdir")
    directory = os.getcwd()
    for file in os.listdir(directory):
        if "montage" in file:
            if not os.path.exists(directory + "/subdir/" + file):
                os.rename(directory + "/" + file, directory + "/subdir/" + file)
    os.chdir("subdir/")
    os.system("convert montage * montage.pdf")