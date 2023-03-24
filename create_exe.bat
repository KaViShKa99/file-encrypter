@echo off

pyinstaller --name=KaviyaEncrypter --onefile -w main.py || echo There was an error during PyInstaller build process.

del /f /q main.py
del /f /q main.spec

rd /s /q build
rd /s /q __pycache__

cd dist
copy KaviyaEncrypter.exe ..
cd ..

del /f /q KaviyaEncrypter.spec
rd /s /q dist