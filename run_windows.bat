@echo off
chcp 65001 >nul
title THE HOLLOW LINE
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
    python play.py %*
) else (
    py -3 play.py %*
)
if errorlevel 1 pause
