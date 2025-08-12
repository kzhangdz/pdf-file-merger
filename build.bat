@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Installing project dependencies from requirements.txt...
pip install -r requirements.txt

echo.
echo Generating the executable with PyInstaller...
rem The --onefile flag creates a single executable.
rem The --windowed flag prevents a console window from opening with your Tkinter app.
pyinstaller --onefile --windowed --name pdf-file-merger.exe main.py

echo.
echo Script finished.
echo Your executable can be found in the "dist" folder.
pause