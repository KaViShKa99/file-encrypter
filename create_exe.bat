@echo off

python --version >nul 2>&1
if %errorlevel% neq 0 ( 
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.10.1/python-3.10.1-amd64.exe', 'python_installer.exe')"
    python_installer.exe /quiet
)


curl -o main.py https://raw.githubusercontent.com/KaViShKa99/file-encrypter/main/main.py

pip install pyinstaller
pyinstaller --name=KaviyaEncrypter --onefile -w main.py


del /f /q main.py
del /f /q main.spec


rd /s /q build
rd /s /q __pycache__


cd dist
copy KaviyaEncrypter.exe ..
cd ..


del /f /q KaviyaEncrypter.spec
rd /s /q dist