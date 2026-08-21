@echo off

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

set "PY_FILE=%SCRIPT_DIR%\TSGT2G.pyw"
set "ENV_FILE=%SCRIPT_DIR%\environment.yml"
set "EXTRA_SCRIPTS_DIR=%SCRIPT_DIR%\scripts"
set "CONDA_INSTALLER=%EXTRA_SCRIPTS_DIR%\install_conda.bat"

set "CONDA_ENV=tsg2tg"

echo.
echo  ^+------------------------------------------------^+
echo  ^| The Stardrifter's Guide to the Galaxy Launcher ^|
echo  ^+------------------------------------------------^+
echo.

where conda >nul 2>nul
if %errorlevel% neq 0 (
    goto CONDANOTFOUND
) else (
    echo Conda installation found!
    goto CONDAFOUND
)

:CONDANOTFOUND
echo Could not find a conda installation!
echo Do you want to automatically download and install Miniconda? (recommended)
choice /c YN /m "Install Miniconda"
if errorlevel 2 goto NOINSTALLCONDA
if errorlevel 1 goto INSTALLCONDA

:NOINSTALLCONDA
echo.
echo ERROR: No conda installation found! Unable to launch!
echo.
<nul set /p "=Press any key to exit . . . "
pause >nul
goto END

:INSTALLCONDA
echo.
call cmd /c "%CONDA_INSTALLER%"
if errorlevel 1 goto NOINSTALLCONDA
set "CONDA_PATH=%USERPROFILE%\Miniconda3"
goto INSTALLENV

:CONDAFOUND
for /f "delims=" %%i in ('where conda') do set "CONDA_PATH=%%i"
for %%A in ("%CONDA_PATH%") do set "CONDA_PATH=%%~dpA"
set "CONDA_PATH=%CONDA_PATH:~0,-1%"
for %%A in ("%CONDA_PATH%") do set "CONDA_PATH=%%~dpA"
set "CONDA_PATH=%CONDA_PATH:~0,-1%"
goto INSTALLENV

:INSTALLENV
set "CONDA_PYTHON=%CONDA_PATH%\envs\%CONDA_ENV%\pythonw.exe"
set "CONDA=%CONDA_PATH%\condabin\conda.bat"

echo.

if not exist "%CONDA_PYTHON%" (
    echo Could not find the conda environment "%CONDA_ENV%", installing it...
    echo.
    
    set CONDA_PLUGINS_AUTO_ACCEPT_TOS=yes
    call "%CONDA%" env create -f "%ENV_FILE%"
    
    echo.
    if exist "%CONDA_PYTHON%" (
        echo Conda enviroment is ready!
        goto LAUNCH
    ) else (
        echo ERROR: Conda environment failed to install! Unable to launch!
        echo.
        <nul set /p "=Press any key to exit . . . "
        pause >nul
        goto END
    )
) else (
    echo Found conda environment!
)

:LAUNCH
echo.
echo Launching: The Stardrifter's Guide to the Galaxy...
start "" /b "%CONDA_PYTHON%" "%PY_FILE%" >nul 2>nul

:END
