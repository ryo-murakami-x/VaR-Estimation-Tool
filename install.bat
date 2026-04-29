@echo off
REM VaR Estimation Tool - Installation Script for Windows
REM This script sets up the VaR Estimation Tool with all dependencies

echo.
echo ================================================
echo VaR Estimation Tool - Installation (Windows)
echo ================================================
echo.

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ERROR: Python is not installed or not in PATH
        echo Please install Python 3.7 or higher from:
        echo   https://www.python.org/downloads/
        echo.
        echo Make sure to check "Add Python to PATH" during installation!
        echo.
        pause
        exit /b 1
    )
    set PYTHON=python3
) else (
    set PYTHON=python
)

for /f "tokens=*" %%i in ('%PYTHON% --version') do set PYTHON_VERSION=%%i
echo OK: %PYTHON_VERSION% found
echo.

REM Check if virtual environment exists
if exist "venv" (
    echo Virtual environment already exists. Using existing environment...
    call venv\Scripts\activate.bat
) else (
    echo Creating virtual environment...
    %PYTHON% -m venv venv
    call venv\Scripts\activate.bat
    echo OK: Virtual environment created
)

echo.
echo Upgrading pip...
%PYTHON% -m pip install --upgrade pip setuptools wheel

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ================================================
echo Installation complete!
echo ================================================
echo.
echo To activate the virtual environment in the future, run:
echo   venv\Scripts\activate.bat
echo.
echo To launch the GUI application, run:
echo   python main.py
echo.
echo To run integration tests, run:
echo   python integration_test.py
echo.
echo To use the data reader interactively, run:
echo   python data_reader.py
echo.
echo For more information, see README.md or QUICKSTART.md
echo.
pause
