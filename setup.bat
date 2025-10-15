@echo off
setlocal enabledelayedexpansion

:: Project name
set PROJECT_NAME=TeleLang

:: Check current folder
for %%i in ("%cd%") do set CUR_DIR=%%~nxi
if not "%CUR_DIR%"=="%PROJECT_NAME%" (
    echo Error: You need to run the script from the %PROJECT_NAME% folder
    exit /b 1
)

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found!
    echo Please download and install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
)

:: Activate venv
call venv\Scripts\activate.bat

:: Install dependencies
if exist "requirements.txt" (
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
) else (
    echo requirements.txt file not found!
)

:: Ask whether to run main.py
set /p RUN_MAIN="Run main.py? (y/n): "
if /i "%RUN_MAIN%"=="y" (
    if exist "main.py" (
        python main.py
    ) else (
        echo main.py not found!
    )
) else (
    echo Exiting.
)

endlocal
