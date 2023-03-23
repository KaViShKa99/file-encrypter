@echo off
curl -o main.py https://raw.githubusercontent.com/KaViShKa99/file-encrypter/main/main.py
pip install pyinstaller
pyinstaller --name=KaviyaEncrypter --onefile -w main.py
del /f /q main.py
del /f /q main.spec
rd /s /q build
rd /s /q __pycache__
cd dist
copy KaviyaEncrypter.exe ..\KaviyaEncrypter.exe
del /f /q KaviyaEncrypter.spec
cd ..
rmdir /s /q dist 