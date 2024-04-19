@echo off
cls
pyinstaller --clean --onefile --noconsole --icon="icon/icon.ico"  main.py
rmdir "build" /s /q
del "main.spec"