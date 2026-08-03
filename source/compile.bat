@echo off

rem Change this to point to the installation directory for Borland C++ 3.1
rem The N: drive is the Noctis-IV-Plus folder
set BCPP31_DIR=N:\bc.31



echo Building Noctis IV Plus...

rem Append Borland C++ 3.1 to the PATH
set PATH=%PATH%;%BCPP31_DIR%\bin;%BCPP31_DIR%\INCLUDE

rem Ensure the 'bin' folder exists and is empty
if exist bin\NUL deltree /Y bin
mkdir bin

rem Build Noctis IV using the make tool
make -fnoctis.mak -DALL=DEF_ALL -B

rem Handle failure to build
if exist bin\noctis.exe goto success
echo Build failed!
echo Press any key to exit . . .
pause >nul
goto done

rem Handle successful build
:success
echo Build completed successfully!

rem Move built executable
echo Moving built executable to modules folder...
copy bin\noctis.exe ..\modules\noctis.exe /y
copy supports.nct ..\data /y
del bin\noctis.exe
echo Executable moved successfully!

rem Pause before running
echo Press any key to run Noctis IV Plus . . .
pause >nul

rem Run Noctis IV
cd ..
modules\noctis.exe
cd ..
cd source

rem End of program
:done
