@echo off

set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

set PY_FILE=%SCRIPT_DIR%\TSGT2G.pyw
set ENV_FILE=%SCRIPT_DIR%\environment.yml

set CONDA_ENV=tsg2tg

echo.
echo ^+-----------------^+
echo ^| TSG2TG Launcher ^|
echo ^+-----------------^+
echo.

where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Could not find a conda installation!
    echo.
    echo ERROR: No conda installation found! Unable to launch!
    echo Download Miniconda from here: https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
    echo.
    <nul set /p "=Press any key to exit . . . "
    pause >nul
    exit /b
) else (
    echo Conda installation found!
)

for /f "delims=" %%i in ('where conda') do set "CONDA_PATH=%%i"
for %%A in ("%CONDA_PATH%") do set "CONDA_PATH=%%~dpA"
set CONDA_PATH=%CONDA_PATH:~0,-1%
for %%A in ("%CONDA_PATH%") do set "CONDA_PATH=%%~dpA"
set CONDA_PATH=%CONDA_PATH:~0,-1%

set CONDA_PYTHON=%CONDA_PATH%\envs\%CONDA_ENV%\pythonw.exe

echo.
if not exist "%CONDA_PYTHON%" (
    echo Could not find the conda environment "%CONDA_ENV%", installing it...
    echo.
    
    call conda env create -f "%ENV_FILE%"
    echo.
    
    echo Conda enviroment is ready!
) else (
    echo Found conda environment!
)



echo.
echo Launching TSG2TG...
start "" /b "%CONDA_PYTHON%" "%PY_FILE%" >nul 2>nul
