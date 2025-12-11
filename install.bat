@echo off
set packages=requests discord.py colorama

echo Starting installation of Python packages...

for %%p in (%packages%) do (
    echo Installing %%p...
    python -m pip install %%p
)

echo.
echo All packages have been installed!
pause
