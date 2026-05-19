@echo off
set PYTHON=%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe
set SCRIPT="%~dp0_read_joblist.py"

echo.
echo  Running Job List diagnostic...
echo.

if exist "%PYTHON%" (
    "%PYTHON%" %SCRIPT%
    goto done
)

for %%P in (
    "%LOCALAPPDATA%\Python\pythoncore-3.13-64\python.exe"
    "%LOCALAPPDATA%\Python\pythoncore-3.12-64\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python314\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "C:\Python314\python.exe"
    "C:\Python313\python.exe"
) do (
    if exist %%P ( %%P %SCRIPT% & goto done )
)

echo  Python not found.
pause
goto end

:done
echo.
echo  Done! Output saved to:
echo  I:\Fleet\Diesel Report\Diesel Consumption\_joblist_info.txt
echo.
pause
:end
