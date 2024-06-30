@echo off
pyinstaller --clean --noconfirm myapp.spec

echo "Build completed. EXE file is located in dist folder of current working directory."
pause
