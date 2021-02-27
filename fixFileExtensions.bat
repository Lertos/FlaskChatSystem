@echo off

FOR /D /r %%G in (*) DO rename "%%~fG\*.PNG" "*.png"
