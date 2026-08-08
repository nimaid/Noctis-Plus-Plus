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

echo Testing for conda installation...
where conda >nul 2>nul
if %errorlevel% neq 0 (
    echo Could not find "conda".
    echo.
    echo ERROR: No conda installation found! Unable to launch!
    echo Download a Conda distribution from here: https://www.anaconda.com/download/success
    echo.
    <nul set /p "=Press any key to exit . . . "
    pause >nul
    exit /b
) else (
    echo Conda installation found!
)

echo.
echo Looking for conda environment...
conda env list | findstr /R /C:"\<%CONDA_ENV%\>" >nul
if %errorlevel% neq 0 (
    echo Could not find the conda environment "%CONDA_ENV%", installing it...
    echo.
    
    conda env create -f "%ENV_FILE%"
    echo.
    
    echo Conda enviroment is ready!
) else (
    echo Found conda environment: "%CONDA_ENV%"
)



echo.
echo Launching TSG2TG...
start "" /b conda run -n %CONDA_ENV% pythonw "%PY_FILE%"
echo Launched!
echo.
echo You can safely close this window now.
