@echo off

set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

set CONDA_ENV=tsg2tg

echo.
echo ^+-----------------^+
echo ^| TSG2TG Launcher ^|
echo ^+-----------------^+
echo.

echo Looking for conda environment...
conda env list | findstr /R /C:"\<%CONDA_ENV%\>" >nul
if %errorlevel% neq 0 (
    echo Could not find the conda environment "%CONDA_ENV%", installing it...
    echo.
    
    conda env create -f environment.yml
) else (
    echo Found conda environment: "%CONDA_ENV%"
)



echo.
echo Launching TSG2TG...
start /b conda run -n %CONDA_ENV% pythonw TSGT2G.pyw
echo Launched!
echo.
echo You can safely close this window now.