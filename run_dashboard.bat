@echo off
cd /d "%~dp0"

:: Known Python location from your machine
set PYDIR=%LOCALAPPDATA%\Python\pythoncore-3.14-64
set STREAMLIT=%PYDIR%\Scripts\streamlit.exe

if exist "%STREAMLIT%" (
    echo.
    echo  ============================================================
    echo   SHINGDA DIESEL DASHBOARD
    echo   Local:   http://localhost:8501
    echo   Network: http://[YOUR-IP]:8501  (ipconfig to find IP)
    echo  ============================================================
    echo.
    "%STREAMLIT%" run app.py
    goto end
)

:: Fallback — search common locations
for %%P in (
    "%LOCALAPPDATA%\Python\pythoncore-3.14-64\Scripts\streamlit.exe"
    "%LOCALAPPDATA%\Python\pythoncore-3.13-64\Scripts\streamlit.exe"
    "%LOCALAPPDATA%\Python\pythoncore-3.12-64\Scripts\streamlit.exe"
    "%LOCALAPPDATA%\Programs\Python\Python314\Scripts\streamlit.exe"
    "%LOCALAPPDATA%\Programs\Python\Python313\Scripts\streamlit.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\Scripts\streamlit.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\Scripts\streamlit.exe"
    "C:\Python314\Scripts\streamlit.exe"
    "C:\Python313\Scripts\streamlit.exe"
    "C:\Python312\Scripts\streamlit.exe"
) do (
    if exist %%P (
        echo  Found Streamlit at %%P
        %%P run app.py
        goto end
    )
)

echo.
echo  Streamlit not found. Run this in PowerShell to install:
echo.
echo  %PYDIR%\python.exe -m pip install streamlit pandas plotly openpyxl xlrd requests
echo.
pause

:end
