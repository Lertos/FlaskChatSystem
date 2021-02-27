@echo off

for /F "tokens=*" %%A in (filesToResize.txt) do magick mogrify -resize 64x64 "%%A"

rem magick mogrify -resize 256x256 "C:\Users\Dylan\Desktop\Projects\FlaskSimpleRPG\badge.PNG"
